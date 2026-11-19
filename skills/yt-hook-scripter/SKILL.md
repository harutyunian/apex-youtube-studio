---
name: yt-hook-scripter
description: "Script the spoken + visual opening that decides retention: the 0-5s Title/Thumbnail Lock and the 0-20s 3-element hook (Context + Stakes/Payoff + Curiosity Gap + Input Bias effort signal + >=8 visual shifts, launching into the video body NO LATER than 0:20) for long-form YouTube videos or the 3-second frame-one hook for Shorts. Use to write or fix any video opening. Not for the title (use yt-title-optimizer) or description (use yt-description-writer)."
---

# YouTube Hook Scripter (`0–5s` Lock + `0–20s` Hook Engine)

The packaging earns the click; the **first 5 seconds** confirm it, and the **first 20 seconds** decide whether the retention curve flattens above 70% or dives off a cliff. The steepest viewer drop-off happens inside the first 20 seconds.

## When to use

- User says "write my intro" or "how should this video open"
- A video's retention drops hard in the first 20–30 seconds and needs a re-cut
- User has a Short and needs the first 3 seconds to stop the swipe
- User wants the spoken + visual hook to match and exceed the title & thumbnail promise

## Empirical Opening Architecture (`5zu8s38ZwtQ`)

1. **`0:00–0:05` — The 2-Step Expectation Lock (Meet Click Expectations Immediately):**
   - **Sentence 1 matches the Title** verbally within 0–5s (zero greeting, zero channel intro).
   - **Frame 1 matches the Thumbnail** visually (primary subject, setting, emotion, color palette), and within the opening seconds the voice clarifies the exact meaning of the thumbnail text/visual.
2. **`0:05–0:20` — The 3 Core Hook Elements + Input Bias Bonus:**
   - **Context (from Title):** What the viewer must know right now so the premise makes sense.
   - **Stakes / Reward / Payoff (matching Title):** Why care / what's on the line / what they get.
   - **Curiosity Gap ("Open Loop"):** Withhold the central answer so they stay to find out.
   - **Match -> Exceed via Input Bias:** Confirm what they clicked for, then show/promise *even more*. Trigger **Input Bias** immediately—let the audience *feel* the huge time, research, craft, or effort invested in the first seconds (spreadsheets, primary docs, multi-angle montage, bespoke visuals).
3. **Dynamic Opening Shots (`>= 8` Visual Shifts in `0:00–0:20`):**
   - Plan `~2.0–2.5s` per shot (`8+` distinct context-driven shots/angles/proof visuals inside 0–20s).
4. **Hard `<= 0:20` Body Launch:**
   - Transition straight into Challenge #1 / Experience #1 / Point #1 **NO LATER than `0:20`** (target `0:12–0:19`).

## Formulas this skill uses (opening-hook shapes)

| Code | Formula | Surface | Best for |
|---|---|---|---|
| Y7 | Restate-and-Raise | long-form `<=20s` | confirm the promise in 5s, raise the stakes by 15s |
| Y8 | Cold-Open Payoff Tease | long-form `<=20s` | match thumbnail frame 1, tease climax, launch body `<=20s` |
| Y9 | Question-and-Contract | long-form `<=20s` | answer fast, show Input Bias effort, open deeper loop |
| Y10 | Shorts 3-Second Hook | Shorts 3s | state payoff/tension on frame one, loop the end |

## Steps

**Voice profile first (all drafts).** If `../../references/voice-profile.md` has `filled: yes`, load it and match the user's voice fingerprint, hard rules, and CTA/link style throughout.

**Never invent the specifics.** Take concrete numbers, dates, and entities from verified facts or what the user supplied. **Do not invent a figure, date, client name, or result.**

1. **Gather inputs.** Title, thumbnail concept/text, single core payoff, effort/research receipts (for Input Bias), target viewer, and long-form vs Short.
2. **Pick the surface.**
   - Long-form: write the **first 20 seconds (`0:00–0:20`)**, beat by beat (`0–5s` lock -> `5–18s` 3 elements + Input Bias -> `<=20s` pivot into Body), specifying BOTH `[SPOKEN]` and `[ON SCREEN VISUAL]` (`8+` dynamic shots).
   - Short: write `0:00–0:03` (frame-one payoff/visual matching thumbnail) plus the seamless end-to-start loop line.
3. **Pick the formula.** Pair the title formula with Y7/Y8/Y9 (or Y10 for Shorts).
4. **Write the script.** Spoken voice, one person to one person:
   - **0:00–0:05:** Sentence 1 echoes the Title + clarifies Thumbnail; Frame 1 matches Thumbnail visually.
   - **0:05–0:16:** Context + Stakes/Reward + Curiosity Gap + Input Bias effort proof.
   - **0:16–0:20:** Pivot directly into Body Point #1 / Act 1 (**strictly `<= 0:20`, max `~55` words total**).
   - Mark all 8+ context-driven `[ON SCREEN: ...]` visual beats (zero boring same-room cuts, zero unmotivated random jumps).
5. **Strip the intro & humanize.** Cut greetings/logos/filler, strip 2026 AI buzzwords, use `..` for spoken pauses.
6. **Score & Verify.** Run `~/.claude/skills/yt-script/hookscore.py --title "..." --hook "..."` and invoke `retention-auditor` if auditing a full opening package.
7. **Approval card.** Output the timestamped `0:00–0:20` audio+visual hook sheet and the Title/Thumbnail it locks to.

## Hard rules

- No greeting, no intro animation, no logo sting before the hook. Ever.
- First spoken sentence (`0:00–0:05`) MUST mirror the Title and clarify the Thumbnail.
- Frame 1 (`0:00–0:03`) MUST visually match the Thumbnail.
- Body starts **no later than `0:20`** (`<= 55` words in long-form hook).
- First `0:20` hits all 3 elements (**Context + Stakes/Payoff + Curiosity Gap**) PLUS **Input Bias** (visible effort) and **`8+` context-driven visual shifts**.
- Never promise more than the video delivers; match expectations, then exceed them.

## Anti-patterns (skill will refuse)

- "Hey guys, welcome back to the channel" or any greeting.
- Intro/setup dragging past `0:20` before the actual video starts.
- Frame 1 and Thumbnail visually contradicting each other.
- Title keywords missing from the opening 5 seconds.
- Zero visible effort / Input Bias in `0:00–0:20`.
- "Make sure to like and subscribe" inside the hook.
- "No X. No Y. Just Z." staccato filler or unsubstantiated candor ("not gonna lie").

## Resources

- `references/retention-beats.md` — `0:00–0:05` + `0:05–0:20` + Shorts retention beats.
- `youtube-retention-engine` skill & `retention-auditor` subagent — full retention architecture & audit.

## Related skills

- `yt-title-optimizer` — the promise the hook keeps
- `yt-thumbnail-brief` — the visual frame 1 must mirror
- `mrbeast-10x-viral-video` — 10x escalation & cadence enforcement
