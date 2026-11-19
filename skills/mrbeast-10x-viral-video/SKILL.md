---
name: mrbeast-10x-viral-video
description: "Master protocol distilled from MrBeast's YouTube methodology (I4nd9t84UvI & Aprilynne Alter 5zu8s38ZwtQ) for viral YouTube Long-form videos and Shorts: 0-5s Title/Thumbnail Lock, 0-20s 3-element hook (Context + Stakes/Payoff + Curiosity Gap) + Input Bias effort signal + <=20s body launch + >=8 visual shifts/20s, context-driven visual variety (anti-same-room & anti-random NY->Chicago jumps for real and AI video), continuous contrast, 2-4 min energy cycling, high-note payoff endings, and dull/confusion roast audits. Always use whenever planning, scripting, designing thumbnails, editing, or auditing any YouTube video or Short."
---

# MrBeast 10x Viral Video & 70%+ Retention Engine (`I4nd9t84UvI` + `5zu8s38ZwtQ`)

Distilled from empirical frame-by-frame & transcript teardowns of both:
1. **`I4nd9t84UvI`** (*MrBeast Best Advice*, `475s`, `133` shots, `2.52s` median cut, `2.36s` opening 60s median)
2. **`5zu8s38ZwtQ`** (*How MrBeast Solved YouTube Retention* by Aprilynne Alter, `850s`, `18` visual shifts in `0–20s`, `469` total shifts, `70%+` retention framework)

## Companion Skills & Mandatory Verifier Agent

Chain this skill with:
1. **`youtube-retention-engine`** & **`retention-auditor` (`subagent`)** — Dedicated retention framework + adversarial verifier enforcing all 13 retention gates.
2. **`yt-package`** (`~/.claude/skills/yt-package/title.py`) & **`yt-title-optimizer`** — Score 10 title candidates + mobile cutoff.
3. **`yt-thumbnail-brief`** — Structure the 120-pixel shrink test and title/thumbnail information split.
4. **`yt-hook-scripter`** & **`yt-script`** (`~/.claude/skills/yt-script/hookscore.py`) & **`viral-hooks`** — Score 5 hooks before locking `0:00–0:20`.
5. **`yt-retention`** & **`yt-edit`** (`~/.claude/skills/yt-edit/deadair.py`) — Strip pauses >0.35s and inspect retention cliffs.

---

## Core Law 1: The 10000% Provocative Preview & `0:00–0:05` Expectation Lock

> *"Your title and thumbnail set expectations, and at the very beginning of the video to minimize drop-off, you want to assure them that those expectations are being met."* — `5zu8s38ZwtQ` (`00:32–00:46`)

