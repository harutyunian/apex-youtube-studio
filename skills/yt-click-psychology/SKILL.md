---
name: yt-click-psychology
description: >-
  Apply cognitive psychology, eye-tracking, behavioral economics, and YouTube
  recommendation dynamics to engineer high-CTR thumbnails and titles without
  clickbait. Use when designing packaging, auditing low Browse/Home CTR, running
  Test & Compare experiments, framing tribal or high-arousal stories, or scoring
  topics with the CCN matrix.
---

# YouTube Click Psychology (`yt-click-psychology`)

Clicks on YouTube are rapid System 1 decisions under severe feed overload, evaluated jointly by the platform's **Engagement** (CTR + watch time) and **Satisfaction** (likes, surveys, Watch Time Share) objectives (Google MMoE / Zhao et al., 2019). High CTR with low AVD and falling impressions is flagged as clickbait and throttled.

Use this skill alongside `yt-thumbnail-brief`, `yt-package`, and `yt-title-optimizer` whenever engineering or diagnosing YouTube packaging.

---

## The 12 Behavioral Click Mechanisms

1. **150ms Rule & System 1 Intercept** (Kahneman; Thorpe 1996 / Kirchner & Thorpe 2006; Paddy Galloway glance test)
   - Visual categorization completes in `<150ms` and saccades launch at `~120ms`. If mobile feed thumbnails (`120–160px` wide) do not communicate instantly, System 2 never engages.
   - **Rule:** Hard cap of **2–3 visual elements**: `1` dominant hero (face/subject at `40–50%` frame) + `1` semantic contrast (artifact, rival, date/number) + `0–3` short words. Over 3 scattered elements costs ~`23%` CTR. Always verify at `10%` scale on a phone screen.

2. **Processing Fluency & Figure-Ground Contrast** (Reber, Schwarz & Winkielman 2004; PIA model Graf & Landwehr 2015)
   - Easy visual decoding produces instant positive affect and perceived quality/trust; dark/muddy collages trigger disfluency ("amateur" bias). Pair effortless visual form with a measured semantic puzzle.
   - **Rule:** Separate hero via rim light and background blur (works in both Light and Dark YouTube themes). Enforce `>= 4.5:1` text-to-backdrop contrast (clean white or yellow bold sans-serif on deep dark/saturated field). Remove tiny borders and channel logos on small channels.

3. **Von Restorff Isolation Effect & Feed Counter-Pattern** (1933)
   - Attention locks onto the single item that sharply diverges in color, scale, or luminance from surrounding uniform stimuli.
   - **Rule:** Before finalizing a thumbnail, open YouTube in Incognito and search the target query. Inspect the top 4–6 competitor cards; push your palette and composition into the **opposite contrast register** (e.g., bright documentary frame or electric blue/emerald if competitors use dark red/black-yellow).

4. **Information Gap Theory** (Loewenstein 1994; Heath "break the guessing machine")
   - Curiosity peaks at **partial knowledge** (a small, concrete, closeable gap)—never at total ignorance or closed summary titles (up to `+63%` CTR over closed descriptive headlines in digital UX studies). Implausible exaggeration or weak payoff destroys future channel trust.
   - **Formula:** `[Well-Known Subject/Entity] + [Concrete Contradiction or Hidden Cause]` — keep the resolution strictly inside the video.

5. **Thumbnail–Title Synergy & Non-Redundancy** (Mayer Redundancy Principle)
   - Repeating identical words across thumbnail text and title wastes cognitive bandwidth and half your ad surface.
   - **Rule:** **Thumbnail** draws an emotional scene and asks a silent question (`0–3` words; `7+` words loses across categories). **Title** escalates the conflict and states the stakes. Front-load the decisive hook inside the **first 45 characters** (`>75%` of views are mobile, where titles truncate around `40–50` chars); strip technical suffixes (`| Documentary`).

6. **Gaze Cueing & Two-Stage Attention** (Friesen & Kingstone 1998; Breeze 2009; Yarbus 1967)
   - Foveal clear vision covers only `2–3°`; viewers reflexively follow eye direction. Gaze cueing only works in Stage 2 if Stage 1 already won attention via clean composition.
   - **Rule:** Use either **direct eye contact** with the camera or a **directed gaze pointing onto the hero text/artifact**. Never point a face's gaze outward past the card edge (pushes viewers onto neighboring videos).

