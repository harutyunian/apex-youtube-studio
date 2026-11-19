#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Stage 3 Hard Release Gate (`verify_supervisor_gate.py`)
for the `visual-supervisor-judge` skill.

Enforces:
1. All mandatory `quality_control/` reports, CSVs, contact sheets, and critical frame folders exist;
2. `supervisor_model != generator_model` (strict independence; zero self-approval);
3. Unresolved `CRITICAL` defects == 0 (NEVER waiverable);
4. `overall_score >= min_score` (default 8.0), OR `--allow-documented-issues` is explicitly set
   after multi-round convergence when remaining non-critical medium/pacing issues are transparently
   documented in `final_quality_report.md` and `editing_recommendations.md` (Section 8 Step 6);
5. Broadcast audio loudness within [-18.5, -13.5] LUFS and True Peak <= -0.8 dBFS.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def verify_gate(
    qc_dir: Path,
    chapter_id: str = "chapter_01",
    min_score: float = 8.0,
    check_full_film: bool = False,
    allow_documented_issues: bool = False,
) -> int:
    errors: list[str] = []
    warnings: list[str] = []

    req_chapter_files = [
        qc_dir / f"{chapter_id}_telemetry.json",
        qc_dir / f"{chapter_id}_supervisor_verdict.json",
        qc_dir / f"{chapter_id}_review.md",
        qc_dir / f"{chapter_id}_shot_report.csv",
        qc_dir / f"{chapter_id}_contact_sheets",
        qc_dir / f"{chapter_id}_critical_frames",
    ]
    for p in req_chapter_files:
        if not p.exists():
            errors.append(f"MISSING_ARTIFACT: {p}")

    if check_full_film:
        for fn in [
            "editing_recommendations.md",
            "historical_accuracy_report.md",
            "audio_review.md",
            "final_quality_report.md",
        ]:
            fp = qc_dir / fn
            if not fp.exists() or fp.stat().st_size < 300:
                errors.append(f"MISSING_OR_EMPTY_FILM_REPORT: {fp}")

    if errors:
        print("SUPERVISOR GATE FAILED (missing mandatory artifacts):")
        for e in errors:
            print(f"  - {e}")
        return 1

    tel = json.loads(
        (qc_dir / f"{chapter_id}_telemetry.json").read_text(encoding="utf-8")
    )
    verdict = json.loads(
        (qc_dir / f"{chapter_id}_supervisor_verdict.json").read_text(encoding="utf-8")
    )

    sup_m = str(verdict.get("supervisor_model", "")).lower().split("/")[-1]
    gen_m = str(verdict.get("generator_model", "")).lower().split("/")[-1]
    if not sup_m or sup_m == gen_m:
        errors.append(f"SELF_APPROVAL_VIOLATION: supervisor={sup_m} generator={gen_m}")

    crit = int(verdict.get("defect_counts", {}).get("critical", 0))
    maj = int(verdict.get("defect_counts", {}).get("major", 0))
    overall = float(verdict.get("scores", {}).get("overall_score", 0.0))

    if crit > 0:
        errors.append(
            f"UNRESOLVED_CRITICAL_DEFECTS: {crit} critical issue(s) remain open (NEVER waiverable)"
        )

    if overall < min_score:
        if (
            allow_documented_issues
            and (qc_dir / "final_quality_report.md").exists()
            and (qc_dir / "editing_recommendations.md").exists()
        ):
            warnings.append(
                f"DOCUMENTED_BELOW_TARGET_SCORE: overall_score={overall} < {min_score} "
                f"(CRITICAL=0, MAJOR={maj} explicitly documented in final_quality_report.md & editing_recommendations.md)"
            )
        else:
            errors.append(
                f"SCORE_BELOW_THRESHOLD: overall_score={overall} < min_score={min_score}"
            )

    ebur = tel.get("ffmpeg_telemetry", {}).get("audio_ebur128", {})
    lufs = ebur.get("integrated_lufs")
    tp = ebur.get("true_peak_dbfs")
    if lufs is not None and not (-18.5 <= float(lufs) <= -13.5):
        errors.append(
            f"AUDIO_LOUDNESS_OUT_OF_SPEC: {lufs} LUFS (expected -18.5..-13.5)"
        )
    if tp is not None and float(tp) > -0.8:
        errors.append(f"AUDIO_TRUE_PEAK_CLIPPING_RISK: {tp} dBFS (expected <= -0.8)")

    if errors:
        print(f"=== SUPERVISOR GATE BLOCKED ({chapter_id}) ===")
        for e in errors:
            print(f"  [BLOCK] {e}")
        return 1

    print(
        f"=== SUPERVISOR GATE PASSED ({chapter_id}) | overall={overall}/10 | "
        f"CRITICAL=0 | LUFS={lufs} | independent_model={sup_m} (!= {gen_m}) ==="
    )
    for w in warnings:
        print(f"  [DOCUMENTED_HANDOFF] {w}")
    return 0


def main() -> None:
    ap = argparse.ArgumentParser(
        description="Verify independent visual-supervisor-judge quality gate."
    )
    ap.add_argument("--qc-dir", required=True, type=Path)
    ap.add_argument("--chapter-id", default="chapter_01")
    ap.add_argument("--min-score", type=float, default=8.0)
    ap.add_argument("--full-film", action="store_true")
    ap.add_argument("--allow-documented-issues", action="store_true")
    args = ap.parse_args()
    sys.exit(
        verify_gate(
            args.qc_dir,
            args.chapter_id,
            args.min_score,
            args.full_film,
            args.allow_documented_issues,
        )
    )


if __name__ == "__main__":
    main()
