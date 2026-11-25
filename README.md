# Apex YouTube Studio

> **Universal AI Film Studio OS for YouTube Creators & Documentary Teams.**  
> **10 Specialized Agents** (Producer, Screenwriter, Director/DP, Editor/Sound, Thumbnail Auditor, Retention Auditor, Visual Supervisor Judge, 24-Viewer Panel, Santa Release Judge, Behavioral Psychology Strategist) + **32 Modular Skills** + **Deterministic Python QA Scripts** enforcing **BEFORE & AFTER** gates on every thumbnail and every second of video.

**Language:** English (Primary) · [Русская документация (`docs/README.ru.md`)](docs/README.ru.md)  
**Author:** Artur Harutyunyan — [LinkedIn](https://www.linkedin.com/in/artur-harutyunyan-a09a3111a/) · [GitHub](https://github.com/harutyunian/apex-youtube-studio)

Works across **any niche** (Finance, Business, Tech, History, True Crime, Science, Storytelling, Education, Shorts, Talking Head, or AI-assisted documentaries) and plugs directly into **OpenCode**, **Claude Code**, or **Antigravity** in one command.

---

## Why This Exists

Most AI video workflows fail for the same five reasons:
1. **Unverified Thumbnails:** Text sits in the bottom half (hidden on YouTube TV rows), repeats the title, fails at `120px` mobile size, or looks irrelevant without reading the title.
2. **Dead `0:00–0:20` Hooks:** Intros open with greetings or take 35 seconds to get to the point—while the steepest retention drop happens in the first 20 seconds.
3. **10-Second Static Fatigue & Fake Cuts:** Repeating the same template/room every 5s or jumping randomly (`New York -> Chicago`) disconnected from the narration.
4. **No Middle Energy Cycles:** High hook -> sagging middle valley -> flat farewell cliff.
5. **Zero Pre-Render & Post-Render Gates:** Teams render hours of audio, AI video, or timelines before discovering basic retention or packaging leaks.

**Apex YouTube Studio** fixes this by turning empirical high-retention methodologies (`I4nd9t84UvI`, `5zu8s38ZwtQ`, `KE4zqD0ONDI`) into **executable BEFORE & AFTER gates** across packaging, scripting, directing, editing, multimodal judging, and simulated audience panels.

---

## The 4-Stage BEFORE & AFTER Pipeline

```text
┌──────────────────────────────────────────────────────────────────────────────┐
│ STAGE 1 — BEFORE THUMBNAIL (PRE_GENERATION)                                 │
│  title.py + yt-thumbnail-brief + audit_thumbnail.py --brief                  │
│  -> thumbnail-auditor (PRE_GENERATION) checks TV 50% plan, Q+E, A/B texts    │
└──────────────────────────────────┬───────────────────────────────────────────┘
                                   ▼ PASS
┌──────────────────────────────────────────────────────────────────────────────┐
│ STAGE 2 — AFTER THUMBNAIL (POST_GENERATION)                                  │
│  audit_thumbnail.py --thumb --out-dir  (generates 4-panel diagnostic sheet)  │
│  -> thumbnail-auditor (POST_GENERATION) inspects TV 50%, 120px, Clutter, Hero│
└──────────────────────────────────┬───────────────────────────────────────────┘
                                   ▼ PASS
┌──────────────────────────────────────────────────────────────────────────────┐
│ STAGE 3 — BEFORE VIDEO RENDER (PRE_RENDER)                                   │
│  hookscore.py --title + audit_retention_architecture.py --transcript --edl   │
│  -> retention-auditor (PRE_RENDER) audits 0-5s, 0-20s, Input Bias, AI prompts│
└──────────────────────────────────┬───────────────────────────────────────────┘
                                   ▼ PASS
┌──────────────────────────────────────────────────────────────────────────────┐
│ STAGE 4 — AFTER VIDEO RENDER (POST_RENDER)                                   │
│  audit_retention_architecture.py --video + audit_mrbeast_video.py            │
│  -> visual-supervisor-judge (15-pt Multimodal MP4 + START/MID/END Sheets)    │
│  -> retention-auditor (POST_RENDER + 10-Blunt-Friends Dull/Confusion Roast)  │
│  -> viewer-panel-critic (10-24 Simulated Target Viewers Focus Group)         │
│  -> santa-release-judge (Dual Independent Adversarial Pre-Upload Sign-Off)   │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## Core Retention & Packaging Laws Built In

### Thumbnail Laws (`KE4zqD0ONDI` + `I4nd9t84UvI`)
- **TV 50% Top-Half Test:** Keep primary focal eyes/hero and hook text in the upper 50% / top third so TV UI doesn't slice them off before the viewer presses Down.
- **Standalone No-Title Test:** Thumbnails grow larger while title fonts shrink—your image alone must spark **Questions + Emotions** without relying on the title.
- **5-Source Reference Mechanism:** Pull 10–15 references (*Internal Outliers, External Outliers, Model 3 cross-niche channels, Bookmarks, Off-Platform*) and transfer *how* they trigger curiosity/emotion.
- **3 Quick Fixes:** Remove clutter, make the main character unmistakable (`<0.2s` at `120px` feed scale, `luma_std >= 42.0`), and test **3+ A/B text variants** (`1–4` words, `0%` overlap with Title).

### Hook, Body & Ending Laws (`5zu8s38ZwtQ` + `I4nd9t84UvI`)
- **First 5 Seconds (`0:00–0:05`):** First spoken sentence echoes the **Title**; Frame 1 visually mirrors the **Thumbnail**; narration clarifies thumbnail meaning immediately. Zero greetings or logo stings.
- **First 20 Seconds (`0:00–0:20`):** Deliver **Context + Stakes/Payoff + Curiosity Gap**, match expectations then **exceed them** via visible **Input Bias** (research depth, sources, high-craft montage), hit **`>= 8` dynamic visual changes in `20s`**, and launch the **Video Body `<= 0:20`**.
- **Video Body (`0:20 -> End`):**
  - **Context-Driven Visual Variety (`2–5s`):** Never leave a static frame or talking head `>= 10s`. Ban boring same-room/same-template cuts AND ban random disconnected location jumps (`New York -> Chicago`)—every real, graphic, and **AI-generated video clip** must advance the exact spoken sentence.
  - **Continuous Contrast:** Alternate tone, scale (`Wide -> Medium -> Close-Up`), tension vs levity, and visual surfaces.
  - **2–4 Min Energy Cycling:** Shorter/faster High->Low cycles upfront; reserve slower, heavy emotional beats for the **final 20%**.
- **Video End & Post-Production Roast:** Big Payoff + High Note (dramatic/wholesome/memorable) with zero farewell cliff, followed by ruthless cuts wherever viewers feel **bored**, **confused**, or forced to exert **high effort** to follow.

---

## Full Crew Roster (`agents/`)

| Agent | Role | Phase | What It Does |
|---|---|---|---|
| **`youtube-producer`** | Producer & Packaging | Pre-Prod | Outlier research, 10x Escalation Arc, Title+Thumb pairing, brief creation |
| **`youtube-screenwriter`** | Retention Screenwriter | Pre-Prod | Scripts `0–5s` lock, `0–20s` hook + Input Bias, `2–4m` energy cycles, high-note close |
| **`youtube-director-dp`** | Director & Cinematographer | Pre-Prod | Visual Worlds, `2.5s` scale/angle progression, contrast, AI-video context lock |
| **`youtube-editor-sound`** | Editor & Sound Designer | Production | HyperFrames/FFmpeg timeline assembly, `deadair.py`, `-15.2 LUFS` mix, SFX, chapters |
| **`thumbnail-auditor`** | Thumbnail Critic & Judge | **BEFORE & AFTER** | `PRE_GENERATION` brief gate + `POST_GENERATION` TV 50% / 120px / clutter / hero gate |
| **`retention-auditor`** | Retention & Hook Judge | **BEFORE & AFTER** | `PRE_RENDER` script/EDL/AI prompt gate + `POST_RENDER` 13-gate & 10-critic roast |
| **`visual-supervisor-judge`** | Multimodal Director Judge | **AFTER** | Uploads MP4 proxy + `START/MID/END` contact sheets to independent Gemini (`15-pt` rubric) |
| **`viewer-panel-critic`** | Target Audience Panel | **AFTER** | Simulates 10–24 realistic target viewers scoring drop-off timestamps & annoyances |
| **`santa-release-judge`** | Dual Release Arbiter | **FINAL GATE** | Runs two isolated adversarial reviewers (`santa-method`) before upload |
| **`behavioral-psychology-strategist`** | Behavioral Click & Neuro-Retention | **PRE & POST** | Audits CCN, 12 click mechanisms, 12 neuro-retention mechanics, voice coupling, Studio curves & `1+3` Shorts |

---

## Bundled Skills & CLI Scripts (`skills/`)

<details>
<summary><strong>Click to expand all 32 Skills & Executable Python Scripts</strong></summary>

| Skill | Purpose | Included Scripts |
|---|---|---|
| `youtube-before-after-qa` | Master 4-Stage BEFORE & AFTER orchestrator | — |
| `yt-click-psychology` | 12 behavioral CTR mechanisms, CCN matrix, Test & Compare & traffic benchmarks | — |
| `yt-neuro-retention` | 12 neuro-retention mechanics, ABT/McKee/Ovsiankina, curve diagnostics & `1+3` Shorts | — |
| `youtube-retention-engine` | Full `5zu8s38ZwtQ` retention rules (`PRE` + `POST`) | `scripts/audit_retention_architecture.py` |
| `mrbeast-10x-viral-video` | 10x escalation & cadence audit | `scripts/audit_mrbeast_video.py` |
| `yt-thumbnail-brief` | `KE4zqD0ONDI` packaging brief + TV 50% / 120px checks | `scripts/audit_thumbnail.py` |
| `yt-package` | Title + Thumbnail unit pairing & truncation check | `title.py` |
| `yt-title-optimizer` | High-CTR 2026 title formulas & checklists | — |
| `yt-hook-scripter` | `0–5s` + `0–20s` & Shorts 3s opening beats | — |
| `yt-script` | 21 hook formulas, `--title` lock & Input Bias scorer | `hookscore.py` |
| `viral-hooks` | 100 stop-scroll hook templates across 10 triggers | — |
| `longform-doc-pipeline` | Universal long-form documentary/essay crew pipeline | — |
| `visual-supervisor-judge` | 15-point multimodal director judge (`inspect` -> `verify`) | `inspect_chapter.py`, `run_multimodal_supervisor.py`, `run_full_film_supervisor.py`, `verify_supervisor_gate.py` |
| `santa-method` | Dual independent adversarial review framework | — |
| `yt-edit` | Transcript gap, filler & retake EDL builder | `deadair.py` |
| `yt-retention` | YouTube Studio audience-retention CSV leak analyzer | `retention.py` |
| `yt-chapters` | Auto-generated rule-compliant YouTube chapters | `chapters.py` |
| `yt-seo` | Search-focused descriptions & disambiguation tags | — |
| `yt-viral` | Channel outlier multiple scorer (`views / median`) | `swipe.py` |
| `yt-audit` | Channel-wide packaging & hook audit | — |
| `yt-plan` | Sustainable upload calendar planner | — |
| `yt-shorts` | Extract self-contained Shorts from long videos | — |
| `yt-comment` | Creator-voice comment triage & replies | — |
| `hyperframes`, `hyperframes-cli` & `hyperframes-registry` | HTML/GSAP/SVG -> deterministic 1080p MP4 engine + 450+ blocks | `scripts/*` |
| `reverse-any-video` & `style-sampling` | Recreate reference video styles or reverse-engineer motion frame-by-frame | `scripts/*` |
| `remotion-to-hyperframes` & `figma` | Port Remotion/Lottie/Three.js/Manim or import Figma tokens/frames into motion | `scripts/*` |
| `media-use` | Audio mixing, LUFS, voiceover, cutouts & color tools | `scripts/*` |
| `video-editing` | FFmpeg / Remotion / AI-assisted video workflows | — |

</details>

---

## Quick Start & Installation

### 1. Prerequisites
- **Python 3.10+** (`pip install -r requirements.txt`)
- **FFmpeg & FFprobe** (`brew install ffmpeg` on macOS / `apt install ffmpeg` on Linux)
- **OpenCode**, **Claude Code**, or **Antigravity** (optional: Node.js `>= 18` for HyperFrames HTML-to-Video rendering)
- Copy `.env.example` to `.env` and set `GEMINI_API_KEY` (for multimodal supervision & image/audio generation)

### 2. Install Agents & Skills

```bash
# Option A: Install skills directly via the open Agent Skills CLI (skills.sh)
npx skills add harutyunian/apex-youtube-studio

# Option B: Full install (all 10 subagents + 32 skills + channel templates)
git clone https://github.com/harutyunian/apex-youtube-studio.git
cd apex-youtube-studio
pip install -r requirements.txt

# Install globally for OpenCode (~/.config/opencode/)
./install.sh --opencode

# OR install globally for Claude Code (~/.claude/)
./install.sh --claude

# OR install globally for Antigravity (~/.gemini/config/)
./install.sh --antigravity

# OR install into OpenCode + Claude Code + Antigravity
./install.sh --all

# OR bootstrap a brand-new YouTube channel repository with all templates
./install.sh --project /path/to/my-youtube-channel
```

### 3. Run Standalone CLI Audits Anytime

```bash
# 1. BEFORE generating thumbnail: verify brief + TV 50% plan + 3+ A/B texts
python3 skills/yt-thumbnail-brief/scripts/audit_thumbnail.py \
  --brief path/to/thumbnail_brief.md \
  --title "Your Video Title" \
  --ab-texts "TEXT ONE" "TEXT TWO" "TEXT THREE"

# 2. AFTER generating thumbnail: check 120px mobile, TV 50%, clutter & build 4-panel sheet
python3 skills/yt-thumbnail-brief/scripts/audit_thumbnail.py \
  --thumb path/to/thumbnail.png \
  --title "Your Video Title" \
  --thumb-text "TEXT ONE" \
  --out-dir ./qc

# 3. BEFORE rendering video: audit script + planned EDL + hook alignment
python3 skills/yt-script/hookscore.py --title "Your Video Title" --hook "Your opening hook..."
python3 skills/youtube-retention-engine/scripts/audit_retention_architecture.py \
  --transcript path/to/script.md \
  --edl path/to/planned_edl.json \
  --thumb path/to/thumbnail.png \
  --title "Your Video Title" \
  --thumb-text "TEXT ONE"

# 4. AFTER rendering MP4: audit full retention, cadence, silence & visual supervision
python3 skills/youtube-retention-engine/scripts/audit_retention_architecture.py \
  --video path/to/master.mp4 \
  --thumb path/to/thumbnail.png \
  --title "Your Video Title" \
  --thumb-text "TEXT ONE" \
  --transcript path/to/script_or_subs.txt \
  --out-dir ./qc

python3 skills/mrbeast-10x-viral-video/scripts/audit_mrbeast_video.py \
  --video path/to/master.mp4 \
  --thumb path/to/thumbnail.png \
  --title "Your Video Title" \
  --thumb-text "TEXT ONE" \
  --transcript path/to/script_or_subs.txt
```

---

## Documentation
- **[Russian Documentation (`docs/README.ru.md`)](docs/README.ru.md)**
- **[Behavioral Click Psychology & Neuro-Retention Research Notes (`docs/BEHAVIORAL_PSYCHOLOGY_NOTES.md`)](docs/BEHAVIORAL_PSYCHOLOGY_NOTES.md)**
- **[Step-by-Step 4-Stage BEFORE & AFTER Workflow (`docs/WORKFLOW.md`)](docs/WORKFLOW.md)**
- **[Complete Crew, Critics, Viewers & Judges Guide (`docs/AGENTS_ROSTER.md`)](docs/AGENTS_ROSTER.md)**
- **[Channel Customization Templates (`templates/`)](templates/)**

## Author & License
Created by **Artur Harutyunyan** ([LinkedIn](https://www.linkedin.com/in/artur-harutyunyan-a09a3111a/) · [GitHub](https://github.com/harutyunian/apex-youtube-studio)).  
MIT License — see [LICENSE](LICENSE).