7. **Closed-Mouth Effect & Emotional Authenticity**
   - Audiences developed skepticism toward theatrical open-mouth shock thumbnails. In MrBeast's public Test & Compare runs, closed-mouth natural expressions outperformed open-mouth shock on **Watch Time Share**.
   - **Rule:** Favor authentic micro-expressions (fatigue, quiet dread, icy focus, suppressed tears) matching the tonal reality of the video's first `30` seconds.

8. **Negativity Asymmetry & Loss Aversion (`×2`)** (Robertson et al. 2023 *Nature Human Behaviour*; Kahneman & Tversky 1979)
   - Across `22,743` Upworthy RCTs (`~105k` headlines, `370M+` impressions), each negative word increased CTR by `+2.3%` while positive words reduced CTR; **sadness** was the most reliable click driver, while templated negativity decayed as audiences habituated. Loss aversion averages `λ ≈ 1.955` across `607` estimates.
   - **Rule:** Frame stakes around threat to legacy, downfall, costly mistake, or ending an era rather than flat victory recaps—while rotating fresh angles so negativity never feels templated.

9. **Tribalism, Schadenfreude & BIRGing / CORFing** (Cikara, Botvinick & Fiske 2011 fMRI; Cialdini 1976)
   - Rival failures activate reward circuitry (`ventral striatum`) just like own-team wins; fans **BIRG** (*Bask in Reflected Glory*) on hero/underdog breakthroughs and **CORF** (*Cut Off Reflected Failure*) on collapses.
   - **Dual Packaging Lever:** Package underdog/community hero triumphs via scale & pride (`BIRGing`), and package dominant giant/institution crises via collapse & reckoning (`Schadenfreude` attracts every rival fanbase).

10. **High-Arousal Emotions for Virality** (Berger & Milkman 2012 *JMR*)
    - Low-arousal sadness drives solo clicks, whereas **high physiological arousal**—**awe**, **moral outrage/anger**, and **anxiety**—drives shares, debates, and comment velocity.
    - **Rule:** Combine an injustice/moral conflict trigger (outrage) with extraordinary triumph or scale (awe) to convert browse clicks into viral distribution.

11. **CCN Matrix & Extreme Stakes Escalation** (Paddy Galloway; MrBeast 2024 internal guide)
    - Mass-reach videos simultaneously hook **Core** (niche die-hards), **Casual** (broad genre followers), and **New** (non-niche viewers drawn to human, financial, or investigative drama).
    - **Rule:** Pass every topic through the CCN filter, then sharpen the title framing (*"Survived 50 Hours"* > *"Spent 50 Hours"*) while ensuring **100% factual proof inside the video**.

12. **Test & Compare Discipline & Traffic-Source CTR Benchmarks**
    - Avoid evaluating CTR under `100` views (`±5pp` noise), tweaking after micro-fluctuations, or comparing Search CTR to Browse/Home CTR.
    - **3-Step Testing Protocol:**
      1. Prepare **3 genuinely distinct concepts** (`A`: close-up emotion + 2 words; `B`: visual before/after or duel contrast; `C`: minimal artifact + bold number) at `>= 1280×720` (avoiding YouTube `480p` downscaling).
      2. Run YouTube **Test & Compare** (optimizes for **Watch Time Share**); do **not** manually edit title/thumb mid-test; allow `7–14` days at `<1,000` daily impressions.
      3. Read CTR by traffic source (`Analytics → Reach → Traffic source`): if **Home/Browse CTR < 3%** in the first `24–48h` while **retention > 45–50%**, the video holds viewers and packaging is the bottleneck—repackage immediately.

---

## Pre-Publish Packaging Checklist

- [ ] **CCN Check:** Does the topic angle engage Core + Casual + New viewers?
- [ ] **150ms Glance Test:** `<= 3` visual elements, hero `40–50%`, `0–3` words, legible at `10%` mobile scale?
- [ ] **Fluency & Counter-Pattern:** Rim light + blur + `>= 4.5:1` contrast + distinct palette vs Incognito search rivals?
- [ ] **Gaze & Emotion:** Gaze points inward/at-target; authentic closed-mouth expression matching first `30s`?
- [ ] **Info Gap & Split:** `[Known Subject] + [Contradiction]` in first `45` chars; `0%` title–thumbnail text overlap?
- [ ] **A/B Ready:** 3 distinct `>= 1280×720` variants queued in Test & Compare?

## Reference

- Detailed research evidence, CTR benchmarks by traffic source/channel scale, and before/after examples: [behavioral-ctr-science.md](./references/behavioral-ctr-science.md).
