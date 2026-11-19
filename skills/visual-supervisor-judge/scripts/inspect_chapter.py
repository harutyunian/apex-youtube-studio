#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Stage 1 Deterministic Video, Frame & Audio Telemetry Inspector (`inspect_chapter.py`)
for the `visual-supervisor-judge` skill.

Performs:
- PySceneDetect (`ContentDetector` + `ThresholdDetector`) scene boundary detection
- Reconciliation with chapter EDL (if provided)
- FFmpeg `blackdetect`, `silencedetect`, and `ebur128` loudness/peak telemetry
- Multi-frame extraction per shot (`START` 12%, `MID` 50%, `END` 88%, plus 30%/70% on shots >15s)
- Annotated Contact Sheet generation (`{chapter_id}_contact_sheets/contact_sheet_*.jpg`)
- Automatic anomaly flagging into `{chapter_id}_critical_frames/`
"""

from __future__ import annotations

import argparse
import json
import math
import re
import subprocess
from pathlib import Path
from typing import Any

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

try:
    from scenedetect import SceneManager, open_video
    from scenedetect.detectors import ContentDetector, ThresholdDetector

    HAS_SCENEDETECT = True
except Exception:
    HAS_SCENEDETECT = False

FONT_BOLD = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
FONT_BLACK = "/System/Library/Fonts/Supplemental/Arial Black.ttf"


def _font(path: str, size: int) -> ImageFont.FreeTypeFont:
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.load_default()


def fmt_ts(sec: float) -> str:
    sec = max(0.0, float(sec))
    m = int(sec // 60)
    s = sec - m * 60
    return f"{m:02d}:{s:05.2f}"


def run_scenedetect(video_path: Path) -> list[dict[str, float]]:
    if not HAS_SCENEDETECT:
        return []
    video = open_video(str(video_path), backend="opencv")
    sm = SceneManager()
    sm.add_detector(ContentDetector(threshold=22.0, min_scene_len=15))
    sm.add_detector(ThresholdDetector(threshold=12.0, min_scene_len=12))
    sm.detect_scenes(video, show_progress=False)
    scene_list = sm.get_scene_list()
    out = []
    for i, (st, en) in enumerate(scene_list, 1):
        s0 = round(float(st.seconds), 3)
        s1 = round(float(en.seconds), 3)
        out.append(
            {
                "detected_scene": i,
                "start_sec": s0,
                "end_sec": s1,
                "duration_sec": round(s1 - s0, 3),
            }
        )
    return out


def run_ffmpeg_telemetry(video_path: Path) -> dict[str, Any]:
    probe_raw = subprocess.check_output(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration,size,bit_rate:stream=codec_type,codec_name,width,height,r_frame_rate,pix_fmt,sample_rate,channels",
            "-of",
            "json",
            str(video_path),
        ],
        text=True,
    )
    probe = json.loads(probe_raw)
    dur = float(probe["format"]["duration"])

    blk_err = subprocess.run(
        [
            "ffmpeg",
            "-i",
            str(video_path),
            "-vf",
            "blackdetect=d=0.12:pix_th=0.08",
            "-an",
            "-f",
            "null",
            "-",
        ],
        capture_output=True,
        text=True,
    ).stderr
    black_intervals = [
        {"start_sec": float(a), "end_sec": float(b), "duration_sec": float(c)}
        for a, b, c in re.findall(
            r"black_start:([0-9.]+)\s+black_end:([0-9.]+)\s+black_duration:([0-9.]+)",
            blk_err,
        )
    ]

    sil_err = subprocess.run(
        [
            "ffmpeg",
            "-i",
            str(video_path),
            "-af",
            "silencedetect=noise=-38dB:d=1.8",
            "-vn",
            "-f",
            "null",
            "-",
        ],
        capture_output=True,
        text=True,
    ).stderr
    silence_intervals = [
        {"start_sec": float(a), "end_sec": float(b), "duration_sec": float(c)}
        for a, b, c in re.findall(
            r"silence_start:\s*([0-9.]+).*?silence_end:\s*([0-9.]+)\s*\|\s*silence_duration:\s*([0-9.]+)",
            sil_err,
            flags=re.DOTALL,
        )
    ]

    ebur_err = subprocess.run(
        [
            "ffmpeg",
            "-nostats",
            "-i",
            str(video_path),
            "-filter_complex",
            "ebur128=peak=true",
            "-f",
            "null",
            "-",
        ],
        capture_output=True,
        text=True,
    ).stderr
    m_i = re.findall(r"I:\s*(-?[0-9.]+)\s*LUFS", ebur_err)
    m_lra = re.findall(r"LRA:\s*(-?[0-9.]+)\s*LU", ebur_err)
    m_tp = re.findall(r"Peak:\s*(-?[0-9.]+)\s*dBFS", ebur_err)

    return {
        "duration_sec": round(dur, 3),
        "duration_mmss": fmt_ts(dur),
        "file_size_mb": round(int(probe["format"]["size"]) / (1024 * 1024), 2),
        "streams": probe["streams"],
        "black_intervals": black_intervals,
        "silence_intervals_gt_1_8s": silence_intervals,
        "audio_ebur128": {
            "integrated_lufs": float(m_i[-1]) if m_i else None,
            "loudness_range_lu": float(m_lra[-1]) if m_lra else None,
            "true_peak_dbfs": float(m_tp[-1]) if m_tp else None,
        },
    }


def extract_frame_rgb(
    cap: cv2.VideoCapture, fps: float, total_frames: int, t_sec: float
) -> np.ndarray:
    f_idx = max(0, min(total_frames - 1, int(round(t_sec * fps))))
    cap.set(cv2.CAP_PROP_POS_FRAMES, f_idx)
    ok, bgr = cap.read()
    if not ok or bgr is None:
        return np.zeros((1080, 1920, 3), dtype=np.uint8)
    return cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)


def inspect_chapter(
    video_path: Path,
    out_dir: Path,
    chapter_id: str = "chapter_01",
    edl_path: Path | None = None,
) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    cs_dir = out_dir / f"{chapter_id}_contact_sheets"
    cf_dir = out_dir / f"{chapter_id}_critical_frames"
    cs_dir.mkdir(parents=True, exist_ok=True)
    cf_dir.mkdir(parents=True, exist_ok=True)

    ff_tel = run_ffmpeg_telemetry(video_path)
    detected_scenes = run_scenedetect(video_path)

    # Build authoritative shot list: prefer declared EDL boundaries (if available) enriched with PySceneDetect boundaries, else PySceneDetect directly
    shots: list[dict[str, Any]] = []
    if edl_path and edl_path.exists():
        edl_data = json.loads(edl_path.read_text(encoding="utf-8"))
        for item in edl_data.get("shots", []):
            shots.append(
                {
                    "shot_number": int(item["shot_index"]) + 1,
                    "start_sec": float(item["start_sec"]),
                    "end_sec": float(item["end_sec"]),
                    "duration_sec": float(item["duration_sec"]),
                    "kind": item.get("kind", "unknown"),
                    "asset_path": item.get("path", ""),
                    "provenance_badge": item.get("prov"),
                    "lower_third_title": item.get("title"),
                    "lower_third_sub": item.get("sub"),
                }
            )
    elif detected_scenes:
        for sc in detected_scenes:
            shots.append(
                {
                    "shot_number": sc["detected_scene"],
                    "start_sec": sc["start_sec"],
                    "end_sec": sc["end_sec"],
                    "duration_sec": sc["duration_sec"],
                    "kind": "detected_cut",
                    "asset_path": "",
                    "provenance_badge": None,
                    "lower_third_title": None,
                    "lower_third_sub": None,
                }
            )
    else:
        dur = ff_tel["duration_sec"]
        step = 10.0
        n_s = max(1, int(math.ceil(dur / step)))
        for i in range(n_s):
            s0 = round(i * step, 3)
            s1 = round(min(dur, (i + 1) * step), 3)
            shots.append(
                {
                    "shot_number": i + 1,
                    "start_sec": s0,
                    "end_sec": s1,
                    "duration_sec": round(s1 - s0, 3),
                    "kind": "uniform_window",
                    "asset_path": "",
                    "provenance_badge": None,
                    "lower_third_title": None,
                    "lower_third_sub": None,
                }
            )

    cap = cv2.VideoCapture(str(video_path))
    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    total_frames = int(
        cap.get(cv2.CAP_PROP_FRAME_COUNT) or round(ff_tel["duration_sec"] * fps)
    )

    black_ivs = ff_tel["black_intervals"]
    shot_telemetry: list[dict[str, Any]] = []
    triplets_for_sheets: list[
        tuple[dict[str, Any], Image.Image, Image.Image, Image.Image]
    ] = []

    for sh in shots:
        s0, s1, dur = sh["start_sec"], sh["end_sec"], sh["duration_sec"]
        # Sample START (12% or +0.45s past fade-in), MID (50%), END (88% or -0.45s before fade-out)
        t_start = min(s1 - 0.05, s0 + min(0.55, dur * 0.14))
        t_mid = (s0 + s1) / 2.0
        t_end = max(s0 + 0.05, s1 - min(0.55, dur * 0.14))

        rgb_s = extract_frame_rgb(cap, fps, total_frames, t_start)
        rgb_m = extract_frame_rgb(cap, fps, total_frames, t_mid)
        rgb_e = extract_frame_rgb(cap, fps, total_frames, t_end)

        # Also sample boundary frame (s1 - 0.04s) to detect dip-to-black transitions between consecutive shots!
        rgb_boundary = extract_frame_rgb(cap, fps, total_frames, max(s0, s1 - 0.04))
        boundary_luma = float(np.mean(rgb_boundary))

        luma_mid = float(np.mean(rgb_m))
        contrast_std = float(np.std(rgb_m))
        motion_delta_sm = float(
            np.mean(np.abs(rgb_m.astype(np.float32) - rgb_s.astype(np.float32)))
        )
        motion_delta_me = float(
            np.mean(np.abs(rgb_e.astype(np.float32) - rgb_m.astype(np.float32)))
        )

        # Extra intermediate frame checks on long shots (>15.0s)
        extra_samples = []
        if dur > 15.0:
            for r in (0.30, 0.70):
                tx = s0 + dur * r
                rgb_x = extract_frame_rgb(cap, fps, total_frames, tx)
                extra_samples.append(
                    {
                        "t_sec": round(tx, 2),
                        "mean_luma": round(float(np.mean(rgb_x)), 1),
                    }
                )

        # Check overlap with blackdetect intervals
        blk_hits = [
            b for b in black_ivs if max(s0, b["start_sec"]) < min(s1, b["end_sec"])
        ]

        auto_flags = []
        if dur < 2.2:
            auto_flags.append(f"SHORT_SHOT({dur:.2f}s<2.2s)")
        if dur > 15.5:
            auto_flags.append(f"OVERLONG_SHOT({dur:.2f}s>15.5s)")
        if motion_delta_sm < 0.8 and motion_delta_me < 0.8 and dur > 3.5:
            auto_flags.append("STATIC_FREEZE_DETECTED")
        if boundary_luma < 6.0 and luma_mid > 24.0:
            auto_flags.append(f"DIP_TO_BLACK_TRANSITION(end_luma={boundary_luma:.1f})")
        if any(b["duration_sec"] > 0.45 for b in blk_hits):
            auto_flags.append("ACCIDENTAL_BLACK_GAP_GT_0.45S")
        if "ai_stills" in sh["asset_path"] and not sh.get("provenance_badge"):
            auto_flags.append("MISSING_AI_PROVENANCE_BADGE")

        rec = {
            **sh,
            "start_ts": fmt_ts(s0),
            "end_ts": fmt_ts(s1),
            "sample_timestamps": {
                "start": round(t_start, 2),
                "mid": round(t_mid, 2),
                "end": round(t_end, 2),
            },
            "metrics": {
                "mid_luma": round(luma_mid, 1),
                "contrast_std": round(contrast_std, 1),
                "motion_delta_start_mid": round(motion_delta_sm, 2),
                "motion_delta_mid_end": round(motion_delta_me, 2),
                "end_boundary_luma": round(boundary_luma, 1),
            },
            "extra_long_shot_samples": extra_samples,
            "black_dips_in_shot": blk_hits,
            "auto_telemetry_flags": auto_flags,
        }
        shot_telemetry.append(rec)

        im_s = Image.fromarray(rgb_s)
        im_m = Image.fromarray(rgb_m)
        im_e = Image.fromarray(rgb_e)
        triplets_for_sheets.append((rec, im_s, im_m, im_e))

        # Save critical frame if telemetry flagged an issue (excluding benign end fade on final shot)
        meaningful_flags = [f for f in auto_flags if not f.startswith("DIP_TO_BLACK")]
        if meaningful_flags:
            cf_out = (
                cf_dir
                / f"shot_{sh['shot_number']:03d}_{fmt_ts(t_mid).replace(':', 'm')}s_telemetry.jpg"
            )
            im_m.save(cf_out, "JPEG", quality=93)

    cap.release()

    # Render Contact Sheets (6 shots per sheet, 3 columns: START | MID | END)
    per_sheet = 6
    thumb_w, thumb_h = 560, 315
    pad_x, row_h, hdr_h = 28, 378, 76
    sheet_w = pad_x * 4 + thumb_w * 3  # 1792 px

    f_hdr = _font(FONT_BLACK, 24)
    f_row = _font(FONT_BOLD, 17)
    f_sm = _font(FONT_BOLD, 14)

    sheet_paths = []
    for sh_idx in range(0, len(triplets_for_sheets), per_sheet):
        batch = triplets_for_sheets[sh_idx : sh_idx + per_sheet]
        sheet_h = hdr_h + len(batch) * row_h + 24
        sheet = Image.new("RGB", (sheet_w, sheet_h), (12, 16, 24))
        d = ImageDraw.Draw(sheet)

        s_num = sh_idx // per_sheet + 1
        d.text(
            (pad_x, 22),
            f"VISUAL SUPERVISOR CONTACT SHEET #{s_num:02d}  •  {chapter_id.upper()}  •  COLUMNS: [START 12%]  |  [MID 50%]  |  [END 88%]",
            font=f_hdr,
            fill=(245, 198, 66),
        )

        y = hdr_h
        for rec, im_s, im_m, im_e in batch:
            flags_str = (
                ", ".join(rec["auto_telemetry_flags"])
                if rec["auto_telemetry_flags"]
                else "CLEAN"
            )
            flag_col = (
                (255, 105, 105) if rec["auto_telemetry_flags"] else (120, 225, 155)
            )
            header_line = (
                f"SHOT #{rec['shot_number']:02d}  [{rec['start_ts']} -> {rec['end_ts']} | {rec['duration_sec']:.2f}s]  "
                f"src={Path(rec['asset_path']).name or rec['kind']}  |  motion={rec['metrics']['motion_delta_start_mid']:.1f}/{rec['metrics']['motion_delta_mid_end']:.1f}"
            )
            d.text((pad_x, y), header_line[:115], font=f_row, fill=(235, 242, 255))
            d.text(
                (pad_x + 1180, y + 2),
                f"FLAGS: {flags_str[:48]}",
                font=f_sm,
                fill=flag_col,
            )

            for c_i, (lbl, im_f) in enumerate(
                [("START", im_s), ("MID", im_m), ("END", im_e)]
            ):
                tx = pad_x + c_i * (thumb_w + pad_x)
                ty = y + 30
                th = im_f.resize((thumb_w, thumb_h), Image.Resampling.LANCZOS)
                sheet.paste(th, (tx, ty))
                d.rectangle(
                    [tx, ty, tx + thumb_w - 1, ty + thumb_h - 1],
                    outline=(70, 95, 130),
                    width=2,
                )
                bx1, by1 = tx + thumb_w - 82, ty + thumb_h - 28
                d.rectangle(
                    [bx1, by1, tx + thumb_w - 6, ty + thumb_h - 6], fill=(8, 12, 20)
                )
                d.text((bx1 + 10, by1 + 3), lbl, font=f_sm, fill=(245, 198, 66))

            y += row_h

        sp = cs_dir / f"contact_sheet_{s_num:02d}.jpg"
        sheet.save(sp, "JPEG", quality=90)
        sheet_paths.append(str(sp))

    telemetry_out = {
        "chapter_id": chapter_id,
        "video_path": str(video_path),
        "pyscenedetect_available": HAS_SCENEDETECT,
        "pyscenedetect_cut_count": len(detected_scenes),
        "declared_or_evaluated_shot_count": len(shot_telemetry),
        "ffmpeg_telemetry": ff_tel,
        "contact_sheets": sheet_paths,
        "shots": shot_telemetry,
    }
    tel_json = out_dir / f"{chapter_id}_telemetry.json"
    tel_json.write_text(
        json.dumps(telemetry_out, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    print(
        f"[Telemetry OK] {chapter_id}: {len(shot_telemetry)} shots, {len(sheet_paths)} contact sheets, "
        f"LUFS={ff_tel['audio_ebur128']['integrated_lufs']}, PySceneDetect={len(detected_scenes)} scenes -> {tel_json}"
    )
    return tel_json


def main() -> None:
    ap = argparse.ArgumentParser(
        description="Deterministic documentary chapter telemetry & contact sheet builder."
    )
    ap.add_argument("--video", required=True, type=Path)
    ap.add_argument("--out-dir", required=True, type=Path)
    ap.add_argument("--chapter-id", default="chapter_01")
    ap.add_argument("--edl", type=Path, default=None)
    args = ap.parse_args()
    inspect_chapter(args.video, args.out_dir, args.chapter_id, args.edl)


if __name__ == "__main__":
    main()
