#!/usr/bin/env python3
"""
Thumbnail Packaging & TV-50% / Mobile-120px Diagnostic Auditor (KE4zqD0ONDI + I4nd9t84UvI).

Supports BOTH BEFORE (Pre-Generation Brief/Prompt Gate) AND AFTER (Post-Generation Pixel Gate):
  - PRE (--brief): Verifies Psychology Lock (Questions + Emotions), 5-Source Reference Mechanism,
    TV 50% Top-Half layout plan, Clutter Removal, Obvious Hero isolation, and 3+ A/B text variants
    with 0% Title word overlap BEFORE spending credits on image generation.
  - POST (--thumb): Verifies >=1280x720, 120px Mobile Pop (luma_std >= 42.0), TV 50% Top-Half Test
    (tv_top50_luma_std >= 28.0, tv_top50_edge_share >= 0.30), edge clutter, 0% Title word overlap,
    and generates 4-panel `_thumbnail_diagnostic_sheet.jpg`.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

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
}


def content_tokens(text: str) -> set[str]:
    norm = re.sub(r"\bmr\.\s+beast\b", "mrbeast", text.lower())
    toks = re.findall(r"[a-zA-Zа-яА-ЯёЁ0-9$%]+", norm)
    return {t for t in toks if len(t) > 2 and t not in STOPWORDS}


def inspect_brief(
    brief_path: Path,
    title: Optional[str] = None,
    ab_texts: Optional[List[str]] = None,
) -> Dict[str, Any]:
    errors: List[str] = []
    warnings: List[str] = []
    metrics: Dict[str, Any] = {}

    if not brief_path.exists():
        return {
            "status": "FAILED",
            "errors": [f"Brief file not found: {brief_path}"],
            "warnings": [],
            "metrics": {},
        }

    raw = brief_path.read_text(encoding="utf-8", errors="ignore")
    low = raw.lower()

    has_question = bool(re.search(r"(question|wonder|\?)", low))
    has_emotion = bool(
        re.search(
            r"(emotion|feel|feeling|awe|dread|shock|vulnerab|credib|curios|urgency|tension|pride)",
            low,
        )
    )
    has_reference = bool(
        re.search(
            r"(reference|mechanism|outlier|model 3|bookmark|off-platform|frameset)", low
        )
    )
    has_tv50 = bool(re.search(r"(tv|50%|top[- ]half|top[- ]third|upper half)", low))
    has_clutter = bool(
        re.search(r"(clutter|clean|strip|remove|minimal|negative space)", low)
    )
    has_hero = bool(
        re.search(
            r"(main character|obvious|hero|focal|isolat|rim light|contrast|crop)", low
        )
    )

    metrics["brief_checks"] = {
        "psychology_question": has_question,
        "psychology_emotion": has_emotion,
        "reference_mechanism": has_reference,
        "tv_50_percent_plan": has_tv50,
        "clutter_removal_plan": has_clutter,
        "obvious_hero_isolation": has_hero,
    }

    if not (has_question and has_emotion):
        errors.append(
            "Pre-Brief fails KE4zqD0ONDI Rule 2: Must specify BOTH what viewer should WONDER (Questions) and FEEL (Emotions) without relying on Title."
        )
    if not has_reference:
        warnings.append(
            "Pre-Brief lacks 5-source Reference & Underlying Mechanism note (Internal/External Outliers, Model 3, Bookmarks, Off-Platform)."
        )
    if not has_tv50:
        errors.append(
            "Pre-Brief fails KE4zqD0ONDI Rule 1: Missing explicit TV 50% Top-Half layout plan (hero + hook placement in upper 50% / top third)."
        )
    if not has_clutter:
        warnings.append(
            "Pre-Brief missing explicit Clutter Removal note (what background noise to strip)."
        )
    if not has_hero:
        errors.append(
            "Pre-Brief missing Obvious Main Character separation plan (color/contrast/rim/crop)."
        )

    # Extract A/B text candidates either from --ab-texts or brief lines like `Lead Words:` / `Variant B:`
    variants: List[str] = list(ab_texts or [])
    if not variants:
        for pat in [
            r"(?:Lead Words|Variant [A-Z]|A/B Variant [A-Z]|Text Overlay|Option [A-Z0-9])\s*:\s*[\"']?([^\"'\n]+)[\"']?",
        ]:
            for m in re.finditer(pat, raw, re.I):
                cand = m.group(1).strip()
                if cand and len(cand.split()) <= 6 and "{" not in cand:
                    variants.append(cand)
    variants = list(dict.fromkeys(variants))
    metrics["ab_text_variants"] = variants

    if len(variants) < 3:
        warnings.append(
            f"Found {len(variants)} A/B text variants (KE4zqD0ONDI recommends 3+ distinct 2-4 word variants for Test & Compare)."
        )
    for v in variants:
        wc = len(v.split())
        if wc > 4:
            warnings.append(
                f"A/B variant '{v}' has {wc} words (>4 words smears at 120px mobile)."
            )
        if title:
            ov = content_tokens(title) & content_tokens(v)
            if ov:
                errors.append(
                    f"A/B variant '{v}' repeats Title words {sorted(ov)} — 0% overlap required."
                )

    return {
        "status": "PASSED" if not errors else "FAILED",
        "errors": errors,
        "warnings": warnings,
        "metrics": metrics,
    }


def inspect_thumbnail(
    thumb_path: Path,
    title: Optional[str] = None,
    thumb_text: Optional[str] = None,
    out_dir: Optional[Path] = None,
) -> Dict[str, Any]:
    errors: List[str] = []
    warnings: List[str] = []
    metrics: Dict[str, Any] = {}

    if not thumb_path.exists():
        return {
            "status": "FAILED",
            "errors": [f"Thumbnail file not found: {thumb_path}"],
            "warnings": [],
            "metrics": {},
        }

    im = Image.open(thumb_path).convert("RGB")
    w, h = im.size
    metrics["size"] = [w, h]
    aspect = w / max(h, 1)
    metrics["aspect_ratio"] = round(aspect, 3)

    if w < 1280 or h < 720:
        errors.append(f"Resolution {w}x{h} is below 1280x720 minimum.")
    if abs(aspect - (16.0 / 9.0)) > 0.08:
        warnings.append(
            f"Aspect ratio {aspect:.2f} deviates from standard 16:9 (1.78)."
        )

    # 1. 120px Mobile Shrink Test
    mh = max(1, int(round(120 * h / max(w, 1))))
    mobile = im.resize((120, mh), Image.Resampling.LANCZOS)
    m_arr = np.asarray(mobile, dtype=np.float32)
    m_luma = 0.299 * m_arr[:, :, 0] + 0.587 * m_arr[:, :, 1] + 0.114 * m_arr[:, :, 2]
    luma_std = float(np.std(m_luma))
    metrics["mobile_120px_luma_std"] = round(luma_std, 2)
    if luma_std < 42.0:
        errors.append(
            f"Fails 120px mobile pop test: luma_std={luma_std:.2f} (minimum 42.0 required)."
        )

    # 2. TV 50% Top-Half Test (KE4zqD0ONDI Rule 1)
    bgr = cv2.imread(str(thumb_path))
    gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
    top_h = h // 2
    top50_gray = gray[:top_h, :]
    top33_gray = gray[: h // 3, :]
    top50_luma_std = float(np.std(top50_gray.astype(np.float32)))
    top33_luma_std = float(np.std(top33_gray.astype(np.float32)))

    edges = cv2.Canny(gray, 70, 170)
    top_edges = float(np.sum(edges[:top_h, :] > 0))
    bot_edges = float(np.sum(edges[top_h:, :] > 0))
    tot_edges = top_edges + bot_edges
    top50_edge_share = (top_edges / tot_edges) if tot_edges > 0 else 0.5

    edge_density = float(np.mean(edges > 0))
    metrics["tv_top50_luma_std"] = round(top50_luma_std, 2)
    metrics["tv_top33_luma_std"] = round(top33_luma_std, 2)
    metrics["tv_top50_edge_share"] = round(top50_edge_share, 3)
    metrics["edge_density"] = round(edge_density, 4)

    if top50_luma_std < 28.0:
        errors.append(
            f"Fails TV 50% Test: top half luma_std={top50_luma_std:.1f} (<28.0 — key elements look blank on TV row crop!)."
        )
    elif top50_luma_std < 36.0:
        warnings.append(
            f"Weak TV 50% Test contrast: top half luma_std={top50_luma_std:.1f} (aim >=36.0; move subject/text higher)."
        )

    if top50_edge_share < 0.30:
        errors.append(
            f"Fails TV 50% Test: only {top50_edge_share * 100:.1f}% of visual detail is in the top half (bottom-heavy layout invisible on TV!)."
        )
    elif top50_edge_share < 0.40:
        warnings.append(
            f"Bottom-biased composition: {top50_edge_share * 100:.1f}% of visual detail sits in top 50% (check TV top-half legibility)."
        )

    if edge_density > 0.16:
        warnings.append(
            f"High visual edge density ({edge_density * 100:.1f}%) — inspect for background clutter (KE4zqD0ONDI: remove anything not working for you)."
        )

    # 3. Title & Thumbnail Text Check
    if title:
        metrics["title_chars"] = len(title.strip())
    if thumb_text:
        tw = thumb_text.strip().split()
        metrics["thumb_text_words"] = len(tw)
        if len(tw) > 4:
            warnings.append(
                f"Thumbnail text has {len(tw)} words (target 2-4 max at 120px mobile feed scale)."
            )
        if title:
            overlap = content_tokens(title) & content_tokens(thumb_text)
            metrics["title_thumb_overlap"] = sorted(overlap)
            if overlap:
                errors.append(
                    f"Thumbnail text repeats Title words {sorted(overlap)} — violates Information Split rule."
                )

    # 4. Generate 4-Panel Diagnostic Strip if out_dir provided
    if out_dir is not None:
        out_dir.mkdir(parents=True, exist_ok=True)
        cw, ch = 640, 360
        canvas = Image.new("RGB", (2 * cw, 2 * ch), (15, 16, 20))
        draw = ImageDraw.Draw(canvas)

        p1 = im.resize((cw, ch), Image.Resampling.LANCZOS)
        canvas.paste(p1, (0, 0))

        p2 = p1.copy()
        d2 = ImageDraw.Draw(p2)
        d2.rectangle([0, ch // 2, cw, ch], fill=(18, 19, 22))
        d2.text(
            (16, ch // 2 + 16),
            "TV UI HIDES BOTTOM 50% UNTIL USER SCROLLS DOWN",
            fill=(180, 185, 195),
        )
        canvas.paste(p2, (cw, 0))

        p3 = Image.new("RGB", (cw, ch), (245, 245, 247))
        d3 = ImageDraw.Draw(p3)
        mob_x2 = mobile.resize(
            (240, int(round(240 * h / max(w, 1)))), Image.Resampling.NEAREST
        )
        p3.paste(mobile, (48, 95))
        d3.text((48, 68), "ACTUAL 120px MOBILE:", fill=(30, 30, 35))
        p3.paste(mob_x2, (240, 95))
        d3.text((240, 68), "2x FEED PREVIEW:", fill=(30, 30, 35))
        d3.rectangle([240, 240, 520, 264], fill=(210, 212, 218))
        d3.text(
            (246, 246),
            (title[:38] + "...")
            if title and len(title) > 38
            else (title or "Tiny shrinking mobile title..."),
            fill=(90, 94, 102),
        )
        canvas.paste(p3, (0, ch))

        p4 = Image.new("RGB", (cw, ch), (18, 19, 23))
        thumb_solo = im.resize((520, 292), Image.Resampling.LANCZOS)
        p4.paste(thumb_solo, (60, 20))
        d4 = ImageDraw.Draw(p4)
        d4.rectangle([60, 320, 580, 344], fill=(42, 44, 52))
        d4.text(
            (70, 325),
            "[TITLE HIDDEN - MUST EVOKE QUESTIONS & EMOTION ALONE]",
            fill=(220, 200, 130),
        )
        canvas.paste(p4, (cw, ch))

        labels = [
            (0, 0, "1. FULL 16:9 THUMBNAIL"),
            (
                cw,
                0,
                f"2. TV 50% TEST (top50_std={top50_luma_std:.1f}, edge={top50_edge_share * 100:.0f}%)",
            ),
            (0, ch, f"3. 120px MOBILE TEST (luma_std={luma_std:.1f})"),
            (cw, ch, "4. STANDALONE NO-TITLE TEST"),
        ]
        for lx, ly, txt in labels:
            draw.rectangle([lx + 8, ly + 8, lx + 430, ly + 30], fill=(10, 10, 14))
            draw.text((lx + 14, ly + 12), txt, fill=(255, 220, 95))

        sheet_path = out_dir / "_thumbnail_diagnostic_sheet.jpg"
        canvas.save(sheet_path, quality=92)
        metrics["diagnostic_sheet"] = str(sheet_path)

    return {
        "status": "PASSED" if not errors else "FAILED",
        "errors": errors,
        "warnings": warnings,
        "metrics": metrics,
    }


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Audit thumbnail BEFORE (--brief) and AFTER (--thumb) against KE4zqD0ONDI + 120px + TV 50% rules."
    )
    ap.add_argument(
        "--brief",
        type=Path,
        default=None,
        help="Pre-generation thumbnail brief/prompt markdown",
    )
    ap.add_argument(
        "--thumb", type=Path, default=None, help="Post-generation thumbnail PNG/JPG"
    )
    ap.add_argument("--title", type=str, default=None)
    ap.add_argument("--thumb-text", type=str, default=None)
    ap.add_argument(
        "--ab-texts",
        nargs="*",
        default=None,
        help="Optional list of 3+ A/B text variants",
    )
    ap.add_argument("--out-dir", type=Path, default=None)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    if not args.brief and not args.thumb:
        ap.error(
            "Provide at least --brief (BEFORE generation) or --thumb (AFTER generation)."
        )

    combined: Dict[str, Any] = {"status": "PASSED", "errors": [], "warnings": []}
    if args.brief:
        pre = inspect_brief(args.brief, title=args.title, ab_texts=args.ab_texts)
        combined["pre_generation"] = pre
        combined["errors"].extend(pre["errors"])
        combined["warnings"].extend(pre["warnings"])
    if args.thumb:
        post = inspect_thumbnail(
            args.thumb,
            title=args.title,
            thumb_text=args.thumb_text,
            out_dir=args.out_dir,
        )
        combined["post_generation"] = post
        combined["errors"].extend(post["errors"])
        combined["warnings"].extend(post["warnings"])
    combined["status"] = "PASSED" if not combined["errors"] else "FAILED"

    if args.json:
        print(json.dumps(combined, indent=2))
    else:
        print("=== THUMBNAIL PACKAGING AUDIT (BEFORE & AFTER - KE4zqD0ONDI) ===")
        print(json.dumps(combined, indent=2))
        print(
            "VERDICT:",
            "THUMBNAIL_GATE_PASSED"
            if combined["status"] == "PASSED"
            else "THUMBNAIL_GATE_FAILED",
        )
    return 0 if combined["status"] == "PASSED" else 1


if __name__ == "__main__":
    sys.exit(main())
