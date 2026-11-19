# 15-Point Director Shot Rubric & 8-Axis Scoring System

## Part 1: Per-Shot Evaluation Criteria (15 Axes)

Evaluate every shot across its `START` (10%), `MID` (50%), and `END` (90%) frames — and via direct video playback for hero/transition clips — against these 15 professional criteria:

| # | Criterion | What Good Looks Like | Defect Signals to Flag |
|---|---|---|---|
| 1 | **Composition & Framing** | Intentional rule-of-thirds or architectural symmetry; balanced negative space; clean horizon. | Awkward tangent crops, cramped headroom, cluttered edges, accidental crooked horizon. |
| 2 | **Camera Angle & Movement** | Motivated push-in (intimacy/tension) or pull-out (reveal/scale); smooth sub-pixel motion. | Unmotivated direction reversals,zoompan pixel judder, static freeze lasting >4s on a supposed motion graphic. |
| 3 | **Subject Positioning** | Primary subject sits cleanly outside lower-third overlays; full head/chin preserved on portraits. | Lower-third banner covering subject's mouth, hands, ball, or key action; severed forehead on vertical-to-16:9 crop. |
| 4 | **Visual Hierarchy** | Viewer's eye lands immediately on the narrative subject first, typography second. | Thin text floating over bright specular highlights without a dark backing plate; competing visual clutter. |
| 5 | **Lighting & Shadows** | Coherent light direction; naturalistic chiaroscuro or stadium floodlight falloff. | Flat plastic AI lighting, impossible dual sun shadows, crushed unreadable shadow detail. |
| 6 | **Color Grading** | Consistent color temperature and black point across shots within the same historical scene. | Jarring jump from warm Kodak 1990s amber to clinical cyan digital without narrative motivation. |
| 7 | **Depth & Cinematic Appearance** | Foreground/midground/background separation, natural optical depth of field, organic film texture. | Waxy AI skin, oversharpened halos, sterile PowerPoint-flat boxes. |
| 8 | **Historical Accuracy** | Period-authentic vehicles, architecture, football kits, national flags, stadium roofs, and dates. | Anachronistic modern cars/smartphones in 1990s scenes; wrong match flags in stadium rafters (e.g., Brazil/Serbia flags during an Argentina/France narration); wrong year on title card. |
| 9 | **Character Consistency** | Subject's age, stature, hairstyle, wardrobe, and likeness match the exact era/person narrated. | Young 20-year-old depiction used during elderly 80-year-old narration; generic plastic AI face replacing real person. |
| 10 | **Visual Storytelling** | The image adds concrete visual information rather than merely decorating wallpaper; every real & AI clip matches spoken context. | Generic exterior repeated; boring same-room/same-template cuts repeated; random unmotivated location jumps (e.g., NY -> Chicago) disconnected from narration. |
| 11 | **Emotional Impact** | Framing and light amplify the human stakes; heavier emotional weight peaks cleanly in the final 20% and high-note climax. | Cheerful bright stock-like photo during tragic narration; heavy slow exposition placed in first 20% instead of last 20%; flat emotional ending. |
| 12 | **Continuity with Neighboring Shots** | Smooth eye-trace, scale progression (Wide -> Medium -> Close-Up), continuous contrast across formats, and transition discipline. | Jump cuts between nearly identical framing/same room; constant dip-to-black (`fade out + fade in`); zero contrast between adjacent shots. |
| 13 | **Suitability for Narration** | Visual content directly corresponds to the exact sentence spoken; `0:00–0:05` Frame 1 & Sentence 1 lock to Thumbnail & Title and clarify thumbnail meaning. | Opening 0–5s misses Title/Thumbnail contract; hook drags past `0:20`; lower-third or image lags/leads narration by >3s; mismatched person shown. |
| 14 | **Editing Rhythm** | Dynamic `0:00–0:20` hook (`>= 7–8` visual shifts in 20s); `2.4–5s` body cadence with `2–4 min` High->Low energy cycles (no middle valley). | Static talking-head or static graphic held `>= 10s`; `< 5` visual changes in first 20s; hook > 20s before Act 1 begins; sagging middle-valley slump; `< 2.0s` unreadable card. |
| 15 | **Technical Quality** | Crisp `1920x1080` native typography, clean H.264 macroblocks, zero garbled AI letters/anatomy. | Gibberish AI signage/crests, six-fingered hands, warped football geometry, pixelated low-res upscale, missing Cyrillic glyphs. |

---

## Part 2: Defect Severity Classification

Every logged issue MUST carry one of three severities:

- **`CRITICAL` (Release Blocker — Must Fix Before Approval):**
  - Unlabeled AI reconstruction presented without synthetic disclosure;
  - Factually wrong historical match/person/flag/kit contradicting narration (e.g., wrong teams' flags in stadium);
  - Unreadable title/caption due to highlight collision or broken Cyrillic glyphs;
  - Severed face/head crop, garbled AI text/hands clearly visible, unintended black drop, audio clipping (`> -1.0 dBTP`), or TTS stage-direction leak.
- **`MAJOR` (Significant Craft Flaw — Fix Required to Reach >= 8.0):**
  - Overlong static/zoompan shot (`> 15.0s`) causing pacing drag;
  - Repetitive dip-to-black between every shot within the same scene instead of clean straight cuts;
  - Color-grade jump within a continuous sequence;
  - Repeated visual asset reused too closely without new narrative purpose;
  - Weak emotional match between image and narration.
- **`MINOR` (Polish Opportunity):**
  - Slight lower-third timing refinement (`0.3–0.8s`);
  - Minor kerning/padding balance on data cards;
  - Subtle room-tone / music crossfade smoothing.

---

## Part 3: 8-Axis Chapter Scoring Rubric (`1–10`)

Score each chapter independently from `1` to `10` (integers or `.5` increments):
1. **Cinematography** (lighting, depth, lens feel, camera motion smoothness)
2. **Composition** (framing, subject placement, title-safe discipline, contrast hierarchy)
3. **Editing** (shot-length rhythm, cut vs fade discipline, sequence continuity)
4. **Visual Consistency** (cohesive color script, unified graphic system, zero jarring style shifts)
5. **Historical Accuracy** (period fidelity, kits/flags/stadiums, honest archival vs AI labeling)
6. **Sound** (TTS naturalness & Russian stress accuracy, `-16 LUFS` loudness, sidechain music balance)
7. **Storytelling** (clarity of cause-and-effect, visual-verbal synergy, hook & chapter payoff)
8. **Emotional Impact** (human resonance, dramatic build, musical & visual catharsis)

### Hard Anti-Inflation Rules:
- **`9.0 – 10.0`:** Exceptional festival/broadcast quality. **Forbidden** if `CRITICAL > 0` or `MAJOR > 0`. Requires explicit shot-by-shot justification.
- **`8.0 – 8.5`:** Strong professional release quality. `CRITICAL == 0`, at most `1–2` documented `MINOR`/`MAJOR` nuances.
- **`6.5 – 7.5`:** Watchable rough cut with noticeable pacing drags, repetitive transitions, or minor historical/contrast flaws. **Requires revision pass.**
- **`<= 6.0`:** Defective cut (`CRITICAL` historical/technical/provenance errors present). **Blocked.**
