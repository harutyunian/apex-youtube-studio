#!/usr/bin/env python3
"""hookscore.py - score a YouTube hook before you waste a take on it.

Six checks (5 core 0-100 properties + optional 0-5s Title alignment & <=20s Input-Bias check):
  SPECIFICITY, ADDRESS, STAKES, CURIOSITY, BREVITY (+ optional TITLE_MATCH & INPUT_BIAS note).

    python3 hookscore.py hooks.txt                       # one hook per line, ranked
    python3 hookscore.py --hook "one line"               # score a single hook
    python3 hookscore.py --title "Title" --hook "..."    # check 0-5s title lock + 20s hook budget
    python3 hookscore.py --json hooks.txt                # machine-readable
"""

import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
FORMULAS = json.load(open(os.path.join(HERE, "hooks.json")))["hooks"]

FILLER = {
    "basically",
    "actually",
    "literally",
    "just",
    "really",
    "very",
    "so",
    "kind",
    "sort",
    "like",
    "guys",
    "hey",
    "welcome",
    "today",
    "video",
    "subscribe",
    "channel",
}
VAGUE = {
    "amazing",
    "incredible",
    "insane",
    "crazy",
    "huge",
    "massive",
    "game",
    "changer",
    "secret",
    "powerful",
    "ultimate",
    "best",
    "revolutionary",
    "mind",
    "blowing",
    "unbelievable",
}
STOP = {
    "the",
    "a",
    "an",
    "of",
    "for",
    "to",
    "in",
    "on",
    "and",
    "or",
    "is",
    "are",
    "was",
    "were",
    "with",
    "your",
    "you",
    "my",
    "i",
    "we",
    "they",
    "this",
    "that",
    "it",
    "how",
    "what",
    "why",
    "from",
    "by",
}
CONCRETE = re.compile(
    r"\b(\d[\d,.]*\s?(%|k|m|b|x|s|h)?|\$\d[\d,.]*[kmb]?|\d+\s?(second|minute|hour|day|week|month|year)s?)\b",
    re.I,
)
YOU = re.compile(r"\b(you|your|you're|youre|yourself)\b", re.I)
STAKE = re.compile(
    r"\b(lose|lost|wasting|waste|quit|fail|broke|cost|risk|before|stop|never|die|dying|dead|bankrupt|collapse|wiped|bet|fight|win|surviv\w*)\b",
    re.I,
)
CURIOSITY = re.compile(
    r"\b(why|how|what|which|until|before|but|nobody|almost|except|reason|actually|really|secret|hidden|truth)\b",
    re.I,
)
EFFORT = re.compile(
    r"\b(spent|studied|analyzed|reviewed|read|examined|filings?|transcripts?|interviews?|tracked|tested|months?|weeks?|years?|days?|hundreds?|thousands?|every single)\b",
    re.I,
)
GREETING = re.compile(
    r"\b(hey guys|welcome back|welcome to|before we start|in today'?s video|make sure to subscribe)\b",
    re.I,
)


def words(t):
    return re.findall(r"[a-z0-9'%$.]+", t.lower())


def specificity(t):
    w = words(t)
    if not w:
        return 0
    nums = len(CONCRETE.findall(t))
    vague = sum(1 for x in w if x in VAGUE)
    filler = sum(1 for x in w if x in FILLER)
    s = 34 + nums * 22 - vague * 16 - filler * 5
    s += min(18, 6 * sum(1 for x in t.split()[1:] if x[:1].isupper()))
    return max(0, min(100, s))


def address(t):
    n = len(YOU.findall(t))
    first = 30 if YOU.search(" ".join(t.split()[:6])) else 0
    return max(0, min(100, 26 + n * 20 + first))


def stakes(t):
    n = len(STAKE.findall(t))
    return max(0, min(100, 22 + n * 26 + (14 if CONCRETE.search(t) else 0)))


def curiosity(t):
    n = len(CURIOSITY.findall(t))
    q = 18 if t.strip().endswith("?") else 0
    closed = -18 if re.search(r"\b(because|so that|which means)\b", t, re.I) else 0
    return max(0, min(100, 24 + n * 17 + q + closed))


def brevity(t):
    n = len(words(t))
    if n == 0:
        return 0
    # 9-24 words for sentence-1 hook (~4-9s) OR up to 55 words for full 20s 3-element hook block
    if 9 <= n <= 24:
        return 100
    if 25 <= n <= 55:
        return max(72, 100 - (n - 24))
    if n < 9:
        return max(30, 100 - (9 - n) * 11)
    return max(10, 72 - (n - 55) * 4)


PROPS = [
    ("SPECIFICITY", specificity),
    ("ADDRESS", address),
    ("STAKES", stakes),
    ("CURIOSITY", curiosity),
    ("BREVITY", brevity),
]


def classify(t):
    best, hits = None, 0
    for f in FORMULAS:
        n = sum(1 for p in f["match"] if re.search(p, t, re.I))
        if n > hits:
            best, hits = f, n
    return (best["name"] if best else "Unclassified"), hits