1. **120-Pixel Mobile Dominance & Extreme Contrast:** 1 focal subject (`45–65%` frame), high luminance/chroma separation (`luma_std >= 42.0`), **2–4 massive impact words** with **0% word overlap** against the Title.
2. **TV 50% Top-Half Test (`KE4zqD0ONDI` Rule 1):** Because TV has surpassed mobile and TV UI hides the bottom half until scrolling down, keep the primary face/hero and hook text in the **top 50% / top third** (`tv_top50_luma_std >= 28`, `top50_edge_share >= 0.30`).
3. **Standalone Questions + Emotions (Don't Rely on Title):** Thumbnails are growing while titles shrink. Design *psychology-first* (*"What do I want the viewer to WONDER and FEEL?"*) using **10–15 references across 5 sources** (*Internal Outliers, External Outliers, Model 3 Channels, Bookmarks, Off-Platform*) so the thumbnail compels clicks even with the title hidden.
4. **3 Thumbnail Quick Fixes (`KE4zqD0ONDI`):** **Remove Clutter** (cut anything not working for you), **Make Main Character Obvious** (color/rim/crop isolation in `<0.2s`), and **A/B Test 3+ Text Variants** for Test & Compare.
5. **Double the Stakes in the Title (`$5,000 -> $10,000`):** Anchor with the highest honest number, conflict, or consequence in the first 45 characters.
6. **The `0:00–0:05` 2-Step Match Formula (Mandatory Frame-1 & Line-1 Lock):**
   - **First Sentence Matches Title (`0:00–0:05`):** Verbally state/confirm what is written in the title immediately. Zero "Welcome back", zero logo sting, zero throat-clearing.
   - **First Shot Matches Thumbnail (`0:00–0:03`):** Frame 1 visually mirrors the thumbnail's subject, setting, emotion, and primary color palette.
   - **Immediate Thumbnail Clarification (`0:02–0:08`):** Within seconds, narration + on-screen context clarifies the exact meaning of the thumbnail visual/text so viewers feel instant payoff alignment.

---

## Core Law 2: `0:00–0:20` Hook Architecture, Input Bias & 10x Escalation

The steepest viewer loss happens inside the **first 20 seconds (`Hook`)**. Inside `0:00–0:20`, deliver ALL of the following and **start the Video Body NO LATER than `0:20`** (`0:12–0:18` target):

1. **The 3 Core Hook Elements (`0:00–0:20`):**
   - **Context (from Title):** Give the exact setup required for the premise to make sense.
   - **Reward / Stakes / Payoff (matching Title):** Make clear why they should care and what prize/discovery/consequence is on the line.
   - **Curiosity Gap ("Open Loop"):** Withhold the ultimate answer/climax so viewers *need* the ending (e.g., teasing the unresolved outcome or flashing a blurred roadmap).
2. **Match Expectations -> THEN Exceed Them (`Input Bias`):**
   - *"Match the expectations, and then you want to exceed them... blow their mind and be like, 'What? You're also getting even more!'"* (`5zu8s38ZwtQ`, `03:35`)
   - *"Viewers aren't stupid. They can tell when you half-ass a video or if you really put in effort."* (`03:57`)
   - **Trigger Input Bias from Second 0:** Humans value output proportionally to perceived effort/time/cost (valuing a $50 wine over an identical $20 wine). Prove immense work immediately in `0:00–0:20` via real research depth (`"I spent a week studying..."`), primary receipts, high-craft motion graphics, and production scale.
3. **Dynamic Opening Shots (`>= 8` Visual Shifts in `0:00–0:20`):**
   - Change shots, camera scale, or visual proof **`8+` times in the first 20 seconds** (`~2.0–2.5s` cadence).
4. **The 10x Escalation Ladder (`0:20` -> Finale):**
   - `0:00–0:05` (**1x Preview Payoff**) -> `0:05–0:20` (**2x Hook Turn & Body Launch**) -> `25%–75%` (**5x Escalation** with higher stakes each act) -> `75%–95%` (**10x Grand Finale**).

---

## Core Law 3: Video Body — Visual Variety, Continuous Contrast & Energy Cycling

> *"If I just talk to a camera for 10 seconds without a cut, a lot of people will just get bored or lose interest."* — `5zu8s38ZwtQ` (`07:22`)

1. **Context-Driven Visual Variety (`3–5s` max; `8` shots in `20s` benchmark):**
   - Why Reels hook viewers for hours: visual novelty every ~2–5 seconds. Never hold a static talking head or static graphic `>= 10s` (target `2.0–3.5s` median, `< 5.0s` max hold).
   - **NO Boring Same-Room / Same-Template Cuts:** Never cut repeatedly inside the exact same camera setup/room/template card every 5s. Shift scale (Extreme Wide -> Medium -> Close-Up -> Low Angle), camera angle, environment, or visual medium (footage <-> diagram <-> primary document).
   - **NO Disconnected Random Location Jumps (`NY -> Chicago` Rule):** Never splice random unrelated cities/scenes (New York -> Chicago 5s later) just to simulate motion. **Every single shot change—including AI-generated video—must serve the exact spoken context at that timestamp.**
2. **Continuous Contrast (*Consistent Contrast*):**
   - Never hold one uniform tone or visual surface across 10–15 minutes. Alternate intensity vs levity/human relief (e.g., cliff trek vs base-camp "Operation Hole"), dark vs light palettes, archival reality vs 2D math vs tight human emotion.
3. **Good Pacing (`2–4 Minute Energy Cycles` — Kill the Middle Valley):**
   - Replace the declining "middle valley" with **repeating 2–4 minute High-Energy -> Low-Energy cycles** (exciting reset/new tier -> deeper exploration -> exciting reset).
   - Put **shorter, faster cycles upfront**; reserve **longer cycles and slower, emotional/serious beats for the final 20%**.

---

## Core Law 4: Video End (`2-Part High-Note`) & Post-Production Roast

1. **Video End Equation (`Last 5–10%`):**
   - **Reveal the Big Payoff** + **End on a High Note** (dramatic, wholesome, or memorable) -> zero "thanks for watching" drop-off; bridge straight to the next mystery.
2. **Post-Production Ruthless Cut (`13:36–14:10`):**
   - Have blunt critics / `retention-auditor` roast the cut for **every second viewers get bored, confused, or have to exert effort to follow**—then **cut or rework those exact moments completely**.

---

## Automated Gate Audit (`audit_mrbeast_video.py` + `retention-auditor`)

Run BOTH:
```bash
python3 ~/.config/opencode/skills/mrbeast-10x-viral-video/scripts/audit_mrbeast_video.py \
  --video path/to/rendered.mp4 \
  --thumb path/to/thumbnail.jpg \
  --title "Your Video Title" \
  --thumb-text "THUMBNAIL WORDS" \
  --transcript path/to/script_or_transcript.txt
```
AND launch `subagent(agent="retention-auditor", ...)` before delivery. Do not ship until `MRBEAST_10X_GATE_PASSED` and `retention-auditor` returns `PASS`.

## Reference Files
- [references/mrbeast_video_breakdown.md](references/mrbeast_video_breakdown.md) — Complete breakdown of `I4nd9t84UvI`.
- [references/aprilynne_5zu8s38ZwtQ_retention_playbook.md](references/aprilynne_5zu8s38ZwtQ_retention_playbook.md) — Empirical breakdown & Cheat Sheet of `5zu8s38ZwtQ`.
- [references/KE4zqD0ONDI_thumbnail_playbook.md](references/KE4zqD0ONDI_thumbnail_playbook.md) — Empirical thumbnail breakdown & Cheat Sheet of `KE4zqD0ONDI`.
