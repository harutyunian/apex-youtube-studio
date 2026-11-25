# Behavioral Click Psychology & CTR Science Reference

Synthesis of peer-reviewed cognitive/behavioral research, YouTube platform engineering papers, and 2025–2026 creator analytics benchmarks.

---

## 1. YouTube CTR Benchmarks by Source & Channel Scale (2025–2026)

| Segment / Traffic Source | Typical Range | Strong Target | Source / Notes |
|---|---|---|---|
| **All YouTube Channels / Videos (Middle 50%)** | `2% – 10%` | `> 10%` | YouTube Help Official |
| **Subscription Feed (Top Videos Ceiling)** | `<= 10%` | `8% – 10%` | Todd Beaupré (YouTube Growth & Discovery, Sept 2026) |
| **Home & Browse Recommendations** | `2% – 5%` (`2–6%` industry norm) | `6% – 10%+` (`7–10%+` outstanding) | vidIQ / OutlierKit |
| **YouTube Search** | `5% – 15%` | `15%+` | vidIQ |
| **Subscriber Notifications** | `10% – 20%` | `15% – 20%+` | vidIQ |
| **Small Channels (Core / Warm First Wave)** | `8% – 20%` | `15%+` | vidIQ |
| **Large Channels (`1M+` Subscribers, Cold Scale)** | `1.5% – 4%` | `4%+` | vidIQ |

> **Algorithmic Rule (Google MMoE — Zhao et al., 2019; Creator Insider / MilX 2026):** YouTube's multitask ranking optimizes **Engagement** (clicks + watch time) alongside **Satisfaction** (likes, surveys, Watch Time Share). High CTR paired with low AVD and falling impressions triggers clickbait demotion.

---

## 2. Empirical Evidence Matrix (12 Mechanisms)

| # | Mechanism | Primary Source / Study | Core Quantitative Finding | Practical Packaging Rule |
|---|---|---|---|---|
| 1 | **150ms System 1 Intercept** | Kahneman; Thorpe et al. (1996); Kirchner & Thorpe (2006); Galloway | Visual categorization `<150ms`; saccade onset `~120ms`; `>3` elements ~`-23%` CTR (AmpiFire) | Max `2–3` visual elements; hero `40–50%` frame; verify at `10%` phone scale |
| 2 | **Processing Fluency** | Reber, Schwarz & Winkielman (2004); PIA Model Graf & Landwehr (2015) | Fluent visual forms generate positive affect & perceived credibility | Rim light + background blur; `>= 4.5:1` text contrast; strip borders & tiny channel logos |
| 3 | **Von Restorff Isolation** | Hedwig von Restorff (1933) | Unique color/scale/luminance stimulus captures involuntary fixation | Incognito search target keyword; pick opposite palette from neighboring 4 cards |
| 4 | **Information Gap** | Loewenstein (1994 *Psych. Bull.*); Heath & Heath (*Made to Stick*) | Curiosity peaks on small, closeable gaps in partial knowledge (up to `+63%` CTR in UX reviews) | `[Known Subject] + [Specific Contradiction/Hidden Cause]`; deliver answer inside |
| 5 | **Non-Redundancy & Split** | Richard Mayer Redundancy Principle; mobile UX (`>75%` views) | Duplicating text across visual + title overloads working memory; mobile cuts at `40–50` chars | Thumb = silent visual question (`0–3` words); Title = stakes in first `45` chars |
| 6 | **Gaze Cueing** | Friesen & Kingstone (1998); Breeze (2009); Yarbus (1967) | Fovea is `2–3°`; viewers reflexively follow gaze in Stage 2 after clean Stage 1 hook | Direct eye contact OR gaze aimed at hero text/artifact; never look outside card edge |
| 7 | **Closed-Mouth Authenticity** | MrBeast Test & Compare observations | Closed-mouth natural expressions outperformed open-mouth shock on watch time | Use authentic restrained emotion matching first `30s` video tone |
| 8 | **Negativity & Loss Aversion** | Robertson et al. (2023 *Nature Human Behaviour*, 22,743 RCTs); Kahneman & Tversky (1979) | `+2.3%` CTR per negative word; sadness lifts clicks; joy/fear drop clicks; `λ ≈ 1.955` | Frame threats to legacy, crises, costly errors; rotate angles to avoid fatigue |
| 9 | **Tribalism (Schadenfreude / BIRGing)** | Cikara, Botvinick & Fiske (2011 fMRI); Cialdini (1976); Bernhardt et al. (1998) | Rival failures activate ventral striatum; fans BIRG on hero wins & CORF on losses | Underdog wins = triumph/scale (`BIRGing`); giant crises = downfall/reckoning (`Schadenfreude`) |
| 10 | **High-Arousal Virality** | Berger & Milkman (2012 *JMR*, NYT corpus) | High arousal (awe, anger/moral outrage, anxiety) drives shares; passive sadness does not | Pair moral injustice/conflict (outrage) with awe-inspiring feat/scale |
| 11 | **CCN + Stakes Escalation** | Paddy Galloway CCN; *How to Succeed in MrBeast Production* (2024) | Broad scale needs **Core + Casual + New** appeal + sharpened honest stakes | Rewrite narrow technical topics into human/investigative stakes backed 100% by facts |
| 12 | **Test & Compare Discipline** | YouTube Help; Test & Compare (`Watch Time Share`) | `<100` views has `±5pp` variance; Test & Compare picks Watch Time Share winner | Test 3 distinct concepts `>= 1280×720` for `7–14` days; swap if Home CTR `<3%` & AVP `>45–50%` |

---

## 3. Before / After Packaging Transformations

| Weak Packaging (Low CTR Pattern) | Behavioral Diagnosis | High-CTR Rework (Mechanism Applied) |
|---|---|---|
| Descriptive full biography title (`"Player X: From Childhood to 8 Trophies"`) | Closed plot — zero Loewenstein information gap; no reason to click now | `[Known Star] + [Specific Unexplained Turning Point]` (`"Why [Star] Wrote His Farewell Letter 48 Hours After the Final"`) |
| Collage of 3 subjects + league badge + scoreboard + 7-word overlay repeating title | Fails `150ms` System 1 test (`>3` elements, `-23%` CTR), Mayer redundancy, `120px` smear | Single tight portrait (`45%` frame, closed-mouth tension, rim light) + 1 contrast artifact + `2` words (`"28 POINTS"`) |
| Narrow tactical title (`"How Midfielder Y Plays Second Balls"`) | Appeals only to Core (`5%` ceiling), zero Casual/New emotional hook | CCN Escalation (`"The $500 Wage to $50M Star: How [Club] Found Their Secret Weapon"`) |
| Flat neutral recap (`"Club X Struggles Under New Coach"`) | Low arousal, weak loss aversion | High-arousal stakes + Schadenfreude (`"$400M Wasted: How [Coach] Led [Club] to a 1–4 Home Collapse"`) |
