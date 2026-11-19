---
name: yt-thumbnail-brief
description: "Turn a YouTube video idea into a high-CTR, TV-friendly, psychology-first thumbnail brief and run deterministic 120px mobile + TV 50% Top-Half audits. Enforces Aprilynne Alter KE4zqD0ONDI rules: TV 50% Test, standalone Questions+Emotions without relying on the title, 10-15 references from 5 sources (extracting Question/Emotion/HOW mechanisms), Remove Clutter, Make Main Character Obvious, 2-4 words max (0% title overlap), and 3+ A/B text variants. Use whenever planning, designing, generating, or auditing any YouTube thumbnail."
---

# YouTube Thumbnail Brief (`KE4zqD0ONDI` + `I4nd9t84UvI`)

Across YouTube UIs today, thumbnails keep getting bigger while titles keep shrinking—and on TV (now the #1 screen in the US), **only the top 50%** of below-the-fold thumbnails are visible until a viewer presses Down. A thumbnail can no longer just look "relevant" to a title: it must generate **Questions + Emotions entirely on its own** and pass the **TV 50% Test** + **120px Mobile Pop Test**.

## When to use

- User asks "what should the thumbnail be for this video" or wants to generate/design a thumbnail
- User wants 2–3 thumbnail concepts + 3+ A/B text variants for Test & Compare
- User wants to audit or fix a thumbnail (`scripts/audit_thumbnail.py` + `thumbnail-auditor` subagent)

## The 6 Non-Negotiable Rules (`KE4zqD0ONDI`)

1. **TV-Friendly ("The 50% Test"):** Cover the bottom 50% of the thumbnail. Is there still enough focal subject (face/eyes/hero) and/or hook text in the **top half / top third** to communicate the video and make a TV viewer press "Down" on their remote?
2. **Standalone Interest (Don't Rely on the Title):** Hide the title completely. Does the thumbnail alone spark concrete **Questions** (*"What happened? What are the 5 rules?"*) and **Emotions** (awe, credibility, dread, vulnerability, shock)? Start brainstorming with *"What do I want the viewer to WONDER and FEEL?"*, never *"What should I show?"*.
3. **Reference Mechanism Transfer (Never Start From Scratch):** Pull **10–15 references** across 5 sources (*Internal Outliers, External Outliers, Model 3 cross-niche format channels, Bookmarks, Off-Platform movies/ads/covers*) and ask for each: *(a) What questions? (b) What emotions? (c) HOW visually does it create them?* Transfer the mechanism, never copy blindly.
4. **Remove Clutter:** Anything not actively helping the core story is actively hurting CTR. Strip real-life background bars, railings, noisy crowds, and secondary props.
5. **Make the Main Character Obvious:** The #1 focal hero must grab the eye in `<0.2s` at `120px` mobile scale (`luma_std >= 42.0`). Separate using bold color contrast, lighting rim, closer crop, or simple directional cue.
6. **A/B Test Thumbnail Text (`<= 4` words, `0%` Title Overlap):** Always write **3+ distinct text overlay angles** alongside visual concepts for YouTube Test & Compare (judged by watch-time share, not raw clicks).

## Steps

1. **Gather inputs & psychology targets:** Title, video payoff, TV vs mobile audience share, **exact Question(s) to spark**, and **exact Emotion(s) to trigger**.
2. **Pull reference mechanisms:** Name the visual mechanism (e.g., 2D vs 3D expectation subversion, stark subject color-pop against neutral backdrop, tight crop isolating scale).
3. **Draft 2–3 visual concepts + 3+ A/B text variants** using `references/brief-template.md` (varying one major visual lever per concept, 0% overlap with Title words).
4. **Verify every rendered or draft thumbnail image** using `scripts/audit_thumbnail.py` AND the independent **`thumbnail-auditor`** subagent (`subagent(agent="thumbnail-auditor", ...)`):
   ```bash
   python3 ~/.claude/skills/yt-thumbnail-brief/scripts/audit_thumbnail.py \
     --thumb path/to/thumbnail.png \
     --title "Exact Video Title" \
     --thumb-text "THUMB WORDS" \
     --out-dir path/to/audit_dir
   ```
   Inspect the generated `_thumbnail_diagnostic_sheet.jpg` (`Full` + `TV 50% Mask` + `120px Mobile` + `Standalone No-Title`) with `read(...)`.

## Anti-patterns (skill will refuse)

- Burying the subject or hook text only in the bottom half (fails TV 50% Test).
- "Relevant wallpaper" thumbnails that make zero sense or spark zero questions/emotion without reading the title.
- Cluttered backgrounds with distracting scaffolding, crowds, or tiny details.
- Main hero blending into the background instead of popping immediately.
- Repeating the Title's words on the thumbnail, or putting >4 words (`120px` smear).
- Generic plastic AI faces that violate channel authenticity or fail likeness checks.

## Resources

- `references/KE4zqD0ONDI_thumbnail_playbook.md` — Complete `KE4zqD0ONDI` playbook & before/after examples.
- `references/brief-template.md` — Fill-in brief + TV 50% + Psychology-First checklist.
- `scripts/audit_thumbnail.py` — Deterministic TV 50% + 120px Mobile + Clutter + Diagnostic Sheet tool.

## Related skills & agent

- `thumbnail-auditor` (`subagent`) — Adversarial thumbnail reviewer inspecting `_thumbnail_diagnostic_sheet.jpg`.
- `yt-title-optimizer` & `yt-package` — The other half of the click unit (`title.py`).
- `yt-hook-scripter` & `youtube-retention-engine` — Frame 1 (`0:00–0:05`) MUST mirror the approved thumbnail visually!
