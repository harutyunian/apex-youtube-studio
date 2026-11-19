# YouTube Studio Agent Operational Gates (`AGENTS.md`)

Read `CHANNEL_PROFILE.md` and `CLAUDE.md` before planning, scripting, generating, or rendering any video or thumbnail.
Auto-load skills: `youtube-before-after-qa`, `youtube-retention-engine`, `mrbeast-10x-viral-video`, `yt-thumbnail-brief`, `yt-package`, `yt-hook-scripter`, `yt-script`, `longform-doc-pipeline`, `visual-supervisor-judge`, `hyperframes`, `media-use`.

## Mandatory 4-Stage BEFORE & AFTER Gates
1. **Stage 1 — BEFORE Thumbnail (`PRE_GENERATION`):** Run `title.py`, `audit_thumbnail.py --brief`, and `subagent(agent="thumbnail-auditor", ...)` BEFORE generating any pixels (`TV 50%` plan, Standalone Questions+Emotions, 5-source mechanism, zero clutter, obvious hero, 3+ A/B texts with 0% Title overlap).
2. **Stage 2 — AFTER Thumbnail (`POST_GENERATION`):** Run `audit_thumbnail.py --thumb --out-dir` and `subagent(agent="thumbnail-auditor", ...)` inspecting the generated `_thumbnail_diagnostic_sheet.jpg` (`120px luma_std >= 42.0`, `TV 50%` legibility, likeness, zero clutter).
3. **Stage 3 — BEFORE Video Render (`PRE_RENDER`):** Run `hookscore.py --title`, `audit_retention_architecture.py --transcript --edl`, and `subagent(agent="retention-auditor", ...)` BEFORE TTS, AI video generation, or rendering (`0–5s` Title/Thumb lock, `0–20s` 3-element + Input Bias hook, `>= 8` hook shifts, body launch `<= 0:20`, zero `>= 10s` holds, zero same-room loops, zero disconnected `NY -> Chicago` AI/location jumps, 2–4m energy cycles).
4. **Stage 4 — AFTER Video Render (`POST_RENDER`):** Run `audit_retention_architecture.py --video`, `audit_mrbeast_video.py`, `visual-supervisor-judge` (`inspect_chapter.py` -> `run_multimodal_supervisor.py` -> `verify_supervisor_gate.py`), `retention-auditor` (`POST_RENDER` + 10-critic roast), `viewer-panel-critic`, and `santa-release-judge` before publishing.
5. **Fact Discipline:** Only verified, source-checked figures, dates, and filings. Never pass synthetic AI scenes off as genuine archival photography.
