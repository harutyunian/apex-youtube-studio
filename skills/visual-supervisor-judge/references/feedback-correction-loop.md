# Producer <-> Independent Visual Supervisor Feedback Loop

## Mandatory Separation of Powers

```text
┌───────────────────────────┐
│   PRODUCTION PIPELINE     │  (e.g. gemini-4-carbon / assemble_act_video.py)
│   Renders Chapter MP4     │
└─────────────┬─────────────┘
              │
              ▼
┌───────────────────────────┐
│  STAGE 1: TELEMETRY       │  scripts/inspect_chapter.py
│  PySceneDetect + FFmpeg   │  -> Contact sheets (START|MID|END), blackdetect, LUFS
└─────────────┬─────────────┘
              │
              ▼
┌───────────────────────────┐
│  STAGE 2: SUPERVISOR      │  scripts/run_multimodal_supervisor.py
│  INDEPENDENT MODEL        │  (e.g. gemini-3.1-pro-preview — NEVER generator!)
│  Video Upload + 15-Rubric │  -> chapter_XX_shot_report.csv + chapter_XX_review.md
└─────────────┬─────────────┘
              │
              ▼
┌───────────────────────────┐
│  STAGE 3: HARD GATE       │  scripts/verify_supervisor_gate.py
│  CRITICAL == 0            │  Checks CSV, scores >= 8.0, model independence,
│  Overall Score >= 8.0     │  provenance labels, audio LUFS/peaks
└──────┬─────────────┬──────┘
       │ PASS        │ BLOCK (Exit 1)
       ▼             ▼
  [ CHAPTER     ┌───────────────────────────────────────────┐
    APPROVED ]  │  PRODUCTION FIX CYCLE (Max 3 Rounds)      │
                │  1. Replace wrong archival/AI assets      │
                │  2. Split dragging (>15s) shots           │
                │  3. Fix contrast / transition defects     │
                │  4. Re-render chapter & re-run Stage 1–3  │
                └───────────────────────────────────────────┘
```

## Convergence Rules
1. **Round 1 Audit:** Preserve Round 1's critical frames and findings in the review history so improvements are auditable, never silently erased.
2. **Targeted Fixes:** Fix every `CRITICAL` issue and every high-impact `MAJOR` issue (pacing drags, dip-to-black overuse, contrast collisions, historical mismatches).
3. **Re-Verification:** Re-run `inspect_chapter.py`, `run_multimodal_supervisor.py`, and `verify_supervisor_gate.py` on the newly rendered MP4 from scratch.
4. **Explicit Handoff if Capped:** If an external constraint prevents resolving a minor/major item after 3 rounds, document it transparently in `final_quality_report.md` rather than inflating the score.
