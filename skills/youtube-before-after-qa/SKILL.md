---
name: youtube-before-after-qa
description: "Unified BEFORE-and-AFTER YouTube quality gate orchestrating every thumbnail, packaging, hook, script, AI-video, and retention rule from KE4zqD0ONDI, 5zu8s38ZwtQ, and I4nd9t84UvI. Enforces 4 sequential gates: (1) BEFORE thumbnail generation (brief + title + TV 50% + Q&E + 3+ A/B texts), (2) AFTER thumbnail generation (diagnostic sheet + thumbnail-auditor), (3) BEFORE video rendering (hookscore + pre-script + EDL + AI prompts via retention-auditor PRE_RENDER), and (4) AFTER video rendering (audit_retention_architecture.py + audit_mrbeast_video.py + visual-supervisor-judge + retention-auditor POST_RENDER 10-critic roast + viewer-panel-critic + santa-release-judge). Trigger on ANY YouTube video or thumbnail creation, scripting, AI video planning, or review."
---

# YouTube Before & After QA Gatekeeper (ДО и ПОСЛЕ)

Never generate a thumbnail, render a video, or deliver a YouTube cut without running **BOTH** the **BEFORE (`PRE`)** and **AFTER (`POST`)** gates across our skills, deterministic scripts, and independent subagents.

---

## Stage 1 — BEFORE Thumbnail Generation (`ДО генерации обложки`)

1. **Titles (`yt-package` + `yt-title-optimizer`):** Draft 10 titles and score via:
   ```bash
   python3 ~/.claude/skills/yt-package/title.py titles.txt
   ```
2. **Thumbnail Brief (`yt-thumbnail-brief`):** Draft brief (`references/brief-template.md`) covering:
   - **TV 50% Top-Half Plan** (hero eyes/subject + hook words survive bottom-50% crop on TV UI)
   - **Standalone Psychology** (explicit *Questions* + *Emotions* triggered even with Title hidden)
   - **5-Source Reference Mechanism** (Outliers / Model 3 / Bookmarks / Off-Platform -> exact HOW)
   - **Zero Clutter & Obvious Main Character** isolation plan
   - **3+ A/B Text Variants** (`1–4` words each, `0%` Title word overlap)
3. **Deterministic Pre-Brief Gate:**
   ```bash
   python3 ~/.claude/skills/yt-thumbnail-brief/scripts/audit_thumbnail.py \
     --brief path/to/thumbnail_brief.md \
     --title "Lead Video Title" \
     --ab-texts "VARIANT ONE" "VARIANT TWO" "VARIANT THREE"
   ```
4. **Agent Gate (`PRE_GENERATION`):** Launch `subagent(agent="thumbnail-auditor", ...)` in `PRE_GENERATION` mode. Do **not** generate pixels until `PASS`.

---

## Stage 2 — AFTER Thumbnail Generation (`ПОСЛЕ генерации обложки`)

1. **Deterministic Pixel & TV-50% / 120px Diagnostic:**
   ```bash
   python3 ~/.claude/skills/yt-thumbnail-brief/scripts/audit_thumbnail.py \
     --thumb path/to/thumbnail.png \
     --title "Lead Video Title" \
     --thumb-text "LEAD WORDS" \
     --out-dir path/to/qc_dir
   ```
2. **Agent Gate (`POST_GENERATION`):** Launch `subagent(agent="thumbnail-auditor", ...)` in `POST_GENERATION` mode to visually inspect the raw thumbnail, any facial reference, and `_thumbnail_diagnostic_sheet.jpg` (`Full` | `TV 50% Mask` | `120px Mobile` | `No-Title`). Loop edits until `PASS`.

---

## Stage 3 — BEFORE Video Generation / Rendering (`ДО генерации и рендера видео`)

Run BEFORE synthesizing TTS, generating AI video clips, or rendering timelines:
1. **Hook & Script Rules (`yt-hook-scripter` + `yt-script` + `youtube-retention-engine`):**
   - `0:00–0:05`: Sentence 1 matches Title; Frame 1 mirrors approved Thumbnail; voice clarifies Thumbnail meaning immediately; zero greetings/logos.
   - `0:00–0:20`: Context + Stakes/Payoff + Curiosity Gap + **Match->Exceed Expectations (Input Bias effort proof)** + `>= 8` planned `[ON SCREEN]` visual shifts + Body Launch **`<= 0:20`**.
   - Body (`0:20 -> End`): Context-driven visual shifts every `2.4–5s` (no `>=10s` holds, no boring same-room/same-template loops, no random `NY -> Chicago` location jumps — strictly audit AI video prompts too!), Continuous Contrast, `2–4 min` High->Low energy cycles (faster upfront, emotional depth in final `20%`), High-Note Payoff End.
2. **Deterministic Pre-Script & Pre-EDL Audit:**
   ```bash
   python3 ~/.claude/skills/yt-script/hookscore.py --title "Lead Video Title" --hook "..."
   python3 ~/.config/opencode/skills/youtube-retention-engine/scripts/audit_retention_architecture.py \
     --transcript path/to/script.md \
     --edl path/to/planned_edl.json \
     --thumb path/to/thumbnail.png \
     --title "Lead Video Title" \
     --thumb-text "LEAD WORDS"
   ```
3. **Agent Gate (`PRE_RENDER`):** Launch `subagent(agent="retention-auditor", ...)` in `PRE_RENDER` mode to audit the Title + Approved Thumbnail + Full Script + Planned EDL + AI Video Prompts. Fix every leak BEFORE rendering.

---

## Stage 4 — AFTER Video Rendering (`ПОСЛЕ рендера видео`)

1. **Deterministic Full-Video Audits:**
   ```bash
   python3 ~/.config/opencode/skills/youtube-retention-engine/scripts/audit_retention_architecture.py \
     --video path/to/master.mp4 \
     --thumb path/to/thumbnail.png \
     --title "Lead Video Title" \
     --thumb-text "LEAD WORDS" \
     --transcript path/to/script_or_srt.txt \
     --out-dir path/to/qc_dir

   python3 ~/.config/opencode/skills/mrbeast-10x-viral-video/scripts/audit_mrbeast_video.py \
     --video path/to/master.mp4 \
     --thumb path/to/thumbnail.png \
     --title "Lead Video Title" \
     --thumb-text "LEAD WORDS" \
     --transcript path/to/script_or_srt.txt
   ```
2. **Multimodal Director Supervision (`visual-supervisor-judge`):** Run `visual-supervisor-judge` (`inspect_chapter.py` + `run_multimodal_supervisor.py` on independent `gemini-3.1-pro-preview` + `verify_supervisor_gate.py`).
3. **Target Audience Panel & Final Release Arbiter:** Run `viewer-panel-critic` (10–24 simulated viewers) and `santa-release-judge` (dual adversarial verification) before upload.
3. **Agent Gate (`POST_RENDER` + 10-Critic Roast):** Launch `subagent(agent="retention-auditor", ...)` in `POST_RENDER` mode to inspect `_retention_hook_sheet.jpg`, `_retention_body_sheet.jpg`, and telemetry across all 13 gates + perform the **10-Blunt-Friends Roast** (`BORED / CONFUSED / HIGH_EFFORT / SAME_ROOM / RANDOM_JUMP`). Cut or re-edit every flagged drag before final delivery.
