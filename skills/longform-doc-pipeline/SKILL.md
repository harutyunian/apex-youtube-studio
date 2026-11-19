---
name: longform-doc-pipeline
description: Universal end-to-end pipeline for 8-to-30+ minute high-retention YouTube documentary and video essays in any niche. Orchestrates Producer, Screenwriter, Director/DP, Editor/Sound, multi-world visual systems, HyperFrames/FFmpeg assembly, and mandatory BEFORE-and-AFTER QA gates (thumbnail-auditor, retention-auditor, visual-supervisor-judge, viewer-panel-critic, santa-release-judge).
---

# Universal Long-Form YouTube Documentary & Essay Pipeline

Use this skill alongside **`youtube-before-after-qa`**, **`youtube-retention-engine`**, **`mrbeast-10x-viral-video`**, and **`visual-supervisor-judge`** whenever producing any long-form YouTube documentary, deep-dive essay, or investigative video.

Read your project's `CHANNEL_PROFILE.md` (if present) first to lock channel language, target audience/RPM, runtime window, voice profile, and visual color/typography identity.

## 1. Universal Production Targets
- **Duration:** `>= 480s` (`8:00` min for mid-roll eligibility; check account upload limits e.g. `<= 840s` if under 15-min cap, or `12:00–30:00` for verified channels).
- **Video Format:** `1920x1080` (or `3840x2160`), `30 fps`, horizontal `16:9`.
- **Audio Target:** Consistent expressive narration (`~145–160 WPM`, zero robotic monotone, zero dead air `> 0.35s`), mood-matched music (`-2.5 dB` vocal pocket / sidechain ducking), purposeful SFX punctuation, mastered to `-14.5 to -16.0 LUFS` and `<= -1.0 dBTP`.
- **Policy & Provenance Honesty:** Never pass AI-generated reconstructions off as real archival footage; label synthetic historical scenes honestly (`DRAMATIC RECONSTRUCTION`) and disclose altered/synthetic media in YouTube Studio when applicable.

## 2. Full Crew Workflow (BEFORE & AFTER Gated)

### Stage A — Research & Producer Packaging (`youtube-producer`)
1. **Fact Verification:** Verify every date, dollar figure, quote, and document before writing. Zero invented statistics.
2. **Packaging (`yt-package` + `yt-thumbnail-brief`):**
   - Score 10 title options with `title.py` (`<= 45–60` chars, front-loaded hook).
   - Design thumbnail via `KE4zqD0ONDI` rules (TV 50% Top-Half Test, Standalone Questions+Emotions, 5-Source Reference Mechanism, Zero Clutter, Obvious Hero, 3+ A/B text variants with `0%` Title overlap).
   - **Gate 1 & 2:** Pass `thumbnail-auditor` (`PRE_GENERATION` before pixels -> `POST_GENERATION` after pixels).

### Stage B — Scripting (`youtube-screenwriter`)
1. **0:00–0:05 Lock:** Sentence 1 directly echoes the Title + clarifies Thumbnail meaning; zero greetings or channel logo stings.
2. **0:00–0:20 Hook:** Deliver Context + Stakes/Reward + Curiosity Gap + visible **Input Bias** (research depth/sources/craft) across `8+` visual shifts, launching Act 1 / Point 1 **no later than `0:20`**.
3. **2–4 Min Energy Cycling:** Structure Acts as High-Energy -> Low-Energy cycles (shorter/lighter upfront, deeper emotional weight in final `20%`), planting micro-open-loops every `20–30s`.
4. **High-Note End:** Deliver the Big Payoff + Emotional/Dramatic High Note + urgent bridge to the next video (zero "thanks for watching").

### Stage C — Directing & Editing (`youtube-director-dp` + `youtube-editor-sound`)
1. **Distinct Visual Worlds:** Change color & material worlds across Acts rather than sitting in one static dark/light template for the whole film.
2. **Context-Driven Visual Shifts (`2.4–3.8s`, zero `>= 10s` static holds):** Every shot change (real footage, archival photo, 2D motion graphic, AND AI-generated video) must follow the spoken context and shift scale/angle/surface. **Ban** repetitive same-room/same-template cuts and unmotivated random location jumps (`NY -> Chicago`).
3. **Gate 3 (`PRE_RENDER`):** Run `hookscore.py --title` + `audit_retention_architecture.py --transcript --edl` + **`retention-auditor` (`PRE_RENDER`)** BEFORE rendering TTS, AI video, or final scenes.

### Stage D — Independent Judges, Viewers & Release (`POST_RENDER`)
1. **Visual & Retention Audits:** Run `audit_retention_architecture.py --video`, `audit_mrbeast_video.py`, and `visual-supervisor-judge` (`inspect_chapter.py` -> `run_multimodal_supervisor.py` -> `verify_supervisor_gate.py`).
2. **Subagent Judges & Panel:** Run **`retention-auditor` (`POST_RENDER` + 10-critic roast)**, **`viewer-panel-critic`** (10–24 simulated target viewers scoring hook, polish, authenticity, and drop-off risk), and **`santa-release-judge`** before publishing.
