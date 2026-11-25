# Complete Crew, Critics, Viewers & Judges Roster (`AGENTS_ROSTER.md`)

All 10 subagents live in `agents/` and work seamlessly across **OpenCode**, **Claude Code**, and **Antigravity**.

---

## Part 1: Production Crew (Builders)

### 1. `youtube-producer` (Producer & Packaging Director)
- **Focus:** Outlier validation, 10x Escalation Arc, Title + Thumbnail unit design, Test & Compare A/B planning.
- **Key Tools:** `swipe.py`, `title.py`, `audit_thumbnail.py --brief`.

### 2. `youtube-screenwriter` (Retention Screenwriter)
- **Focus:** Spoken natural scripting (`0–5s` Title/Thumb lock, `0–20s` 3-element + Input Bias hook, `<= 20s` body transition, `2–4 min` energy cycles, micro-open-loops, final-20% emotional climax, high-note close).
- **Key Tools:** `hookscore.py`, `audit_retention_architecture.py --transcript`.

### 3. `youtube-director-dp` (Director & Cinematographer / Operator)
- **Focus:** Multi-world visual palette, `2.0–3.5s` shot progression (`Wide -> Medium -> Close-Up -> Angle`), Continuous Contrast, honest provenance (`DRAMATIC RECONSTRUCTION`), strict AI-video context lock (bans same-room loops and disconnected `NY -> Chicago` jumps).
- **Key Tools:** `planned_edl.json`, `audit_retention_architecture.py --edl`.

### 4. `youtube-editor-sound` (Editor & Sound Designer)
- **Focus:** HyperFrames/FFmpeg timeline cutting, `0` blank frames, `<= 0.35s` dead-air removal, `-14.5..-16.0 LUFS` mastering, sidechain BGM ducking, SFX accents, YouTube chapters, Shorts extraction, SEO metadata.
- **Key Tools:** `hyperframes`, `deadair.py`, `chapters.py`, `ffmpeg`.

---

## Part 2: Independent Critics, Viewers & Judges (Adversarial QA)

*(All critics & judges have `edit: deny` and default to `gemini-3.1-pro-preview` so they remain strictly independent from the production orchestrator.)*

### 5. `thumbnail-auditor` (BEFORE & AFTER Thumbnail Critic)
- **`PRE_GENERATION`:** Audits brief/prompts before generating pixels.
- **`POST_GENERATION`:** Inspects rendered thumbnail + `_thumbnail_diagnostic_sheet.jpg` (`TV 50% Mask`, `120px Mobile`, `Standalone No-Title`, Clutter, Obvious Hero, Likeness, `0%` Title Overlap, `3+ A/B Texts`).

### 6. `retention-auditor` (BEFORE & AFTER Retention & Hook Judge)
- **`PRE_RENDER`:** Audits Title + Thumbnail + Script + EDL + AI Prompts before rendering.
- **`POST_RENDER`:** Audits rendered MP4 + hook/body contact sheets across all 13 gates + runs the **10-Blunt-Friends Roast** (`BORED / CONFUSED / HIGH_EFFORT / SAME_ROOM / RANDOM_JUMP`).

### 7. `visual-supervisor-judge` (Independent Multimodal Director Judge)
- **Focus:** Evaluates full-motion MP4 chapters + `START | MID | END` contact sheets across 15 Director Criteria & 8 Scoring Axes (`cinematography`, `composition`, `editing`, `visual_consistency`, `historical_accuracy`, `sound`, `storytelling`, `emotional_impact`) with optional `--fact-bible`.

### 8. `viewer-panel-critic` (Simulated 10–24 Diverse Target Viewers)
- **Focus:** Roleplays 12–24 distinct audience archetypes (Mobile Commuter, TV Couch Viewer, Skeptical Domain Pro, Casual Browse Clicker, Gen-Z Fast Scroller, Motion/Design Snob, Audio Listener, Cynical Anti-AI Viewer, etc.) to catch real-world drop-offs and tone clashes before publishing.

### 9. `santa-release-judge` (Dual Adversarial Release Arbiter)
- **Focus:** Two isolated reviewers independently verify facts, telemetry consistency, chapter rules (`00:00`, `>= 3`, `>= 10s`), ad/synthetic compliance, and link hygiene (`PASS` + `PASS` required before upload).

### 10. `behavioral-psychology-strategist` (Behavioral Click & Neuro-Retention Strategist)
- **Focus:** Audits and designs CCN Matrix positioning, all 12 behavioral click mechanisms (`150ms` System 1, Processing Fluency, Von Restorff feed contrast, Loewenstein Info Gap, Gaze Cueing, Closed-Mouth authenticity, Negativity/Loss Aversion, Tribalism `BIRGing`/`Schadenfreude`, High Arousal, Test & Compare), all 12 neuro-retention mechanics (*In Media Res*, Cortisol->Oxytocin, cascading Ovsiankina loops, ABT spine, `45s` dishabituation, `3:00` Re-hook, McKee act polarity, Goal-Gradient chapters, Mayer load, Peak-End bridge, expressive voice/auto-dub risk), Studio curve diagnostics, and the `1+3` Long-to-Shorts pipeline.
- **Key Tools:** `title.py`, `hookscore.py`, `audit_thumbnail.py`, `audit_retention_architecture.py`, `retention.py`.
