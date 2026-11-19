#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Universal Stage 2 Independent Multimodal Video & Sequence Supervisor (`run_multimodal_supervisor.py`).

Key guarantees:
1. Enforces `supervisor_model != generator_model` (strict independence; zero self-approval).
2. Uploads a full-motion 960x540 inspection proxy of the chapter MP4 to Gemini Files API
   with explicit HTTP timeout + retries so moving transitions, narration, and music sync are verified.
3. Sends all high-resolution `START | MID | END` contact sheets + EDL telemetry + script + optional fact-bible.
4. Outputs shot-by-shot CSV (`chapter_XX_shot_report.csv`), review Markdown (`chapter_XX_review.md`),
   verdict JSON, and exports full-res defect frames to `chapter_XX_critical_frames/`.
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import re
import subprocess
import tempfile
import time
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from google import genai
from google.genai import types


def _extract_exact_frame(video_path: Path, t_sec: float, out_jpg: Path) -> None:
    subprocess.run(
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
            str(out_jpg),
        ],
        check=True,
    )


def build_video_proxy(video_path: Path, proxy_mp4: Path) -> Path:
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-loglevel",
            "error",
            "-i",
            str(video_path),
            "-vf",
            "scale=960:540:flags=bicubic,fps=15",
            "-c:v",
            "libx264",
            "-preset",
            "veryfast",
            "-crf",
            "27",
            "-c:a",
            "aac",
            "-b:a",
            "96k",
            str(proxy_mp4),
        ],
        check=True,
    )
    return proxy_mp4