def title_alignment(t, title):
    if not title:
        return None
    tt = set(words(title)) - STOP
    first_sent = re.split(r"[.!?]+", t.strip())[0]
    ft = set(words(first_sent)) - STOP
    overlap = sorted(tt & ft)
    return {
        "title_tokens": sorted(tt),
        "first_sentence_overlap": overlap,
        "matched_in_first_5s": len(overlap) > 0,
    }


def score(t, title=None):
    parts = {n: fn(t) for n, fn in PROPS}
    vals = list(parts.values())
    verdict = round(0.6 * (sum(vals) / len(vals)) + 0.4 * min(vals))
    if GREETING.search(t):
        verdict = max(0, verdict - 25)
    name, hits = classify(t)
    wcount = len(words(t))
    est_sec = round(wcount / 2.55, 1)  # ~153 WPM
    effort_hits = len(EFFORT.findall(t))
    align = title_alignment(t, title)
    return {
        "parts": parts,
        "verdict": verdict,
        "name": name,
        "hits": hits,
        "word_count": wcount,
        "est_seconds": est_sec,
        "exceeds_20s_cap": est_sec > 20.0,
        "has_greeting": bool(GREETING.search(t)),
        "input_bias_cues": effort_hits,
        "title_alignment": align,
    }


def band(v):
    return "STRONG" if v >= 72 else "WORKABLE" if v >= 55 else "WEAK"


def report(t, res):
    parts = res["parts"]
    verdict = res["verdict"]
    print(f"\n  {t.strip()}")
    print(f"  {'-' * min(72, max(20, len(t.strip())))}")
    for k, v in parts.items():
        print(f"    {k:<12} {v:3d}  {'#' * (v // 5)}")
    print(
        f"    {'VERDICT':<12} {verdict:3d}  {band(verdict)}  (~{res['est_seconds']}s / {res['word_count']} words)"
    )
    print(
        f"    formula      {res['name']}"
        + (
            f"  ({res['hits']} pattern{'s' if res['hits'] != 1 else ''} matched)"
            if res["hits"]
            else "  (no formula matched - that is usually a summary, not a hook)"
        )
    )
    if res["has_greeting"]:
        print(
            "    WARNING      Greeting/filler detected — cut 'hey guys / welcome' (0-5s Expectation Lock!)"
        )
    if res["exceeds_20s_cap"]:
        print(
            f"    WARNING      Hook runs ~{res['est_seconds']}s (>20s hard ceiling! Body must start <=20s)"
        )
    if res["input_bias_cues"] == 0:
        print(
            "    tip          Add an Input Bias cue (time/effort/research proof) or pair with high-craft opening montage"
        )
    else:
        print(
            f"    input-bias   {res['input_bias_cues']} effort/research cue(s) detected"
        )
    if res["title_alignment"]:
        al = res["title_alignment"]
        if al["matched_in_first_5s"]:
            print(
                f"    title-lock   OK (first sentence echoes title: {', '.join(al['first_sentence_overlap'])})"
            )
        else:
            print(
                f"    title-lock   MISSING in Sentence 1! Echo title terms {al['title_tokens']} in 0-5s"
            )
    low = min(parts, key=parts.get)
    print(f"    weakest      {low} - {FIX[low]}")


FIX = {
    "SPECIFICITY": "swap one adjective for a number, a name or a date",
    "ADDRESS": "say 'you' in the first six words",
    "STAKES": "name what it costs them to keep doing it the current way",
    "CURIOSITY": "cut the half of the sentence that answers itself",
    "BREVITY": "9-24 words for Sentence 1, <=55 words for full 0-20s hook before Body starts",
}


def main():
    a = sys.argv[1:]
    as_json = "--json" in a
    a = [x for x in a if x != "--json"]
    title = None
    if "--title" in a:
        ti = a.index("--title")
        title = a[ti + 1]
        a = a[:ti] + a[ti + 2 :]
    if "--hook" in a:
        lines = [a[a.index("--hook") + 1]]
    elif a and os.path.exists(a[0]):
        lines = [l for l in open(a[0]).read().splitlines() if l.strip()]
    else:
        print(__doc__)
        sys.exit(1 if not a else 0)
    out = []
    for t in lines:
        res = score(t, title=title)
        out.append(
            {
                "hook": t.strip(),
                "properties": res["parts"],
                "verdict": res["verdict"],
                "band": band(res["verdict"]),
                "formula": res["name"],
                "matched": res["hits"],
                "word_count": res["word_count"],
                "est_seconds": res["est_seconds"],
                "exceeds_20s_cap": res["exceeds_20s_cap"],
                "input_bias_cues": res["input_bias_cues"],
                "title_alignment": res["title_alignment"],
                "res": res,
            }
        )
    out.sort(key=lambda r: -r["verdict"])
    if as_json:
        print(
            json.dumps(
                [
                    {k: v for k, v in r.items() if k not in ("matched", "res")}
                    for r in out
                ],
                indent=1,
            )
        )
        return
    for r in out:
        report(r["hook"], r["res"])
    if len(out) > 1:
        print(
            f"\n  winner: {out[0]['hook'].strip()}  ({out[0]['verdict']}, {out[0]['band']})\n"
        )


if __name__ == "__main__":
    main()
