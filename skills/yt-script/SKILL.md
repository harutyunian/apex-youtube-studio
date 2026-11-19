---
name: yt-script
description: >-
  Write a YouTube video script from a raw idea - hook options off 21 formulas,
  scored, enforcing 0-5s Title/Thumbnail lock, 0-20s 3-element + Input Bias
  hook (<=20s body launch, >=8 visual shifts), context-driven [ON SCREEN]
  variety every 2-5s (no same-room repetition or NY->Chicago jumps, incl. AI video),
  continuous contrast, 2-4 min energy cycling, and high-note payoff endings.
  Use whenever writing a video script, hook, or opening lines.
---

# yt-script

One idea into a script somebody finishes (`70%+` retention architecture from `5zu8s38ZwtQ` + `I4nd9t84UvI`).

Tools live in this folder and actually run. Use them—do not eyeball the hook:

```bash
python3 hookscore.py hooks.txt                      # rank your hook options
python3 hookscore.py --hook "one line"              # score a single hook
python3 hookscore.py --title "Title" --hook "..."   # score + verify 0-5s Title alignment & 20s budget
```

## Before you write

1. Read `voice.md` or `CHANNEL_PROFILE.md` in your project root (or `~/.claude/youtube/voice.md`) if it exists. That is the creator's voice profile: how they talk on camera, the words they never use, who they are talking to, what they will not claim. If it does not exist, infer the voice from three sample scripts/videos first.
2. Never invent a number, a result, or a source. If a figure would strengthen it and you do not have one, ask for it or write the line without it.

## The shape (`5zu8s38ZwtQ` Retention Architecture)

1. **`0:00–0:05` Expectation Lock (2-Step Formula):**
   - **First Sentence matches the Title** verbally within 0–5s (zero greeting, zero logo intro).
   - **Frame 1 matches the Thumbnail** visually (focal subject, setting, color palette) and the opening lines clarify the thumbnail's exact meaning.
2. **`0:05–0:20` The 3-Element + Input Bias Hook (`<= 55` words, body starts `<= 0:20`):**
   - Write FIVE hooks against [the 21 formulas](hooks.json), run them through `hookscore.py --title "..."`, keep the top two, and show the user both with their scores.
   - Every hook MUST contain inside `0:00–0:20`:
     1) **Context** from the title;
     2) **Stakes / Reward / Payoff** matching the title;
     3) **Curiosity Gap** (open loop forcing the viewer to stay);
     4) **Match -> Exceed via Input Bias** (prove research depth, craft, or effort immediately so viewers value the video more);
     5) **`8+` `[ON SCREEN: ...]` dynamic visual cues inside `0:00–0:20`** (`~2.0–2.5s` each).
   - **Hard `0:20` Body Launch:** Transition straight into Point #1 / Act 1 **no later than `0:20`**.
3. **The Body (`0:20` -> End): 3 Secrets to Keep the Curve Flat:**
   - **Context-Driven Visual Variety (`2.0–5.0s`, zero `>=10s` static holds):** Mark `[ON SCREEN: ...]` on every beat! Never let cuts cycle inside one boring static room/template, AND never make random disconnected jumps (e.g., New York -> Chicago) — **every cut (including AI-generated video) must follow the exact spoken context** while changing scale, angle, or medium.
   - **Continuous Contrast:** Alternate emotional intensity vs relief/contrast perspectives, dark vs light visual surfaces, archival footage vs 2D diagrams vs real voices.
   - **2–4 Min Energy Cycling:** Structure acts in 2–4 min High-Energy -> Low-Energy cycles (shorter/lighter upfront, longer cycles and slower emotional depth reserved for the **final 20%**).
4. **The Payoff & High-Note End (Last 5–10%):**
   - Deliver the **Big Payoff** explicitly, then **end on a high note** (dramatic, wholesome, or memorable) and bridge straight to the next video—never say *"thanks for watching, bye"*.
5. **Post-Script Retention Roast:**
   - Run `retention-auditor` (`subagent(agent="retention-auditor", ...)`) to hunt every line where a viewer might feel bored, confused, or forced to exert effort to follow, and cut/tighten before recording.

## What to hand back

- The top two hooks with their `hookscore.py` scored panels (`0–5s` Title match + `<=20s` word check)
- The full script, beat by beat, with `[ON SCREEN: ...]` (`<=3–5s` context-driven cuts), cycle resets (`2–4m`), and `0:20` Body Launch timestamp marked
- Runtime estimate at ~150–155 words per minute
- One line naming which formula the winning hook used and how Input Bias + Continuous Contrast are achieved

## The gate

Nothing here publishes. Every output ends in a block the user copies, and the last line of every run is: **ship it, or change it?**
