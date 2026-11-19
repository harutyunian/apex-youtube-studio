#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Universal Full-Film Independent Documentary Supervisor (`run_full_film_supervisor.py`).

Auto-discovers all `chapter_*_telemetry.json` and `chapter_*_supervisor_verdict.json` files
inside `--qc-dir`, aggregates telemetry across N chapters, runs an independent multimodal
cross-chapter review, and generates:
1. `editing_recommendations.md`
2. `historical_accuracy_report.md`
3. `audio_review.md`
4. `final_quality_report.md`
"""

from __future__ import annotations

import argparse
import json
import os
import re
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from google import genai
from google.genai import types


def _fmt_mmss(sec: float) -> str:
    tot = int(round(sec))
    return f"{tot // 60:02d}:{tot % 60:02d}"


def run_full_film_audit(
    qc_dir: Path,
    project_title: str = "YouTube Documentary Feature",
    master_video_name: str = "master.mp4",
    fact_bible: Path | None = None,
    env_file: Path | None = None,
    language: str = "en",
    supervisor_model: str = "gemini-3.1-pro-preview",
    generator_model: str = "gemini-4-argon",
) -> None:
    if (
        supervisor_model.strip().lower().split("/")[-1]
        == generator_model.strip().lower().split("/")[-1]
    ):
        raise RuntimeError("Supervisor model must be independent of generator model!")

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

    skill_root = Path(__file__).resolve().parent.parent
    rubric_md = (skill_root / "references" / "15-point-director-rubric.md").read_text(
        encoding="utf-8"
    )
    bible_md = (
        fact_bible.read_text(encoding="utf-8", errors="ignore")
        if fact_bible and fact_bible.exists()
        else "(No external fact-bible provided — audit internal factual & archival provenance consistency.)"
    )

    tel_files = sorted(qc_dir.glob("chapter_*_telemetry.json"))
    if not tel_files:
        raise RuntimeError(f"No chapter_*_telemetry.json files found in {qc_dir}")

    chapters_payload = []
    parts: list[Any] = []
    global_offset = 0.0
    verdicts_by_cid: dict[str, dict[str, Any]] = {}

    for tf in tel_files:
        cid = tf.name.replace("_telemetry.json", "")
        tel = json.loads(tf.read_text(encoding="utf-8"))
        vp = qc_dir / f"{cid}_supervisor_verdict.json"
        if vp.exists():
            verdicts_by_cid[cid] = json.loads(vp.read_text(encoding="utf-8"))

        dur = float(tel["ffmpeg_telemetry"]["duration_sec"])
        n_shots = int(tel["declared_or_evaluated_shot_count"])
        asl = round(dur / max(1, n_shots), 2)

        overlong = [
            {
                "shot": s["shot_number"],
                "chap_ts": f"{s['start_ts']}-{s['end_ts']}",
                "film_ts": f"{_fmt_mmss(global_offset + s['start_sec'])}-{_fmt_mmss(global_offset + s['end_sec'])}",
                "dur_s": s["duration_sec"],
                "asset": Path(s.get("asset_path", "")).name or s.get("kind", ""),
                "title": s.get("lower_third_title") or "Visual / Graphic",
            }
            for s in tel["shots"]
            if float(s["duration_sec"]) > 10.0
        ]

        chapters_payload.append(
            {
                "chapter_id": cid,
                "film_offset_start_mmss": _fmt_mmss(global_offset),
                "film_offset_end_mmss": _fmt_mmss(global_offset + dur),
                "duration_sec": dur,
                "duration_mmss": tel["ffmpeg_telemetry"]["duration_mmss"],
                "shot_count": n_shots,
                "average_shot_length_sec": asl,
                "pyscenedetect_cuts": tel.get("pyscenedetect_cut_count", 0),
                "black_intervals_count": len(
                    tel["ffmpeg_telemetry"]["black_intervals"]
                ),
                "silence_intervals_gt_1_8s": tel["ffmpeg_telemetry"][
                    "silence_intervals_gt_1_8s"
                ],
                "audio_ebur128": tel["ffmpeg_telemetry"]["audio_ebur128"],
                "overlong_shots_gt_10s": overlong,
                "existing_verdict": verdicts_by_cid.get(cid, {}).get("scores"),
                "all_shots_summary": [
                    {
                        "shot": s["shot_number"],
                        "ts": f"{s['start_ts']}-{s['end_ts']}",
                        "dur": s["duration_sec"],
                        "asset": Path(s.get("asset_path", "")).name
                        or s.get("kind", ""),
                        "prov": s.get("provenance_badge"),
                        "title": s.get("lower_third_title"),
                    }
                    for s in tel["shots"]
                ],
            }
        )
        global_offset += dur

        for cs_idx in range(min(2, len(tel.get("contact_sheets", [])))):
            cs_p = Path(tel["contact_sheets"][cs_idx])
            if cs_p.exists():
                parts.append(
                    types.Part.from_bytes(
                        data=cs_p.read_bytes(), mime_type="image/jpeg"
                    )
                )

    prompt = f"""
