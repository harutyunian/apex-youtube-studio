---
name: youtube-retention-engine
description: "Complete YouTube 70%+ retention architecture distilled from empirical analysis of How MrBeast Solved YouTube (Aprilynne Alter 5zu8s38ZwtQ) and I4nd9t84UvI. Enforces 0-5s Title/Thumbnail lock, 0-20s 3-element hook (Context + Stakes/Reward + Curiosity Gap) + Input Bias effort signal + hard <=20s body launch + >=8 dynamic cuts in 20s, context-driven visual variety every 2-5s (anti-same-room & anti-random-location jumps for both real and AI-generated video), continuous contrast, 2-4 min energy cycling (last 20% emotional depth), high-note payoff endings, and post-production 10-critic dull/confusion audits. Use whenever planning, scripting, editing, generating AI video for, or auditing any YouTube long-form or short-form video."
---

# YouTube Retention Engine (`5zu8s38ZwtQ` + `I4nd9t84UvI`)

Retention is won or lost by how fast you verify the click, how visibly you prove your effort, and whether every single cut earns the next 3–5 seconds. The steepest viewer drop-off happens in the **first 20 seconds (The Hook)**.

Always pair this skill with the independent **`retention-auditor`** subagent (`subagent(agent="retention-auditor", ...)`) and **`thumbnail-auditor`** subagent (`subagent(agent="thumbnail-auditor", ...)`) plus `scripts/audit_retention_architecture.py` before considering any thumbnail, script, storyboard, or rendered MP4 finished.

---

## Law 0 (Pre-Click): Packaging & Thumbnail Rules (`KE4zqD0ONDI`)

Before Frame 1 can work, the thumbnail must win the click across TV, Mobile, and Browse without relying on the title:
1. **TV 50% Top-Half Test:** Keep the focal subject and hook text visible in the **top 50% / top third** (`tv_top50_luma_std >= 28.0`, `top50_edge_share >= 0.30`).
2. **Standalone Questions + Emotions (Title Hidden):** Titles are shrinking while thumbnails grow huge—design psychology-first (*"What should the viewer WONDER and FEEL?"*) so the thumbnail creates curiosity & emotion on its own.
3. **5-Source References & Mechanisms:** Collect 10–15 references (*Internal Outliers, External Outliers, Model 3 Channels, Bookmarks, Off-Platform*) and extract *how* they trigger questions/emotions.
4. **3 Quick Fixes:** **Remove Clutter** (strip everything not working for you), **Make Main Character Obvious** (color/contrast/crop separation in `<0.2s`), and **A/B Test 3+ Text Variants** (`<= 4` words, `0%` overlap with Title, `120px luma_std >= 42.0`).

---

## Law 1: The First 5 Seconds — Match Expectations Immediately (`0:00–0:05`)

Your Title and Thumbnail make an implicit contract with the viewer. Any hesitation, channel greeting, or mismatched imagery triggers an instant back-button cliff.

1. **First Spoken Sentence Matches the Title (`0:00–0:05`):**
   - Say and confirm what is written in the title inside the very first 5 seconds—no "welcome back", no logo animation, no throat-clearing.
   - Example: Title *"I Survived 50 Hours In Antarctica"* -> Sentence 1: *"We just landed in Antarctica and we're going to survive the next 50 hours here."*
2. **First Visual Shot Matches the Thumbnail (`0:00–0:03`):**
   - Frame 1 must mirror the Thumbnail's primary focal subject, setting, emotional tension, and dominant color palette.
3. **Clarify the Thumbnail Meaning Immediately (`0:02–0:08`):**
   - Within the opening seconds, the voiceover/speaker and on-screen cues explicitly clarify the exact meaning of the thumbnail visual and overlay words so there is zero ambiguity about what the video delivers.

---

## Law 2: The First 20 Seconds — Hook Architecture & Body Launch (`0:00–0:20`)

The largest retention drop-off happens during the hook (`0:00–0:20`). Hit all 3 core elements + Input Bias + dynamic cuts, and **start the Video Body no later than `0:20`**:

1. **The 3 Core Hook Elements (All inside `0:00–0:20`):**
   - **Context (from the Title):** What does the viewer immediately need to know for the premise/setup to make sense?
   - **Reward / Stakes / Payoff (matching the Title):** Why should they care? What is the prize, `$` stake, discovery, or concrete takeaway they clicked for?
   - **Curiosity Gap ("Open Loop"):** Leave a deliberate informational gap—do NOT resolve the central mystery or reveal all answers upfront. Make them need the ending.
2. **Match Expectations, THEN Exceed Them (Input Bias / Effort Signal):**
   - Confirm right away that they are getting exactly what they clicked for—then blow past expectations (*"and you're also getting even more"*).
   - **Leverage Input Bias from Second 0:** Viewers value a video proportionally to the time, energy, research depth, and craft they *feel* went into it (like valuing a $50 bottle of wine over a $20 bottle). Without a $4M warehouse, trigger Input Bias immediately via:
     - Explicit research/work receipts in narration (*"I spent a week dissecting..."*, primary SEC filings, cross-checked transcripts);
     - High-effort opening visual polish (custom motion graphics, clean animated proof cards, multi-source montage) visible right from `0:00–0:15`.
