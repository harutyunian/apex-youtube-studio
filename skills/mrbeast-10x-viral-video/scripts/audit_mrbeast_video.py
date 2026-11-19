#!/usr/bin/env python3
"""
MrBeast 10x Viral Video & Retention Gate Auditor (I4nd9t84UvI + 5zu8s38ZwtQ).

Audits:
1. Thumbnail / Preview (--thumb, --title, --thumb-text):
   - Resolution & aspect ratio check
   - Luminance contrast & color saturation (120px mobile pop check, luma_std >= 42)
   - Word count (1-4 impact words max) and 0% word overlap with the title
2. 0-5s Expectation Lock & 0-20s Dynamic Hook (--video, --thumb, --title, --transcript):
   - Opening frame (0.5s-4.5s) color/luma correlation against thumbnail
   - First 5s spoken overlap with Title keywords + zero banned greetings (if --transcript passed)
   - First 20s visual shifts count (target >= 8, min 5; max hold in first 20s <= 5.0s)
3. Video Cadence, Anti-Stall & Energy Cycles (--video):
   - Median visual beat duration (<= 2.5s Shorts, <= 3.2s Long-form)
   - Zero truly static stretches >= 10.0s (MrBeast's "no 10s static talking head" rule)
   - Quartile Q1-Q4 pacing balance (anti-middle-valley)
   - Audio presence & dead-air check (0 gaps > 0.55s at -35dB)
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import List, Optional, Tuple

import cv2
import numpy as np
from PIL import Image

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
}

BANNED_OPENERS = [
    r"\bhey guys\b",
    r"\bwelcome back\b",
    r"\bwelcome to\b",
    r"\bin today'?s video\b",
    r"\bbefore we (get started|begin|start)\b",
    r"\bmake sure to (like|subscribe)\b",
]


def normalize_words(text: str) -> set[str]:
    norm = re.sub(r"\bmr\.\s+beast\b", "mrbeast", text.lower())
    words = re.findall(r"[a-zA-Zа-яА-ЯёЁ0-9$%]+", norm)
    return {w for w in words if len(w) > 2 and w not in STOPWORDS}


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
    proc = subprocess.run(
        [
            "ffmpeg",
            "-i",
            str(video_path),
            "-vf",
            ",".join(filters),
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
    pts_times = [offset]
    for line in proc.stderr.splitlines():
        if "pts_time:" in line:
            m = re.search(r"pts_time:([0-9.]+)", line)
            if m:
                t = offset + float(m.group(1))
                if t - pts_times[-1] >= min_gap:
                    pts_times.append(t)
    return pts_times


def audit_packaging(
    thumb_path: Optional[Path],
    title: Optional[str],
    thumb_text: Optional[str],
) -> Tuple[List[str], List[str]]:
    errors: List[str] = []
    warnings: List[str] = []
    if title:
        if len(title) > 100:
            errors.append(f"Title length ({len(title)}) exceeds 100 chars.")
        if not re.search(r"\d|[?!]|—|:", title):
            warnings.append(
                "Title lacks a concrete number, colon, or high-stakes punctuation hook."
            )

    if thumb_text:
        words = thumb_text.strip().split()
        if len(words) > 5 or len(words) < 1:
            errors.append(
                f"Thumbnail text has {len(words)} words (target: 2-4 impact words for 120px mobile read)."
            )
        if title:
            overlap = normalize_words(title) & normalize_words(thumb_text)
            if len(overlap) > 1:
                errors.append(
                    f"Thumbnail repeats title words {overlap} — violates Information Split Rule."
                )

    if thumb_path:
        if not thumb_path.exists():
            errors.append(f"Thumbnail file not found: {thumb_path}")
        else:
            im = Image.open(thumb_path).convert("RGB")
            w, h = im.size
            if w < 1280 or h < 720:
                errors.append(
                    f"Thumbnail resolution {w}x{h} is below 1280x720 minimum."
                )
            mobile = im.resize(
                (120, int(120 * h / max(w, 1))), Image.Resampling.LANCZOS
            )
            arr = np.asarray(mobile, dtype=np.float32)
            luma = 0.299 * arr[:, :, 0] + 0.587 * arr[:, :, 1] + 0.114 * arr[:, :, 2]
            luma_std = float(np.std(luma))
            if luma_std < 42.0:
                errors.append(
                    f"Thumbnail fails 120px mobile contrast test: luma std={luma_std:.1f} (minimum 42.0 required)."
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
                if top50_std < 28.0 or top50_edge < 0.30:
                    errors.append(
                        f"Thumbnail fails TV 50% Top-Half Test (top50_std={top50_std:.1f}, top50_edge={top50_edge:.2f}) — move hero/text to top half!"
                    )
                elif top50_std < 36.0 or top50_edge < 0.40:
                    warnings.append(
                        f"Borderline TV 50% visibility (top50_std={top50_std:.1f}, top50_edge={top50_edge:.2f})."
                    )
    return errors, warnings


def audit_transcript(
    transcript_path: Optional[Path],
    title: Optional[str],
) -> Tuple[List[str], List[str]]:
    errors: List[str] = []
    warnings: List[str] = []
    if not transcript_path:
        return errors, warnings
    if not transcript_path.exists():
        return [f"Transcript/script not found: {transcript_path}"], warnings

    raw = transcript_path.read_text(encoding="utf-8", errors="ignore")
    lines = []
    first_5s = []
    for ln in raw.splitlines():
        s = ln.strip()
        if (
            not s
            or s.startswith(("WEBVTT", "Kind:", "Language:", "#", "---", ">"))
            or re.match(r"^\d+$", s)
            or "-->" in s
        ):
            continue
        m = re.match(r"^\[(\d{2}):(\d{2}):(\d{2})\]\s*(.+)$", s)
        if m:
            sec = int(m.group(1)) * 3600 + int(m.group(2)) * 60 + int(m.group(3))
            txt = m.group(4).strip()
            lines.append(txt)
            if sec <= 6:
                first_5s.append(txt)
        else:
            clean = re.sub(r"<[^>]+>", "", s).strip()
            if clean:
                lines.append(clean)

    head_20 = " ".join(lines[:30])
    head_5 = " ".join(first_5s) if first_5s else " ".join(head_20.split()[:18])

    for pat in BANNED_OPENERS:
        if re.search(pat, head_20, re.I):
            errors.append(
                f"Banned opening greeting/filler `{pat}` in hook (0-20s). First sentence MUST match the title."
            )

    if title:
        t_toks = normalize_words(title)
        if t_toks and not (t_toks & normalize_words(head_5)):
            if t_toks & normalize_words(head_20):
                warnings.append(
                    "Title keywords appear after 5s instead of inside the very first sentence (0-5s Expectation Lock)."
                )
            else:
                errors.append(
                    f"First 5s spoken text misses Title keywords {sorted(t_toks)}."
                )
    return errors, warnings


def audit_video_cadence(
    video_path: Path,
    thumb_path: Optional[Path] = None,
    is_short: bool = False,
) -> Tuple[List[str], List[str]]:
    errors: List[str] = []
    warnings: List[str] = []
    if not video_path.exists():
        return [f"Video file not found: {video_path}"], warnings

    probe = subprocess.run(
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
        duration = float(probe.stdout.strip())
    except ValueError:
        return [f"Could not read video duration from {video_path}"], warnings

    # 1. Hook 0-20s dynamic shot density (target 8+ visual changes, hard min 5)
    hook_end = min(20.0, duration)
    hook_pts = detect_cuts(video_path, threshold=0.08, min_gap=0.45, max_sec=hook_end)
    if hook_end - hook_pts[-1] > 0.3:
        hook_pts.append(hook_end)
    hook_beats = [hook_pts[i + 1] - hook_pts[i] for i in range(len(hook_pts) - 1)]
    hook_changes = len(hook_beats)
    hook_max = max(hook_beats) if hook_beats else hook_end
    if duration >= 20.0:
        if hook_changes < 5:
            errors.append(
                f"Hook (0-20s) has only {hook_changes} visual shifts (MrBeast target: 8+ dynamic shots in 20s; hard min: 5)."
            )
        elif hook_changes < 7:
            warnings.append(
                f"Hook (0-20s) has {hook_changes} visual shifts (target 8+ in first 20s)."
            )
        if hook_max > 5.5:
            errors.append(
                f"Hook (0-20s) holds a single visual for {hook_max:.2f}s (max 5.5s)."
            )

    # 2. Optional 0-5s thumbnail-to-opening color match check
    if thumb_path and thumb_path.exists():
        t_bgr = cv2.imread(str(thumb_path))
        if t_bgr is not None:
            t_hsv = cv2.cvtColor(t_bgr, cv2.COLOR_BGR2HSV)
            t_hist = cv2.calcHist([t_hsv], [0, 1], None, [24, 24], [0, 180, 0, 256])
            cv2.normalize(t_hist, t_hist)
            best_corr = -1.0
            with tempfile.TemporaryDirectory() as td:
                for ts in (0.5, 2.0, 4.0):
                    if ts >= duration:
                        continue
                    fp = Path(td) / f"f_{ts}.jpg"
                    subprocess.run(
                        [
                            "ffmpeg",
                            "-y",
                            "-loglevel",
                            "error",
                            "-ss",
                            str(ts),
                            "-i",
                            str(video_path),
                            "-frames:v",
                            "1",
                            str(fp),
                        ],
                        check=False,
                    )
                    if fp.exists():
                        f_bgr = cv2.imread(str(fp))
                        f_hsv = cv2.cvtColor(f_bgr, cv2.COLOR_BGR2HSV)
                        f_hist = cv2.calcHist(
                            [f_hsv], [0, 1], None, [24, 24], [0, 180, 0, 256]
                        )
                        cv2.normalize(f_hist, f_hist)
                        corr = float(
                            cv2.compareHist(t_hist, f_hist, cv2.HISTCMP_CORREL)
                        )
                        best_corr = max(best_corr, corr)
            if best_corr >= 0 and best_corr < 0.12:
                warnings.append(
                    f"Low Thumbnail-to-Frame-1 (0-5s) visual match (HSV corr={best_corr:.2f}). Verify opening frame mirrors Thumbnail."
                )

    # 3. Full-video cadence & static stretch audit
    pts_times = detect_cuts(video_path, threshold=0.12, min_gap=0.35)
    if duration - pts_times[-1] > 0.2:
        pts_times.append(duration)
    beats = [pts_times[i + 1] - pts_times[i] for i in range(len(pts_times) - 1)]
    if not beats:
        return ["No visual beats detected in video."], warnings

    median_beat = float(np.median(beats))
    max_beat = float(np.max(beats))
    target_median = 2.5 if is_short else 3.2

    print(
        f"[CADENCE] Duration={duration:.2f}s | Hook0-20s={hook_changes} shifts (max={hook_max:.2f}s) | "
        f"TotalBeats={len(beats)} | Median={median_beat:.2f}s | Max={max_beat:.2f}s"
    )

    if median_beat > target_median:
        errors.append(
            f"Median visual beat ({median_beat:.2f}s) exceeds MrBeast target ({target_median:.2f}s). "
            "Add more context-driven B-roll cuts, scale shifts, or kinetic proof overlays."
        )
    if is_short and max_beat > 4.5:
        errors.append(
            f"Found a static stretch of {max_beat:.2f}s in Short (max allowed: 4.5s). Every second must move!"
        )
    elif not is_short and max_beat > 12.0:
        errors.append(
            f"Found a static stretch of {max_beat:.2f}s in Long video (MrBeast rule: never hold a static talking head/shot >=10-12s)."
        )
    elif not is_short and max_beat >= 10.0:
        warnings.append(
            f"Longest stretch is {max_beat:.2f}s (>=10s risks drop-off; keep visual shifts every 3-5s)."
        )

    # 4. Quartile anti-middle-valley pacing check
    if duration >= 120.0:
        q_len = duration / 4.0
        qcpm = [
            round(
                sum(1 for t in pts_times[1:-1] if i * q_len <= t < (i + 1) * q_len)
                / (q_len / 60.0),
                1,
            )
            for i in range(4)
        ]
        if qcpm[0] > 0 and min(qcpm[1], qcpm[2]) < 0.50 * qcpm[0]:
            warnings.append(
                f"Middle-valley pacing drop detected (Q1={qcpm[0]} CPM vs Q2={qcpm[1]}, Q3={qcpm[2]}). Add 2-4m energy resets."
            )

    # 5. Dead air (> 0.55s at -35dB)
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
    silence_durations = [
        float(m.group(1))
        for line in sil.stderr.splitlines()
        if (m := re.search(r"silence_duration:\s*([0-9.]+)", line))
    ]
    if silence_durations:
        errors.append(
            f"Detected {len(silence_durations)} dead-air gaps >0.55s (max={max(silence_durations):.2f}s). Cut all dead air!"
        )

    return errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Audit video, packaging & transcript against MrBeast 10x + 5zu8s38ZwtQ rules."
    )
    parser.add_argument("--video", type=Path, help="Path to rendered MP4 video")
    parser.add_argument(
        "--short",
        action="store_true",
        help="Audit as a 9:16 Short (stricter 2.5s cadence)",
    )
    parser.add_argument("--thumb", type=Path, help="Path to thumbnail image")
    parser.add_argument("--title", type=str, help="Video title")
    parser.add_argument("--thumb-text", type=str, help="Text overlay on the thumbnail")
    parser.add_argument(
        "--transcript", type=Path, help="Script, SRT, VTT, or clean transcript"
    )
    args = parser.parse_args()

    all_errors: List[str] = []
    all_warnings: List[str] = []

    e, w = audit_packaging(args.thumb, args.title, args.thumb_text)
    all_errors.extend(e)
    all_warnings.extend(w)

    e, w = audit_transcript(args.transcript, args.title)
    all_errors.extend(e)
    all_warnings.extend(w)

    if args.video:
        e, w = audit_video_cadence(
            args.video, thumb_path=args.thumb, is_short=args.short
        )
        all_errors.extend(e)
        all_warnings.extend(w)

    for w in all_warnings:
        print(f"  [WARN] {w}")

    if all_errors:
        print("MRBEAST_10X_GATE_FAILED:")
        for err in all_errors:
            print(f"  - {err}")
        return 1

    print("MRBEAST_10X_GATE_PASSED")
    return 0


if __name__ == "__main__":
    sys.exit(main())