You are `visual-supervisor-judge` ({supervisor_model}), an uncompromising, independent Senior Documentary Director, Cinematographer, Film Editor, Historical/Fact Consultant, and Sound Supervisor reviewing `{project_title}` ({len(chapters_payload)} chapters, {_fmt_mmss(global_offset)} runtime).
Write critique prose in `{language}`.

Do NOT praise or inflate scores. Evaluate strictly against the 15-point rubric and Fact Bible using the attached contact sheets and telemetry.

### RUBRIC & FACT BIBLE
{rubric_md}
{bible_md}

### TELEMETRY & CHAPTER SUMMARIES
{json.dumps(chapters_payload, ensure_ascii=False, indent=2)}

Return STRICT valid JSON matching this schema:
{{
  "chapter_scores_matrix": [
    {{
      "chapter_id": "chapter_01",
      "cinematography": 7.5,
      "composition": 7.5,
      "editing": 7.5,
      "visual_consistency": 7.5,
      "historical_accuracy": 8.0,
      "sound": 7.5,
      "storytelling": 7.5,
      "emotional_impact": 7.5,
      "overall": 7.5,
      "critical_open": 0,
      "key_note": "..."
    }}
  ],
  "director_opening_and_arc_critique": "...",
  "editing_specific_notes": ["..."],
  "historical_findings": [
    {{
      "chapter_id": "chapter_XX",
      "shot_ref": "Shot #N (MM:SS)",
      "status": "VERIFIED_CLEAN | FIXED | MINOR_NOTE | MAJOR_NOTE | CRITICAL",
      "detail": "..."
    }}
  ],
  "audio_director_critique": "...",
  "executive_final_verdict": "..."
}}
"""
    parts.append(types.Part.from_text(text=prompt))
    print(
        f"[Full-Film Supervisor] Auditing {len(chapters_payload)} chapters via {supervisor_model}...",
        flush=True,
    )
    resp = client.models.generate_content(
        model=supervisor_model,
        contents=parts,
        config=types.GenerateContentConfig(
            temperature=0.15, response_mime_type="application/json"
        ),
    )
    raw = resp.text.strip()
    if raw.startswith("```"):
        raw = re.sub(r"^```(?:json)?\s*", "", raw)
        raw = re.sub(r"\s*```$", "", raw)
    data = json.loads(raw)

    matrix = data["chapter_scores_matrix"]
    (qc_dir / "full_film_scores_matrix.json").write_text(
        json.dumps(matrix, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    ed_lines = [
        "# EDITING RECOMMENDATIONS & PACING AUDIT",
        f"- **Project:** `{project_title}` (`{_fmt_mmss(global_offset)}` across `{len(chapters_payload)}` chapters)",
        f"- **Independent Supervisor:** `{supervisor_model}` *(generator: `{generator_model}`)*",
        "",
        "## 1. Opening Hook, Narrative Arc & Structural Critique",
        data.get("director_opening_and_arc_critique", ""),
        "",
        "## 2. Chapter Telemetry Summary",
        "| Chapter | Film Offset | Duration | Shots | PySceneDetect Cuts | Avg Shot (ASL) | Shots > 10s | Black Gaps |",
        "|---|---|---|---:|---:|---:|---:|---:|",
    ]
    for ch in chapters_payload:
        ed_lines.append(
            f"| **{ch['chapter_id']}** | `{ch['film_offset_start_mmss']}–{ch['film_offset_end_mmss']}` | `{ch['duration_mmss']}` | "
            f"`{ch['shot_count']}` | `{ch['pyscenedetect_cuts']}` | **`{ch['average_shot_length_sec']}s`** | `{len(ch['overlong_shots_gt_10s'])}` | `{ch['black_intervals_count']}` |"
        )
    ed_lines.append("\n## 3. Specific Editing Notes")
    for note in data.get("editing_specific_notes", []):
        ed_lines.append(f"- {note}")
    ed_lines.append("\n## 4. Shots > 10.0s Requiring Split / Visual Variety")
    for ch in chapters_payload:
        for ov in ch["overlong_shots_gt_10s"]:
            ed_lines.append(
                f"- `{ch['chapter_id']}` Shot `#{ov['shot']:02d}` (`{ov['film_ts']}`, `{ov['dur_s']:.1f}s`, `{ov['asset']}`): Split into <=3.5s context-driven cuts."
            )
    (qc_dir / "editing_recommendations.md").write_text(
        "\n".join(ed_lines), encoding="utf-8"
    )

    hist_lines = [
        "# FACTUAL ACCURACY & PROVENANCE REPORT",
        f"- **Project:** `{project_title}`",
        f"- **Independent Supervisor:** `{supervisor_model}`",
        "",
        "## Cross-Chapter Findings",
    ]
    for hf in data.get("historical_findings", []):
        hist_lines.append(
            f"- **`{hf.get('chapter_id')}` — {hf.get('shot_ref')} [`{hf.get('status')}`]:** {hf.get('detail')}"
        )
    (qc_dir / "historical_accuracy_report.md").write_text(
        "\n".join(hist_lines), encoding="utf-8"
    )

    aud_lines = [
        "# AUDIO & LOUDNESS REVIEW",
        f"- **Master:** `{master_video_name}`",
        f"- **Independent Supervisor:** `{supervisor_model}`",
        "",
        "| Chapter | Duration | Integrated LUFS | LRA | True Peak (dBFS) | Silences >1.8s |",
        "|---|---|---:|---:|---:|---:|",
    ]
    for ch in chapters_payload:
        eb = ch["audio_ebur128"]
        aud_lines.append(
            f"| **{ch['chapter_id']}** | `{ch['duration_mmss']}` | `{eb['integrated_lufs']}` | `{eb['loudness_range_lu']}` | `{eb['true_peak_dbfs']}` | `{len(ch['silence_intervals_gt_1_8s'])}` |"
        )
    aud_lines.extend(
        ["", "## Director Audio Critique", data.get("audio_director_critique", "")]
    )
    (qc_dir / "audio_review.md").write_text("\n".join(aud_lines), encoding="utf-8")

    avg_overall = round(
        sum(float(m["overall"]) for m in matrix) / max(1, len(matrix)), 2
    )
    total_crit = sum(int(m.get("critical_open", 0)) for m in matrix)
    fin_lines = [
        "# FINAL QUALITY REPORT (VISUAL SUPERVISOR JUDGE)",
        f"- **Project:** `{project_title}` (`{_fmt_mmss(global_offset)}`)",
        f"- **Independent Supervisor:** `{supervisor_model}` *(generator: `{generator_model}`)*",
        f"- **Open CRITICAL Defects:** `{total_crit}`",
        f"- **Mean Chapter Score:** **`{avg_overall} / 10.0`**",
        "",
        "| Chapter | Cinema | Comp | Editing | Consistency | Fact/Hist | Sound | Story | Emotion | Overall | Crit | Notes |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|",
    ]
    for m in matrix:
        fin_lines.append(
            f"| **{m['chapter_id']}** | {m['cinematography']} | {m['composition']} | {m['editing']} | "
            f"{m['visual_consistency']} | {m['historical_accuracy']} | {m['sound']} | {m['storytelling']} | "
            f"{m['emotional_impact']} | **{m['overall']}** | `{m.get('critical_open', 0)}` | {m.get('key_note', '')} |"
        )
    fin_lines.extend(
        ["", "## Executive Verdict", data.get("executive_final_verdict", "")]
    )
    (qc_dir / "final_quality_report.md").write_text(
        "\n".join(fin_lines), encoding="utf-8"
    )
    print("[Full-Film Supervisor] Reports generated successfully!")


def main() -> None:
    ap = argparse.ArgumentParser(
        description="Universal Full-Film Independent Visual Supervisor."
    )
    ap.add_argument("--qc-dir", required=True, type=Path)
    ap.add_argument("--project-title", default="YouTube Documentary Feature")
    ap.add_argument("--master-video", default="master.mp4")
    ap.add_argument("--fact-bible", type=Path, default=None)
    ap.add_argument("--env-file", type=Path, default=None)
    ap.add_argument("--language", default="en")
    ap.add_argument("--supervisor-model", default="gemini-3.1-pro-preview")
    ap.add_argument("--generator-model", default="gemini-4-argon")
    args = ap.parse_args()
    run_full_film_audit(
        qc_dir=args.qc_dir,
        project_title=args.project_title,
        master_video_name=args.master_video,
        fact_bible=args.fact_bible,
        env_file=args.env_file,
        language=args.language,
        supervisor_model=args.supervisor_model,
        generator_model=args.generator_model,
    )


if __name__ == "__main__":
    main()
