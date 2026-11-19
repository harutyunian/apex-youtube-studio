#!/usr/bin/env python3
"""
YouTube Retention Architecture Auditor (5zu8s38ZwtQ + I4nd9t84UvI).

Verifies rendered MP4, thumbnail, title, and optional transcript/script against:
1. 0:00-0:05 Expectation Lock:
   - First sentence matches Title keywords (when transcript/script provided)
   - Frame 1 (0.5s-4.0s) matches Thumbnail palette & luminance profile
   - Zero banned greetings ("welcome back", "hey guys", etc.)
2. 0:00-0:20 Dynamic Hook Gate:
   - >= 7 visual changes in first 20s (target 8+, ~2.5s/shot)
   - Max static hold in first 20s <= 4.0s (hard fail > 5.5s)
   - Generates `_retention_hook_sheet.jpg` (Thumbnail + 0.5s..19.5s)
3. Video Body Visual Variety & Anti-Same-Room Stagnation:
   - Median cut duration <= 3.2s (long-form) / <= 2.5s (Shorts)
   - Zero truly static stretches >= 10.0s; warns on holds > 5.5s
   - Measures inter-cut spatial/color contrast across cuts (flags >45% identical-backdrop cuts)
   - Generates `_retention_body_sheet.jpg` (25%, 45%, 65%, 80%, 92%, End-2s + longest hold)
4. Energy Cycling (Anti-Middle-Valley):
   - Compares Q1, Q2, Q3, Q4 cut cadence per minute & final-20% pacing
5. Audio Dead Air & Ending Activity:
   - 0 silencedetect gaps > 0.55s at -35dB
   - Final 4s does not fade to premature black
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import cv2
import numpy as np
from PIL import Image, ImageDraw

STOPWORDS = {
    "the",
    "a",
    "an",
    "of",
    "for",
    "to",
    "in",
    "on",
    "and",
    "or",
    "is",
    "are",
    "was",
    "were",
    "with",
    "your",
    "you",
    "my",
    "i",
    "we",
    "they",
    "this",
    "that",
    "it",
    "how",
    "what",
    "why",
    "when",
    "who",
    "from",
    "by",
    "as",
    "at",
    "into",
    "about",
    "one",
    "times",
    "here",
    "just",
    "next",
}

BANNED_OPENERS = [
    r"\bhey guys\b",
    r"\bwelcome back\b",
    r"\bwelcome to\b",
    r"\bin today'?s video\b",
    r"\bbefore we (get started|begin|start)\b",
    r"\bmake sure to (like|subscribe)\b",
    r"\bdon'?t forget to subscribe\b",
]


def fmt_ts(sec: float) -> str:
    m, s = divmod(max(0.0, sec), 60.0)
    return f"{int(m):02d}:{s:05.2f}"


def content_tokens(text: str) -> set[str]:
    norm = re.sub(r"\bmr\.\s+beast\b", "mrbeast", text.lower())
    toks = re.findall(r"[a-zA-Zа-яА-ЯёЁ0-9$%]+", norm)
    return {t for t in toks if len(t) > 2 and t not in STOPWORDS}


def extract_frame(video_path: Path, t_sec: float, out_path: Path) -> bool:
    p = subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-loglevel",
            "error",
            "-ss",
            f"{max(0.0, t_sec):.2f}",
            "-i",
            str(video_path),
            "-frames:v",
            "1",
            "-q:v",
            "2",
            str(out_path),
        ],
        capture_output=True,
        check=False,
    )
    return p.returncode == 0 and out_path.exists()


def hsv_hist(img_bgr: np.ndarray) -> np.ndarray:
    hsv = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV)
    hist = cv2.calcHist([hsv], [0, 1], None, [24, 24], [0, 180, 0, 256])
    cv2.normalize(hist, hist)
    return hist


def spatial_grid_luma(img_bgr: np.ndarray) -> np.ndarray:
    gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
    small = cv2.resize(gray, (48, 27), interpolation=cv2.INTER_AREA).astype(np.float32)
    return small.flatten()


def cosine_sim(a: np.ndarray, b: np.ndarray) -> float:
    na = float(np.linalg.norm(a))
    nb = float(np.linalg.norm(b))
    if na == 0.0 or nb == 0.0:
        return 0.0
    return float(np.dot(a, b) / (na * nb))


def parse_transcript_opening(transcript_path: Path) -> Tuple[str, str]:
    raw = transcript_path.read_text(encoding="utf-8", errors="ignore")
    lines: List[str] = []
    first_5s_lines: List[str] = []
    for ln in raw.splitlines():
        s = ln.strip()
        if not s or s.startswith(("WEBVTT", "Kind:", "Language:", "#", "---", ">")):
            continue
        if re.match(r"^\d+$", s) or "-->" in s:
            continue
        m = re.match(r"^\[(\d{2}):(\d{2}):(\d{2})\]\s*(.+)$", s)
        if m:
            sec = int(m.group(1)) * 3600 + int(m.group(2)) * 60 + int(m.group(3))
            txt = m.group(4).strip()
            lines.append(txt)
            if sec <= 6:
                first_5s_lines.append(txt)
        else:
            clean = re.sub(r"\[[^\]]+\]", "", re.sub(r"<[^>]+>", "", s)).strip()
            if clean:
                lines.append(clean)
    full_head = " ".join(lines[:15])
    opening_5s = (
        " ".join(first_5s_lines) if first_5s_lines else " ".join(full_head.split()[:18])
    )
    return opening_5s, " ".join(lines[:35])


def ffprobe_duration(video_path: Path) -> Optional[float]:
    p = subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            str(video_path),
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    try:
        return float(p.stdout.strip())
    except ValueError:
        return None


def detect_cuts(
    video_path: Path,
    threshold: float = 0.12,
    min_gap: float = 0.35,
    start_sec: Optional[float] = None,
    max_sec: Optional[float] = None,
) -> List[float]:
    filters = []
    if start_sec is not None or max_sec is not None:
        s = f"start={start_sec}" if start_sec is not None else ""
        e = f"end={max_sec}" if max_sec is not None else ""
        args = ":".join(x for x in (s, e) if x)
        filters.append(f"trim={args},setpts=PTS-STARTPTS")
    filters.append(f"scale=320:180,select='gt(scene,{threshold})',showinfo")
    vf = ",".join(filters)
    p = subprocess.run(
        [
            "ffmpeg",
            "-i",
            str(video_path),
            "-vf",
            vf,
            "-vsync",
            "vfr",
            "-f",
            "null",
            "-",
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    offset = start_sec or 0.0
    times = [offset]
    for ln in p.stderr.splitlines():
        if "pts_time:" in ln:
            m = re.search(r"pts_time:([0-9.]+)", ln)
            if m:
                t = offset + float(m.group(1))
                if t - times[-1] >= min_gap:
                    times.append(t)
    return times


def build_sheet(items: List[Tuple[str, Path]], out_path: Path, cols: int = 4) -> None:
    if not items:
        return
    cw, ch = 480, 270
    rows = (len(items) + cols - 1) // cols
    canvas = Image.new("RGB", (cols * cw, rows * ch), (15, 15, 18))
    draw = ImageDraw.Draw(canvas)
    for idx, (lbl, fp) in enumerate(items):
        r, c = divmod(idx, cols)
        im = Image.open(fp).convert("RGB").resize((cw, ch), Image.Resampling.LANCZOS)
        canvas.paste(im, (c * cw, r * ch))
        draw.rectangle(
            [c * cw + 4, r * ch + 4, c * cw + 240, r * ch + 26], fill=(10, 10, 12)
        )
        draw.text((c * cw + 8, r * ch + 8), lbl, fill=(255, 220, 90))
    canvas.save(out_path, quality=90)


def audit_packaging(
    thumb_path: Optional[Path],
    title: Optional[str],
    thumb_text: Optional[str],
) -> Tuple[List[str], List[str], Dict[str, Any]]:
    errors: List[str] = []
    warnings: List[str] = []
    info: Dict[str, Any] = {}

    if title:
        t = title.strip()
        info["title_chars"] = len(t)
        if len(t) > 100:
            errors.append(f"Title exceeds YouTube 100-char hard cap ({len(t)} chars).")
        elif len(t) > 60:
            warnings.append(
                f"Title is {len(t)} chars (desktop truncates ~60 chars; mobile ~40 chars)."
            )
        caps = [w for w in t.split() if len(w) > 2 and w.isupper()]
        if len(caps) > 2:
            warnings.append(f"Title has {len(caps)} ALL-CAPS words (ceiling: 2).")

    if thumb_text:
        tw = thumb_text.strip().split()
        info["thumb_word_count"] = len(tw)
        if len(tw) > 4:
            warnings.append(
                f"Thumbnail overlay has {len(tw)} words (target 2-4 max for 120px readability)."
            )
        if title:
            overlap = content_tokens(title) & content_tokens(thumb_text)
            info["title_thumb_overlap"] = sorted(overlap)
            if len(overlap) > 0:
                errors.append(
                    f"Thumbnail text repeats title tokens {sorted(overlap)} — violates Title/Thumbnail Split Rule."
                )

    if thumb_path:
        if not thumb_path.exists():
            errors.append(f"Thumbnail file missing: {thumb_path}")
        else:
            im = Image.open(thumb_path).convert("RGB")
            w, h = im.size
            info["thumb_size"] = [w, h]
            if w < 1280 or h < 720:
                errors.append(f"Thumbnail resolution {w}x{h} below 1280x720 minimum.")
            mobile = im.resize(
                (120, int(120 * h / max(w, 1))), Image.Resampling.LANCZOS
            )
            arr = np.asarray(mobile, dtype=np.float32)
            luma = 0.299 * arr[:, :, 0] + 0.587 * arr[:, :, 1] + 0.114 * arr[:, :, 2]
            luma_std = float(np.std(luma))
            info["thumb_120px_luma_std"] = round(luma_std, 2)
            if luma_std < 42.0:
                errors.append(
                    f"Thumbnail fails 120px mobile pop test: luma_std={luma_std:.2f} (<42.0)."
                )
            # TV 50% Top-Half Test (KE4zqD0ONDI Rule 1)
            t_bgr = cv2.imread(str(thumb_path))
            if t_bgr is not None:
                t_gray = cv2.cvtColor(t_bgr, cv2.COLOR_BGR2GRAY)
                top50_std = float(np.std(t_gray[: h // 2, :].astype(np.float32)))
                edges = cv2.Canny(t_gray, 70, 170)
                te = float(np.sum(edges[: h // 2, :] > 0))
                be = float(np.sum(edges[h // 2 :, :] > 0))
                top50_edge = (te / (te + be)) if (te + be) > 0 else 0.5
                info["thumb_tv_top50_luma_std"] = round(top50_std, 2)
                info["thumb_tv_top50_edge_share"] = round(top50_edge, 3)
                if top50_std < 28.0 or top50_edge < 0.30:
                    errors.append(
                        f"Thumbnail fails TV 50% Top-Half Test (top50_luma_std={top50_std:.1f}, top50_edge_share={top50_edge:.2f}) — move hero/text higher!"
                    )
                elif top50_std < 36.0 or top50_edge < 0.40:
                    warnings.append(
                        f"Borderline TV 50% visibility (top50_luma_std={top50_std:.1f}, top50_edge_share={top50_edge:.2f})."
                    )
    return errors, warnings, info


def audit_transcript(
    transcript_path: Optional[Path],
    title: Optional[str],
) -> Tuple[List[str], List[str], Dict[str, Any]]:
    errors: List[str] = []
    warnings: List[str] = []
    info: Dict[str, Any] = {}
    if not transcript_path:
        return errors, warnings, info
    if not transcript_path.exists():
        return [f"Transcript/script not found: {transcript_path}"], warnings, info

    opening_5s, opening_20s = parse_transcript_opening(transcript_path)
    info["opening_5s_sample"] = opening_5s
    info["opening_20s_sample"] = opening_20s[:240]

    for pat in BANNED_OPENERS:
        if re.search(pat, opening_20s, re.I):
            errors.append(
                f"Banned greeting/filler detected in first 20s (`{pat}`). Start immediately on the title's promise!"
            )

    if title:
        t_toks = content_tokens(title)
        o_toks = content_tokens(opening_5s)
        overlap = t_toks & o_toks
        info["first_5s_title_overlap"] = sorted(overlap)
        if t_toks and not overlap:
            o20_toks = content_tokens(opening_20s)
            if t_toks & o20_toks:
                warnings.append(
                    f"Title words ({sorted(t_toks & o20_toks)}) appear after 5s instead of inside the very first sentence (0-5s Expectation Match)."
                )
            else:
                errors.append(
                    f"First 5s spoken text misses Title terms ({sorted(t_toks)}). First sentence MUST match the Title."
                )

    return errors, warnings, info


def audit_video(
    video_path: Path,
    thumb_path: Optional[Path],
    out_dir: Optional[Path],
    is_short: bool = False,
) -> Tuple[List[str], List[str], Dict[str, Any]]:
    errors: List[str] = []
    warnings: List[str] = []
    info: Dict[str, Any] = {}

    if not video_path.exists():
        return [f"Video file missing: {video_path}"], warnings, info

    duration = ffprobe_duration(video_path)
    if duration is None or duration <= 0:
        return [f"Could not read duration for {video_path}"], warnings, info
    info["duration_sec"] = round(duration, 2)

    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        # 1. Hook frames + _retention_hook_sheet.jpg
        hook_times = [0.5, 2.0, 4.5, 8.0, 12.0, 16.0, 19.5]
        extracted: List[Tuple[str, Path]] = []
        if thumb_path and thumb_path.exists():
            extracted.append(("THUMBNAIL", thumb_path))
        for ht in hook_times:
            if ht < duration:
                fp = tmp / f"h_{ht:.1f}.jpg"
                if extract_frame(video_path, ht, fp):
                    extracted.append((f"{ht:.1f}s", fp))

        if thumb_path and thumb_path.exists():
            t_bgr = cv2.imread(str(thumb_path))
            t_hist = hsv_hist(t_bgr)
            best_corr = -1.0
            best_t = None
            for lbl, fp in extracted:
                if lbl in ("0.5s", "2.0s", "4.5s"):
                    f_bgr = cv2.imread(str(fp))
                    corr = float(
                        cv2.compareHist(t_hist, hsv_hist(f_bgr), cv2.HISTCMP_CORREL)
                    )
                    if corr > best_corr:
                        best_corr = corr
                        best_t = lbl
            info["thumb_vs_opening_hsv_corr"] = round(best_corr, 3)
            info["thumb_best_match_frame"] = best_t
            if best_corr < 0.12:
                warnings.append(
                    f"Low Thumbnail-to-Opening (0-5s) visual color/tone match (HSV corr={best_corr:.2f}). Confirm Frame 1 mirrors Thumbnail visually."
                )

        if out_dir is not None and extracted:
            out_dir.mkdir(parents=True, exist_ok=True)
            sheet_p = out_dir / "_retention_hook_sheet.jpg"
            build_sheet(extracted, sheet_p, cols=4)
            info["hook_sheet_path"] = str(sheet_p)

        # 2. Hook 0-20s Dynamic Cadence
        hook_end_sec = min(20.0, duration)
        hook_pts = detect_cuts(
            video_path, threshold=0.08, min_gap=0.45, max_sec=hook_end_sec
        )
        if hook_end_sec - hook_pts[-1] > 0.3:
            hook_pts.append(hook_end_sec)
        hook_beats = [hook_pts[i + 1] - hook_pts[i] for i in range(len(hook_pts) - 1)]
        hook_changes = len(hook_beats)
        hook_max_hold = max(hook_beats) if hook_beats else hook_end_sec
        info["hook_0_20s_visual_changes"] = hook_changes
        info["hook_0_20s_max_hold_sec"] = round(hook_max_hold, 2)

        if duration >= 20.0:
            if hook_changes < 5:
                errors.append(
                    f"Hook (0-20s) has only {hook_changes} visual shifts (MrBeast target: 8+ dynamic shots in 20s; hard min: 5)."
                )
            elif hook_changes < 7:
                warnings.append(
                    f"Hook (0-20s) has {hook_changes} visual shifts (target 8+ dynamic shots in first 20s)."
                )
            if hook_max_hold > 5.5:
                errors.append(
                    f"Hook (0-20s) holds one frame for {hook_max_hold:.2f}s (max 5.5s; steepest drop-off happens in first 20s!)."
                )
            elif hook_max_hold > 4.0:
                warnings.append(
                    f"Hook (0-20s) max single hold is {hook_max_hold:.2f}s (target <=3.5s)."
                )

        # 3. Full-video cut cadence & static span inspection
        pts = detect_cuts(video_path, threshold=0.12, min_gap=0.35)
        if duration - pts[-1] > 0.25:
            pts.append(duration)
        beat_spans = [
            (pts[i + 1] - pts[i], pts[i], pts[i + 1]) for i in range(len(pts) - 1)
        ]
        beats = [b[0] for b in beat_spans]
        median_beat = float(np.median(beats)) if beats else duration
        max_beat = float(np.max(beats)) if beats else duration
        target_median = 2.5 if is_short else 3.2
        info["total_cuts"] = len(beats)
        info["median_beat_sec"] = round(median_beat, 2)
        info["max_beat_sec"] = round(max_beat, 2)

        top_spans = sorted(beat_spans, reverse=True)[:5]
        span_reports = []
        truly_static_ge_10 = []
        for dur_s, s_t, e_t in top_spans:
            # Check micro-activity (0.04) inside spans >= 10s so animated charts on white canvas are distinguished from dead freezes
            sub_cuts = 0
            if dur_s >= 9.5:
                sc = detect_cuts(
                    video_path, threshold=0.04, min_gap=0.5, start_sec=s_t, max_sec=e_t
                )
                sub_cuts = max(0, len(sc) - 1)
                if dur_s >= 10.0 and (sub_cuts == 0 or dur_s > 14.0):
                    truly_static_ge_10.append((dur_s, s_t, e_t, sub_cuts))
            span_reports.append(
                {
                    "span": f"{fmt_ts(s_t)}-{fmt_ts(e_t)}",
                    "duration_sec": round(dur_s, 2),
                    "micro_motion_events": sub_cuts,
                }
            )
        info["longest_spans"] = span_reports

        if median_beat > target_median:
            errors.append(
                f"Median visual beat ({median_beat:.2f}s) exceeds target ({target_median:.2f}s)."
            )
        if is_short and max_beat > 4.5:
            errors.append(f"Static stretch {max_beat:.2f}s in Short (max 4.5s).")
        elif not is_short:
            if truly_static_ge_10:
                worst = truly_static_ge_10[0]
                errors.append(
                    f"Static/low-contrast stretch {worst[0]:.2f}s at {fmt_ts(worst[1])}-{fmt_ts(worst[2])} (micro_motion={worst[3]}; >=10s risks viewer drop-off)."
                )
            elif max_beat > 6.0:
                warnings.append(
                    f"Longest single-cut hold is {max_beat:.2f}s at {span_reports[0]['span']} (aim <=5.0s for consistent visual variety)."
                )

        # Anti-Same-Room stagnation check across up to 36 interior cuts
        cut_boundaries = [t for t in pts[1:-1] if 1.0 < t < duration - 1.0]
        if len(cut_boundaries) >= 6:
            step = max(1, len(cut_boundaries) // 36)
            sampled = cut_boundaries[::step][:36]
            same_room_count = 0
            checked = 0
            for ct in sampled:
                f_pre = tmp / f"pre_{ct:.2f}.jpg"
                f_post = tmp / f"post_{ct:.2f}.jpg"
                if extract_frame(video_path, ct - 0.35, f_pre) and extract_frame(
                    video_path, ct + 0.35, f_post
                ):
                    b1 = cv2.imread(str(f_pre))
                    b2 = cv2.imread(str(f_post))
                    c_hsv = float(
                        cv2.compareHist(hsv_hist(b1), hsv_hist(b2), cv2.HISTCMP_CORREL)
                    )
                    c_sp = cosine_sim(spatial_grid_luma(b1), spatial_grid_luma(b2))
                    checked += 1
                    if c_hsv > 0.93 and c_sp > 0.96:
                        same_room_count += 1
            if checked:
                ratio = same_room_count / checked
                info["same_room_low_contrast_cut_ratio"] = round(ratio, 3)
                if ratio > 0.45:
                    warnings.append(
                        f"{same_room_count}/{checked} ({ratio * 100:.0f}%) sampled cuts share nearly identical backdrop/luminance (risk of boring same-room/same-template cuts without continuous contrast)."
                    )

        # Body sample contact sheet
        if out_dir is not None and duration >= 30.0:
            body_marks = [
                (duration * 0.25, "25%"),
                (duration * 0.45, "45%"),
                (duration * 0.65, "65%"),
                (duration * 0.80, "80% (final 20%)"),
                (duration * 0.92, "92% climax"),
                (max(0.0, duration - 2.0), "End -2s"),
            ]
            if top_spans:
                (
                    ls_dur,
                    ls_s,
                    ls_e,
                ) = top_spans[0]
                body_marks.append(((ls_s + ls_e) / 2.0, f"Longest {ls_dur:.1f}s"))
            body_items: List[Tuple[str, Path]] = []
            for idx, (mt, lbl) in enumerate(body_marks):
                bp = tmp / f"b_{idx}.jpg"
                if extract_frame(video_path, mt, bp):
                    body_items.append((f"{lbl} ({fmt_ts(mt)})", bp))
            body_p = out_dir / "_retention_body_sheet.jpg"
            build_sheet(body_items, body_p, cols=4)
            info["body_sheet_path"] = str(body_p)

        # 4. Energy Cycling / Middle-Valley Check across Quartiles Q1..Q4
        if duration >= 120.0:
            q_cpm: Dict[str, float] = {}
            q_len = duration / 4.0
            for qi in range(4):
                qs, qe = qi * q_len, (qi + 1) * q_len
                cnt = sum(1 for t in pts[1:-1] if qs <= t < qe)
                q_cpm[f"Q{qi + 1}"] = round(cnt / (q_len / 60.0), 1)
            info["quartile_cuts_per_min"] = q_cpm
            if q_cpm["Q1"] > 0 and min(q_cpm["Q2"], q_cpm["Q3"]) < 0.50 * q_cpm["Q1"]:
                warnings.append(
                    f"Middle-valley pacing slump detected (Q1={q_cpm['Q1']} CPM vs Q2={q_cpm['Q2']}, Q3={q_cpm['Q3']}). Inject 2-4 min High-Energy resets."
                )

        # 5. Dead Air (>0.55s at -35dB) & Final 4s premature black fade check
        sil = subprocess.run(
            [
                "ffmpeg",
                "-i",
                str(video_path),
                "-af",
                "silencedetect=noise=-35dB:d=0.55",
                "-f",
                "null",
                "-",
            ],
            capture_output=True,
            text=True,
            check=False,
        )
        sil_durs = [
            float(m.group(1))
            for ln in sil.stderr.splitlines()
            if (m := re.search(r"silence_duration:\s*([0-9.]+)", ln))
        ]
        info["dead_air_gaps_gt_0_55s"] = len(sil_durs)
        if sil_durs:
            errors.append(
                f"Detected {len(sil_durs)} dead-air gaps >0.55s (max={max(sil_durs):.2f}s)."
            )

        end_f = tmp / "end_check.jpg"
        if duration > 4.0 and extract_frame(video_path, duration - 2.0, end_f):
            end_luma = float(
                np.mean(cv2.cvtColor(cv2.imread(str(end_f)), cv2.COLOR_BGR2GRAY))
            )
            info["end_minus_2s_luma"] = round(end_luma, 1)
            if end_luma < 8.0:
                warnings.append(
                    f"Video goes dark early at {duration - 2.0:.1f}s (luma={end_luma:.1f}) — avoid premature ending drop-offs!"
                )

    return errors, warnings, info


def audit_edl(edl_path: Optional[Path]) -> Tuple[List[str], List[str], Dict[str, Any]]:
    """Pre-render storyboard/EDL audit (checks 0-20s shot count, duration bounds, anti-same-room, quartile pace)."""
    errors: List[str] = []
    warnings: List[str] = []
    info: Dict[str, Any] = {}
    if not edl_path:
        return errors, warnings, info
    if not edl_path.exists():
        return [f"EDL file not found: {edl_path}"], warnings, info

    raw = json.loads(edl_path.read_text(encoding="utf-8"))
    shots: List[Dict[str, Any]] = []
    if "shots" in raw and isinstance(raw["shots"], list):
        shots = raw["shots"]
    elif "acts" in raw and isinstance(raw["acts"], dict):
        t_offset = 0.0
        for act_key in sorted(raw["acts"].keys()):
            act_shots = raw["acts"][act_key].get("shots", [])
            for sh in act_shots:
                copy_sh = dict(sh)
                if "global_start_s" not in copy_sh:
                    copy_sh["global_start_s"] = t_offset + float(sh.get("start_s", 0.0))
                shots.append(copy_sh)
            if act_shots:
                t_offset += max(float(s.get("end_s", 0.0)) for s in act_shots)

    if not shots:
        return [f"No shots found in EDL: {edl_path}"], warnings, info

    durs = [
        float(s.get("duration_s", s.get("end_s", 0) - s.get("start_s", 0)))
        for s in shots
    ]
    info["planned_shots"] = len(shots)
    info["planned_median_sec"] = round(float(np.median(durs)), 2)
    info["planned_max_sec"] = round(float(np.max(durs)), 2)

    # First 20s planned shots
    hook_shots = [
        s
        for s in shots
        if float(s.get("global_start_s", s.get("start_s", 999.0))) < 20.0
    ]
    info["planned_hook_0_20s_shots"] = len(hook_shots)
    if len(hook_shots) < 6:
        errors.append(
            f"Pre-EDL Hook (0-20s) plans only {len(hook_shots)} shots (target >=8 dynamic shifts in first 20s)."
        )
    elif len(hook_shots) < 8:
        warnings.append(
            f"Pre-EDL Hook (0-20s) plans {len(hook_shots)} shots (MrBeast target: 8+ shots in 20s)."
        )

    long_shots = [
        (s.get("shot_id", idx + 1), d)
        for idx, (s, d) in enumerate(zip(shots, durs))
        if d >= 10.0
    ]
    if long_shots:
        errors.append(
            f"Pre-EDL has {len(long_shots)} shot(s) >=10.0s (first: {long_shots[0]}). Break into <=3.5-5s context cuts!"
        )
    elif info["planned_median_sec"] > 3.5:
        warnings.append(
            f"Pre-EDL planned median shot is {info['planned_median_sec']}s (target 2.4-3.2s)."
        )

    # Back-to-back same asset / same room check
    repeats = []
    for i in range(1, len(shots)):
        a_prev = (
            shots[i - 1].get("type"),
            shots[i - 1].get("asset"),
            shots[i - 1].get("room"),
        )
        a_cur = (shots[i].get("type"), shots[i].get("asset"), shots[i].get("room"))
        if a_prev == a_cur and (a_cur[1] is not None or a_cur[2] is not None):
            repeats.append(shots[i].get("shot_id", i + 1))
    info["adjacent_same_asset_or_room"] = repeats
    if repeats:
        errors.append(
            f"Pre-EDL has adjacent identical asset/room repeats at {repeats[:5]} — violates Anti-Same-Room / Visual Variety rule."
        )

    return errors, warnings, info


def audit_pre_script_structure(
    transcript_path: Optional[Path],
) -> Tuple[List[str], List[str], Dict[str, Any]]:
    """Pre-render checks on full script markdown: <=20s body launch, Input Bias, [ON SCREEN] cadence, no farewell cliff."""
    errors: List[str] = []
    warnings: List[str] = []
    info: Dict[str, Any] = {}
    if not transcript_path or not transcript_path.exists():
        return errors, warnings, info

    raw = transcript_path.read_text(encoding="utf-8", errors="ignore")
    # Only run structural script checks if it looks like a script/pre-script (contains stage/screen cues or Act/Body headers)
    if not re.search(r"(\[ON SCREEN:|##\s*(?:Act|Body|Hook)|0:20|00:20)", raw, re.I):
        return errors, warnings, info

    # Check where Body / Act 1 starts relative to hook words
    m_body = re.search(
        r"(?:^|\n)(?:#+\s*(?:Body|Act\s*(?:1|I)\b|Point\s*1\b)|\[(?:BODY|ACT\s*1)\b|0:1[2-9]|0:20)",
        raw,
        re.I,
    )
    if m_body:
        hook_block = raw[: m_body.start()]
        spoken_only = re.sub(r"\[[^\]]+\]", " ", hook_block)
        spoken_only = re.sub(r"^#.*$", " ", spoken_only, flags=re.M)
        hook_words = len(re.findall(r"[a-zA-Zа-яА-ЯёЁ0-9$%'-]+", spoken_only))
        est_sec = round(hook_words / 2.55, 1)
        hook_visuals = len(
            re.findall(
                r"\[(?:ON SCREEN|VISUAL|SHOT|CUT|AI VIDEO)\s*:", hook_block, re.I
            )
        )
        info["pre_script_hook_words"] = hook_words
        info["pre_script_hook_est_sec"] = est_sec
        info["pre_script_hook_visual_cues"] = hook_visuals
        if est_sec > 20.5:
            errors.append(
                f"Pre-script Hook before Body/Act 1 is ~{est_sec}s ({hook_words} words > ~52 words) — MUST launch Body <= 0:20!"
            )
        if hook_visuals and hook_visuals < 6:
            warnings.append(
                f"Pre-script Hook has only {hook_visuals} [ON SCREEN/SHOT] cues (target 8+ dynamic shifts in 0-20s)."
            )

    tail = " ".join(raw.splitlines()[-15:]).lower()
    if re.search(
        r"(thanks for watching|thank you for watching|bye guys|see you next time|that'?s all for today)",
        tail,
    ):
        warnings.append(
            "Pre-script ending contains classic farewell phrase ('thanks for watching / see you next time') — replace with High-Note Payoff + urgent next-video bridge."
        )

    return errors, warnings, info


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Audit video, packaging, pre-script & EDL BEFORE and AFTER against 5zu8s38ZwtQ + KE4zqD0ONDI."
    )
    ap.add_argument("--video", type=Path, help="Rendered MP4 path (POST-render)")
    ap.add_argument(
        "--edl", type=Path, help="Planned EDL/storyboard JSON path (PRE-render)"
    )
    ap.add_argument("--thumb", type=Path, help="Thumbnail PNG/JPG path")
    ap.add_argument("--title", type=str, help="Exact YouTube title")
    ap.add_argument("--thumb-text", type=str, help="Exact overlay words on thumbnail")
    ap.add_argument(
        "--transcript",
        type=Path,
        help="Script, pre-script markdown, SRT, VTT, or timestamped transcript",
    )
    ap.add_argument(
        "--out-dir", type=Path, help="Directory to save contact sheets & report JSON"
    )
    ap.add_argument("--short", action="store_true", help="Short-form mode (<60s)")
    ap.add_argument("--json", action="store_true", help="Print JSON output only")
    args = ap.parse_args()

    all_errors: List[str] = []
    all_warnings: List[str] = []
    report: Dict[str, Any] = {}

    e, w, i = audit_packaging(args.thumb, args.title, args.thumb_text)
    all_errors.extend(e)
    all_warnings.extend(w)
    report["packaging"] = i

    e, w, i = audit_transcript(args.transcript, args.title)
    all_errors.extend(e)
    all_warnings.extend(w)
    e2, w2, i2 = audit_pre_script_structure(args.transcript)
    all_errors.extend(e2)
    all_warnings.extend(w2)
    i.update(i2)
    report["transcript"] = i

    if args.edl:
        e, w, i = audit_edl(args.edl)
        all_errors.extend(e)
        all_warnings.extend(w)
        report["pre_edl"] = i

    if args.video:
        e, w, i = audit_video(args.video, args.thumb, args.out_dir, is_short=args.short)
        all_errors.extend(e)
        all_warnings.extend(w)
        report["video"] = i

    report["errors"] = all_errors
    report["warnings"] = all_warnings
    report["status"] = "PASSED" if not all_errors else "FAILED"

    if args.out_dir:
        args.out_dir.mkdir(parents=True, exist_ok=True)
        (args.out_dir / "retention_audit_report.json").write_text(
            json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8"
        )

    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        print("=== RETENTION ARCHITECTURE REPORT ===")
        print(json.dumps(report, indent=2, ensure_ascii=False))
        print(
            "STATUS:",
            "RETENTION_ARCHITECTURE_PASSED"
            if not all_errors
            else "RETENTION_ARCHITECTURE_FAILED",
        )

    return 0 if not all_errors else 1


if __name__ == "__main__":
    sys.exit(main())