def run_chapter_supervisor(
    video_path: Path,
    telemetry_path: Path,
    out_dir: Path,
    script_path: Path | None = None,
    fact_bible: Path | None = None,
    env_file: Path | None = None,
    chapter_id: str = "chapter_01",
    language: str = "en",
    supervisor_model: str = "gemini-3.1-pro-preview",
    generator_model: str = "gemini-4-argon",
    round_label: str = "Round 1",
) -> dict[str, Any]:
    if (
        supervisor_model.strip().lower().split("/")[-1]
        == generator_model.strip().lower().split("/")[-1]
    ):
        raise RuntimeError(
            f"INDEPENDENCE VIOLATION: supervisor_model ({supervisor_model}) MUST differ from generator_model ({generator_model})!"
        )

    if env_file and env_file.exists():
        load_dotenv(env_file, override=True)
    else:
        load_dotenv()

    api_key = os.environ.get("GEMINI_API_KEY", "")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY not found in environment or --env-file")

    client = genai.Client(
        api_key=api_key,
        http_options={"api_version": "v1beta", "timeout": 240000},
    )
    telemetry = json.loads(telemetry_path.read_text(encoding="utf-8"))
    script_text = (
        script_path.read_text(encoding="utf-8", errors="ignore")
        if script_path and script_path.exists()
        else "(No separate script file provided — judge against spoken audio in video)"
    )

    skill_root = Path(__file__).resolve().parent.parent
    rubric_md = (skill_root / "references" / "15-point-director-rubric.md").read_text(
        encoding="utf-8"
    )
    bible_md = (
        fact_bible.read_text(encoding="utf-8", errors="ignore")
        if fact_bible and fact_bible.exists()
        else "(No external fact-bible provided — verify factual consistency against spoken narration and onscreen citations.)"
    )

    shots_context = []
    total_sh = len(telemetry["shots"])
    for sh in telemetry["shots"]:
        end_luma = float(sh["metrics"]["end_boundary_luma"])
        mid_luma = float(sh["metrics"]["mid_luma"])
        has_blk = len(sh.get("black_dips_in_shot", [])) > 0
        if int(sh["shot_number"]) == total_sh:
            trans_type = "CHAPTER_END_FADE_OUT"
        elif has_blk or (end_luma < 6.0 and mid_luma > 24.0):
            trans_type = "DIP_TO_BLACK_DETECTED"
        else:
            trans_type = (
                f"VERIFIED_STRAIGHT_CUT (0 black frames, boundary_luma={end_luma})"
            )
        shots_context.append(
            {
                "shot_number": sh["shot_number"],
                "start_ts": sh["start_ts"],
                "end_ts": sh["end_ts"],
                "duration_sec": sh["duration_sec"],
                "asset": Path(sh.get("asset_path", "")).name or sh.get("kind", ""),
                "provenance_badge": sh.get("provenance_badge"),
                "lower_third": f"{sh.get('lower_third_title') or ''} | {sh.get('lower_third_sub') or ''}".strip(
                    " |"
                ),
                "verified_transition_out": trans_type,
                "metrics": sh["metrics"],
                "telemetry_flags": sh["auto_telemetry_flags"],
            }
        )

    uploaded_video = None
    try:
        with tempfile.TemporaryDirectory() as tmpdir:
            proxy_p = build_video_proxy(
                video_path, Path(tmpdir) / f"{chapter_id}_proxy.mp4"
            )
            print(
                f"[Supervisor] Uploading moving video proxy ({proxy_p.stat().st_size / 1e6:.1f} MB) to {supervisor_model}...",
                flush=True,
            )
            uploaded_video = client.files.upload(file=str(proxy_p))
            while uploaded_video.state.name == "PROCESSING":
                time.sleep(2.0)
                uploaded_video = client.files.get(name=uploaded_video.name)
            if uploaded_video.state.name != "ACTIVE":
                raise RuntimeError(f"Video upload state={uploaded_video.state.name}")

        parts: list[Any] = [uploaded_video]
        for cs_path in telemetry["contact_sheets"]:
            p = Path(cs_path)
            if p.exists():
                parts.append(
                    types.Part.from_bytes(data=p.read_bytes(), mime_type="image/jpeg")
                )

        prompt = f"""
You are `visual-supervisor-judge` ({round_label}), an uncompromising, independent Senior Documentary Director, Cinematographer, Film Editor, Colorist, Sound Supervisor, and Visual Fact-Check Judge.
Review language for report prose: `{language}`.

Your job is NOT to praise generated work. Inspect BOTH the full moving video (live narration, music, pacing, transitions) AND every shot's [START | MID | END] contact sheets across all 15 rubric criteria. Find every real mistake, score strictly without inflation, and demand concrete fixes.

### RUBRIC & SCORING RULES
{rubric_md}

### DOMAIN FACT BIBLE
{bible_md}

### CHAPTER SCRIPT
{script_text[:18000]}

### DETERMINISTIC TELEMETRY & SHOT LIST ({len(shots_context)} SHOTS)
Audio EBU R128: {json.dumps(telemetry["ffmpeg_telemetry"]["audio_ebur128"])}
Black intervals detected: {len(telemetry["ffmpeg_telemetry"]["black_intervals"])}
Silence intervals >1.8s: {json.dumps(telemetry["ffmpeg_telemetry"]["silence_intervals_gt_1_8s"])}
Shots:
{json.dumps(shots_context, ensure_ascii=False, indent=2)}

### INSTRUCTIONS
1. Watch the moving video from start to finish AND inspect all contact sheets carefully across all 15 criteria.
2. ANTI-HALLUCINATION RULE: Never claim a shot has a `dip-to-black` when `verified_transition_out` is `VERIFIED_STRAIGHT_CUT` and `Black intervals detected` is `0`. Criticize ONLY real observable defects.
3. Evaluate EVERY single shot (1 through {len(shots_context)}) and return STRICT valid JSON matching this schema:
{{
  "chapter_id": "{chapter_id}",
  "round": "{round_label}",
  "supervisor_model": "{supervisor_model}",
  "generator_model": "{generator_model}",
  "scores": {{
    "cinematography": 0.0,
    "composition": 0.0,
    "editing": 0.0,
    "visual_consistency": 0.0,
    "historical_accuracy": 0.0,
    "sound": 0.0,
    "storytelling": 0.0,
    "emotional_impact": 0.0,
    "overall_score": 0.0
  }},
  "score_justifications": {{
    "cinematography": "...",
    "composition": "...",
    "editing": "...",
    "visual_consistency": "...",
    "historical_accuracy": "...",
    "sound": "...",
    "storytelling": "...",
    "emotional_impact": "...",
    "overall_verdict": "..."
  }},
  "executive_critique": "...",
  "sequence_and_continuity_notes": ["..."],
  "audio_and_sync_notes": ["..."],
  "editing_supervisor_actions": [
    {{
      "action_type": "REPLACE|SHORTEN|EXTEND|FIX_CONTRAST|FIX_TRANSITION|KEEP",
      "shot_numbers": [1],
      "timestamp_span": "00:00-00:09",
      "reason": "...",
      "exact_fix": "..."
    }}
  ],
  "shots": [
    {{
      "shot_number": 1,
      "start_ts": "00:00.00",
      "end_ts": "00:09.63",
      "score": 8.0,
      "severity": "NONE|MINOR|MAJOR|CRITICAL",
      "failed_criteria": ["..."],
      "what_is_wrong": "...",
      "why_it_weakens_film": "...",
      "visual_evidence": "...",
      "recommended_correction": "..."
    }}
  ]
}}
"""
        parts.append(types.Part.from_text(text=prompt))
        print(
            f"[Supervisor] Running {supervisor_model} deep 15-criteria audit...",
            flush=True,
        )
        resp = None
        for attempt in range(3):
            try:
                resp = client.models.generate_content(
                    model=supervisor_model,
                    contents=parts,
                    config=types.GenerateContentConfig(
                        temperature=0.15,
                        response_mime_type="application/json",
                    ),
                )
                break
            except Exception as exc:
                print(f"[Supervisor] Retry {attempt + 1}: {exc}", flush=True)
                if attempt == 2:
                    raise
                time.sleep(3.0 * (attempt + 1))
    finally:
        if uploaded_video is not None:
            try:
                client.files.delete(name=uploaded_video.name)
            except Exception:
                pass

    raw = resp.text.strip()
    if raw.startswith("```"):
        raw = re.sub(r"^```(?:json)?\s*", "", raw)
        raw = re.sub(r"\s*```$", "", raw)
    result = json.loads(raw)

    # Programmatic anti-inflation enforcement
    crit_n = sum(1 for s in result["shots"] if s.get("severity") == "CRITICAL")
    maj_n = sum(1 for s in result["shots"] if s.get("severity") == "MAJOR")
    axis_vals = [
        float(result["scores"][k])
        for k in [
            "cinematography",
            "composition",
            "editing",
            "visual_consistency",
            "historical_accuracy",
            "sound",
            "storytelling",
            "emotional_impact",
        ]
    ]
    computed_avg = round(sum(axis_vals) / len(axis_vals), 2)
    if crit_n > 0:
        computed_avg = min(computed_avg, 6.5)
    elif maj_n > 0:
        computed_avg = min(computed_avg, 8.4)
    result["scores"]["overall_score"] = computed_avg
    result["defect_counts"] = {
        "critical": crit_n,
        "major": maj_n,
        "minor": sum(1 for s in result["shots"] if s.get("severity") == "MINOR"),
    }

    out_dir.mkdir(parents=True, exist_ok=True)
    json_out = out_dir / f"{chapter_id}_supervisor_verdict.json"
    json_out.write_text(
        json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    csv_out = out_dir / f"{chapter_id}_shot_report.csv"
    tel_by_num = {int(s["shot_number"]): s for s in telemetry["shots"]}
    cf_dir = out_dir / f"{chapter_id}_critical_frames"
    cf_dir.mkdir(parents=True, exist_ok=True)

    with open(csv_out, "w", newline="", encoding="utf-8") as cf:
        writer = csv.writer(cf)
        writer.writerow(
            [
                "shot_number",
                "start_timestamp",
                "end_timestamp",
                "duration_sec",
                "asset_source",
                "score_1_to_10",
                "severity",
                "failed_criteria",
                "detected_problems",
                "why_it_weakens_film",
                "visual_evidence",
                "recommended_correction",
            ]
        )
        for s in result["shots"]:
            snum = int(s["shot_number"])
            t_meta = tel_by_num.get(snum, {})
            dur_s = t_meta.get("duration_sec", 0.0)
            src_name = Path(t_meta.get("asset_path", "")).name or t_meta.get("kind", "")
            sev = s.get("severity", "NONE")
            writer.writerow(
                [
                    snum,
                    s.get("start_ts", t_meta.get("start_ts", "")),
                    s.get("end_ts", t_meta.get("end_ts", "")),
                    dur_s,
                    src_name,
                    s.get("score", ""),
                    sev,
                    "; ".join(s.get("failed_criteria", [])),
                    s.get("what_is_wrong", ""),
                    s.get("why_it_weakens_film", ""),
                    s.get("visual_evidence", ""),
                    s.get("recommended_correction", ""),
                ]
            )
            if sev in ("CRITICAL", "MAJOR") and t_meta:
                mid_t = (float(t_meta["start_sec"]) + float(t_meta["end_sec"])) / 2.0
                _extract_exact_frame(
                    video_path,
                    mid_t,
                    cf_dir
                    / f"{round_label.lower().replace(' ', '_')}_shot_{snum:02d}_{sev}.jpg",
                )

    sc = result["scores"]
    sj = result.get("score_justifications", {})
    md = [
        f"# VISUAL SUPERVISOR REVIEW — {chapter_id.upper()} ({round_label})",
        f"- **File:** `{video_path.name}` (`{telemetry['ffmpeg_telemetry']['duration_mmss']}`)",
        f"- **Independent Supervisor Model:** `{supervisor_model}` *(generator: `{generator_model}`)*",
        f"- **Defects:** `CRITICAL: {crit_n}` | `MAJOR: {maj_n}` | `MINOR: {result['defect_counts']['minor']}`",
        "",
        "## 1. 8-Axis Scorecard (1–10)",
        "| Axis | Score | Justification |",
        "|---|---:|---|",
        f"| 1. Cinematography | **{sc['cinematography']}/10** | {sj.get('cinematography', '')} |",
        f"| 2. Composition | **{sc['composition']}/10** | {sj.get('composition', '')} |",
        f"| 3. Editing | **{sc['editing']}/10** | {sj.get('editing', '')} |",
        f"| 4. Visual Consistency | **{sc['visual_consistency']}/10** | {sj.get('visual_consistency', '')} |",
        f"| 5. Historical / Fact Accuracy | **{sc['historical_accuracy']}/10** | {sj.get('historical_accuracy', '')} |",
        f"| 6. Sound | **{sc['sound']}/10** | {sj.get('sound', '')} |",
        f"| 7. Storytelling | **{sc['storytelling']}/10** | {sj.get('storytelling', '')} |",
        f"| 8. Emotional Impact | **{sc['emotional_impact']}/10** | {sj.get('emotional_impact', '')} |",
        f"| **OVERALL SCORE** | **{sc['overall_score']}/10** | {sj.get('overall_verdict', '')} |",
        "",
        "## 2. Executive Critique",
        result.get("executive_critique", ""),
        "",
        "## 3. Sequence & Continuity Notes",
    ]
    for item in result.get("sequence_and_continuity_notes", []):
        md.append(f"- {item}")

    md.append("\n## 4. Audio & Sync Notes")
    eb = telemetry["ffmpeg_telemetry"]["audio_ebur128"]
    md.append(
        f"- **EBU R128:** Integrated `{eb['integrated_lufs']} LUFS`, LRA `{eb['loudness_range_lu']} LU`, True Peak `{eb['true_peak_dbfs']} dBFS`."
    )
    for item in result.get("audio_and_sync_notes", []):
        md.append(f"- {item}")

    md.append("\n## 5. Flagged Shots (Critical / Major / Minor)")
    flagged = [s for s in result["shots"] if s.get("severity", "NONE") != "NONE"]
    if not flagged:
        md.append("- No defects flagged.")
    else:
        for s in flagged:
            md.append(
                f"### Shot #{s['shot_number']:02d} (`{s.get('start_ts')}` – `{s.get('end_ts')}`) — **{s['severity']}** (`{s['score']}/10`)\n"
                f"- **Failed Criteria:** {', '.join(s.get('failed_criteria', []))}\n"
                f"- **Issue:** {s.get('what_is_wrong')}\n"
                f"- **Impact:** {s.get('why_it_weakens_film')}\n"
                f"- **Evidence:** {s.get('visual_evidence')}\n"
                f"- **Fix:** {s.get('recommended_correction')}\n"
            )

    md.append("\n## 6. Editing Supervisor Directives")
    for act in result.get("editing_supervisor_actions", []):
        md.append(
            f"- **[{act.get('action_type')}] Shots {act.get('shot_numbers')} (`{act.get('timestamp_span')}`):** "
            f"{act.get('reason')} -> *Fix:* {act.get('exact_fix')}"
        )

    review_out = out_dir / f"{chapter_id}_review.md"
    review_out.write_text("\n".join(md), encoding="utf-8")
    print(
        f"[Supervisor Done] {chapter_id} ({round_label}): overall={sc['overall_score']}/10 | "
        f"CRITICAL={crit_n}, MAJOR={maj_n}, MINOR={result['defect_counts']['minor']} -> {review_out}",
        flush=True,
    )
    return result


def main() -> None:
    ap = argparse.ArgumentParser(
        description="Universal Independent Multimodal Visual Supervisor."
    )
    ap.add_argument("--video", required=True, type=Path)
    ap.add_argument("--telemetry", required=True, type=Path)
    ap.add_argument("--out-dir", required=True, type=Path)
    ap.add_argument("--script", type=Path, default=None)
    ap.add_argument("--fact-bible", type=Path, default=None)
    ap.add_argument("--env-file", type=Path, default=None)
    ap.add_argument("--chapter-id", default="chapter_01")
    ap.add_argument("--language", default="en")
    ap.add_argument("--supervisor-model", default="gemini-3.1-pro-preview")
    ap.add_argument("--generator-model", default="gemini-4-argon")
    ap.add_argument("--round-label", default="Round 1")
    args = ap.parse_args()
    run_chapter_supervisor(
        video_path=args.video,
        telemetry_path=args.telemetry,
        out_dir=args.out_dir,
        script_path=args.script,
        fact_bible=args.fact_bible,
        env_file=args.env_file,
        chapter_id=args.chapter_id,
        language=args.language,
        supervisor_model=args.supervisor_model,
        generator_model=args.generator_model,
        round_label=args.round_label,
    )


if __name__ == "__main__":
    main()
