# 4-Stage BEFORE & AFTER Production Workflow (`WORKFLOW.md`)

Follow these exact 4 stages for every YouTube video or Short so weak hooks, broken thumbnails, static AI stretches, and dead-end conclusions are caught **before** you waste rendering time—and double-checked **after** rendering.

---

## Stage 1 — BEFORE Thumbnail Generation (`PRE_GENERATION`)
1. **Run `youtube-producer`:** Collect outliers (`swipe.py`), lock the 10x Escalation Arc, score 10 titles with `skills/yt-package/title.py`, and draft `thumbnail_brief.md` using `skills/yt-thumbnail-brief/references/brief-template.md`.
2. **Deterministic Pre-Brief Check:**
   ```bash
   python3 skills/yt-thumbnail-brief/scripts/audit_thumbnail.py \
     --brief thumbnail_brief.md \
     --title "Exact Title" \
     --ab-texts "VARIANT A" "VARIANT B" "VARIANT C"
   ```
3. **Subagent Gate (`thumbnail-auditor`):** Launch `thumbnail-auditor` in `PRE_GENERATION` mode. Fix any TV 50%, standalone Question/Emotion, clutter, or title-overlap error before generating any pixels.

## Stage 2 — AFTER Thumbnail Generation (`POST_GENERATION`)
1. **Generate 2–3 distinct thumbnails** (varying one major visual/emotional lever + A/B text variants).
2. **Deterministic Diagnostic Strip:**
   ```bash
   python3 skills/yt-thumbnail-brief/scripts/audit_thumbnail.py \
     --thumb path/to/thumb.png \
     --title "Exact Title" \
     --thumb-text "LEAD WORDS" \
     --out-dir ./qc/thumb
   ```
3. **Subagent Gate (`thumbnail-auditor`):** Launch `thumbnail-auditor` in `POST_GENERATION` mode inspecting the raw thumbnail, any facial reference, and `_thumbnail_diagnostic_sheet.jpg`. Confirm `TV 50%`, `120px luma_std >= 42.0`, `Standalone No-Title`, `Zero Clutter`, `Obvious Hero`, and authentic likeness.

## Stage 3 — BEFORE Video Rendering (`PRE_RENDER`)
1. **Run `youtube-screenwriter` + `youtube-director-dp`:** Write full script with `[ON SCREEN: ...]` cues every `2.0–3.5s` and assemble `planned_edl.json` (plus AI video prompts if used).
2. **Deterministic Pre-Script & Pre-EDL Audit:**
   ```bash
   python3 skills/yt-script/hookscore.py --title "Exact Title" --hook "Opening 20s..."
   python3 skills/youtube-retention-engine/scripts/audit_retention_architecture.py \
     --transcript script.md \
     --edl planned_edl.json \
     --thumb approved_thumb.png \
     --title "Exact Title" \
     --thumb-text "LEAD WORDS"
   ```
3. **Subagent Gate (`retention-auditor`):** Launch `retention-auditor` in `PRE_RENDER` mode. Verify:
   - `0:00–0:05`: Sentence 1 echoes Title; Frame 1 mirrors Thumbnail; voice clarifies Thumbnail meaning.
   - `0:00–0:20`: Context + Stakes/Payoff + Curiosity Gap + visible Input Bias + `8+` planned shifts + Body launch **`<= 0:20`**.
   - Body: No planned shot `>= 10s`, zero adjacent same-room/same-template loops, zero random `NY -> Chicago` jumps (real OR AI-generated), `2–4 min` High->Low energy cycles, final-20% emotional depth, high-note payoff close.

## Stage 4 — AFTER Video Rendering (`POST_RENDER`)
1. **Render & Assemble (`youtube-editor-sound`):** Strip dead air (`deadair.py --floor 0.35`), master `-14.5..-16.0 LUFS` / `<= -1.0 dBTP`, add chapters (`chapters.py`).
2. **Run Deterministic Full-Video Audits:**
   ```bash
   python3 skills/youtube-retention-engine/scripts/audit_retention_architecture.py \
     --video master.mp4 --thumb approved_thumb.png \
     --title "Exact Title" --thumb-text "LEAD WORDS" \
     --transcript script_or_subs.txt --out-dir ./qc

   python3 skills/mrbeast-10x-viral-video/scripts/audit_mrbeast_video.py \
     --video master.mp4 --thumb approved_thumb.png \
     --title "Exact Title" --thumb-text "LEAD WORDS" \
     --transcript script_or_subs.txt
   ```
3. **Run All 4 Independent Critics & Judges:**
   - **`visual-supervisor-judge`:** `inspect_chapter.py` -> `run_multimodal_supervisor.py` -> `run_full_film_supervisor.py` -> `verify_supervisor_gate.py` (`CRITICAL == 0`).
   - **`retention-auditor` (`POST_RENDER`):** Audits all 13 gates on rendered MP4 + `_retention_hook_sheet.jpg` & `_retention_body_sheet.jpg` + **10-Blunt-Friends Roast**.
   - **`viewer-panel-critic`:** Simulates 10–24 target viewers to detect drop-off timestamps & annoyances.
   - **`santa-release-judge`:** Runs two isolated final reviewers (`PASS` / `PASS`) before upload.