3. **Dynamic Opening Frame Cadence (`>= 8` Visual Shifts in `0:00–0:20`):**
   - Target **`8+` distinct visual changes across the first 20 seconds** (`~2.0–2.5s` average per shot; zero holds `> 4.0s`).
4. **Hard `0:20` Body Transition Warning:**
   - Start Challenge #1 / Experience #1 / Point #1 **no later than `0:20`** (MrBeast starts at `0:12`–`0:18`). The faster you enter the body, the sooner the retention curve flattens above `70%`.

---

## Law 3: Video Body — The 3 Retention Engines (`0:20` -> `End`)

Why can people watch Reels for hours while dropping off long videos? Constant, meaningful visual evolution. To keep the retention curve flat across 10–15+ minutes:

### 1. Context-Driven Visual Variety (`<= 3–5s`, NEVER `10s` Static)
- Talking to a camera or holding one static template/slide for `10 seconds` guarantees drop-offs. Cut or transform the frame at least every **`3–5 seconds`** (target **`2.0–3.5s`**).
- **Example (`8` shots in `20s` on a simple mountain hike):** Extreme wide aerial -> medium snow plain -> tight front close-up -> side tracking -> low-angle ridge silhouette.
- **Two Hard Anti-Slop Laws (Applies equally to Real Footage, Motion Graphics, AND AI-Generated Video):**
  1. **NO Boring Same-Room / Same-Template Cuts:** Changing camera cut or popping small text every 5s inside the *exact same room, angle, or background card* feels fake and fatiguing. Change shot **scale (Wide -> Medium -> Close-Up)**, **angle**, **environment**, or **visual layer (Footage -> Document -> 2D Diagram -> Archival Cut)**.
  2. **NO Disconnected Random Location Jumps (`NY -> Chicago` Rule):** Never jump from New York to Chicago 5 seconds later purely to force visual motion when the narration doesn't motivate it. **Every single shot change—especially AI-generated video—must directly advance the exact spoken context at that timestamp.**

### 2. Continuous Contrast (*Consistent Contrast*)
- One continuous tone, visual world, or storyline cannot grip viewers for 10–15 minutes straight.
- **Contrast Everything Continuously:**
  - Alternate narrative weight (high-stakes tension <-> human relief/irony/side-angle perspective; e.g., freezing cliff climb <-> base-camp "Operation Hole");
  - Alternate visual textures & luminance (dark nocturnal cinema <-> crisp editorial paper <-> real broadcast video <-> animated vector math <-> tight human reaction).

### 3. Good Pacing (*2–4 Minute Energy Cycles — Kill the Middle Valley*)
- Most videos spike at the hook, sag through a boring "middle valley," and rise only at the finale.
- **Build 2–4 Minute High->Low Energy Cycles:**
  - Open each cycle/act with a **High-Energy Reset** (new tier, surprising twist, bold audio-visual contrast), transition into lower-energy exploration/mechanics, then trigger the next High-Energy Reset.
  - **Front-Load Speed, Back-Load Emotion:** Place **shorter, lighter, faster cycles in the first half** of the video; reserve **longer cycles and slower, heavier emotional weight for the final 20%**.

---

## Law 4: Video End — The 2-Part High-Note Equation

Prevent end-of-video drop-offs and train viewers to click your next upload:
1. **Reveal the Big Payoff:** Clearly resolve the main curiosity gap/climax near the finale.
2. **End on a High Note:** Deliver a dramatic, wholesome, or unforgettable emotional punch right after the payoff, then transition cleanly without a "thanks for watching, bye" signal.

---

## Law 5: Post-Production — Ruthless Dull-Moment Audit

Never ship your first complete edit. After assembly:
1. **Run the "10 Blunt Critics" + "Watch-People-Watch" Roast:**
   Ask independent/simulated viewers (`retention-auditor` + viewer panels) to pinpoint every exact second where they felt:
   - **Bored** (eyes glaze over, reaching for their phone),
   - **Confused** (missed logical link or rushed diagram), or
   - **Forced to exert high effort to follow along** (overly dense jargon/numbers without visual anchoring).
2. **Cut or Rework Ruthlessly:** Delete or re-edit every flagged drag before publishing.

---

## Mandatory Verification Workflow

1. **Deterministic Audit Script:**
   ```bash
   python3 ~/.config/opencode/skills/youtube-retention-engine/scripts/audit_retention_architecture.py \
     --video path/to/video.mp4 \
     --thumb path/to/thumbnail.png \
     --title "Your Exact Title" \
     --thumb-text "THUMB WORDS" \
     --transcript path/to/script_or_srt.txt
   ```
   Inspect the generated `_retention_hook_sheet.jpg` with `read(...)` to verify Frame 1 mirrors the Thumbnail and `0:00–0:20` delivers `>= 8` dynamic context-driven visual shifts.
2. **Independent Subagent Gate:**
   Launch `subagent(agent="retention-auditor", ...)` on your title, thumbnail, script/EDL, and rendered MP4 + audit telemetry before declaring any video complete.

## References
- [references/5zu8s38ZwtQ_blueprint.md](references/5zu8s38ZwtQ_blueprint.md) — Timestamped empirical breakdown & Cheat Sheet from *How MrBeast Solved YouTube Retention* (`5zu8s38ZwtQ`).
