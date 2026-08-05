#!/usr/bin/env python3
"""
Fetch Orangetheory Fitness workout summaries from Reddit.
Usage: get_workout.py [--date YYYY-MM-DD] [--format 2G|3G|Strength50|...]
Defaults to tomorrow's date if not specified.
"""

import sys
import json
import urllib.request
import argparse
import re
from datetime import datetime, timedelta


SEARCH_URL = (
    "https://www.reddit.com/r/orangetheory/search.json"
    "?q=flair%3A%22{flair}%22&restrict_sr=1&sort=new&limit=25"
)
POST_URL = "https://www.reddit.com/r/orangetheory/comments/{post_id}.json?limit=100"
HEADERS = {"User-Agent": "OTFWorkoutBot/1.0"}

WORKOUT_KEYWORDS = ["tread", "row", "floor", "block", "exercise", "base pace", "push pace"]
FORMAT_PATTERN = re.compile(
    r"(?:^|\W)(orange\s*\d+\s*[23]g|[23]g\s*\d+|[23]g|strength\s*\d+|endurance\s*\d+|power\s*\d+|esp\s*\d+|tread\s*\d+|hybrid\s*[23]g|tornado)",
    re.IGNORECASE,
)


def fetch_json(url):
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read())


def date_matches_title(target: datetime, title: str) -> bool:
    month_name = target.strftime("%B")
    month_abbr = target.strftime("%b")
    day = target.day

    patterns = [
        rf"\b{month_name}\s+{day}\b",
        rf"\b{month_abbr}\s+{day}\b",
        rf"\b{target.month}/{day}\b",
        rf"\b{day}\s+{month_name}\b",
        rf"\b{day}\s+{month_abbr}\b",
    ]
    for pat in patterns:
        if re.search(pat, title, re.IGNORECASE):
            return True
    return False


def search_posts(flair: str, target: datetime) -> list[dict]:
    url = SEARCH_URL.format(flair=flair.replace(" ", "+"))
    data = fetch_json(url)
    matches = []
    for child in data.get("data", {}).get("children", []):
        post = child.get("data", {})
        if date_matches_title(target, post.get("title", "")):
            matches.append(post)
    return matches


def fetch_post_content(post_id: str) -> dict:
    url = POST_URL.format(post_id=post_id)
    data = fetch_json(url)
    post = data[0]["data"]["children"][0]["data"]
    comments = []
    for child in data[1]["data"]["children"]:
        if child["kind"] == "t1":
            comments.append(child["data"])
    return {"post": post, "comments": comments}


def has_workout_content(text: str) -> bool:
    lower = text.lower()
    return sum(1 for kw in WORKOUT_KEYWORDS if kw in lower) >= 2


def detect_format_label(text: str, fallback: str = "") -> str:
    """Extract a workout format label like '2G', 'Strength 50' from text."""
    m = FORMAT_PATTERN.search(text)
    if m:
        return m.group(1).strip()
    return fallback


def is_full_workout(text: str) -> bool:
    """A full workout comment mentions both tread and floor sections."""
    lower = text.lower()
    has_tread = "tread" in lower
    has_floor = "floor" in lower
    return has_tread and has_floor


def collect_workout_blocks(posts: list[dict]) -> list[dict]:
    """Gather workout blocks from posts and their comments."""
    blocks = []

    for post in posts:
        content = fetch_post_content(post["id"])
        p = content["post"]
        title = post.get("title", "")

        # Check post body
        body = p.get("selftext", "")
        if has_workout_content(body):
            label = detect_format_label(body) or detect_format_label(title) or title
            blocks.append({
                "label": label,
                "body": body,
                "score": p.get("score", 0),
                "full": is_full_workout(body),
            })

        # Check comments
        for c in content["comments"]:
            cbody = c.get("body", "")
            label = detect_format_label(cbody)
            has_content = has_workout_content(cbody)
            if not label and not has_content:
                continue
            if not label:
                label = detect_format_label(title)
            if not label:
                continue
            blocks.append({
                "label": label,
                "body": cbody,
                "score": c.get("score", 0),
                "full": is_full_workout(cbody),
            })

    return blocks


def pick_block(blocks: list[dict], fmt: str | None) -> dict | None:
    if not blocks:
        return None

    # Prefer full workout blocks (tread + floor in one comment)
    full = [b for b in blocks if b["full"]]
    candidates = full if full else blocks

    if fmt:
        fmt_lower = fmt.lower().replace(" ", "")
        for b in candidates:
            if fmt_lower in b["label"].lower().replace(" ", ""):
                return b
        # Fall back to all blocks if format not found in full ones
        for b in blocks:
            if fmt_lower in b["label"].lower().replace(" ", ""):
                return b

    # Default: prefer 2G
    for b in candidates:
        if "2g" in b["label"].lower():
            return b

    return max(candidates, key=lambda b: b["score"])


def main():
    parser = argparse.ArgumentParser(description="Fetch OTF workout from Reddit")
    parser.add_argument("--date", help="Target date (YYYY-MM-DD), default: tomorrow")
    parser.add_argument("--format", dest="fmt", help="Workout format (e.g. 2G, 3G, Strength50)")
    args = parser.parse_args()

    if args.date:
        target = datetime.strptime(args.date, "%Y-%m-%d")
    else:
        target = datetime.now() + timedelta(days=1)

    date_str = target.strftime("%A, %B %-d, %Y")
    source = None

    posts = search_posts("Daily Workout", target)
    if posts:
        source = "Daily Workout"
    else:
        posts = search_posts("Early Intel", target)
        if posts:
            source = "Early Intel"

    if not posts:
        print(json.dumps({"error": f"No workout found for {date_str}"}))
        sys.exit(0)

    all_blocks = collect_workout_blocks(posts)
    chosen = pick_block(all_blocks, args.fmt)

    labels = list(dict.fromkeys(b["label"] for b in all_blocks if b["label"]))

    result = {
        "date": date_str,
        "source": source,
        "available_formats": labels,
    }

    if chosen:
        result["workout"] = {"label": chosen["label"], "content": chosen["body"]}
    else:
        result["error"] = f"No workout block found matching format: {args.fmt or 'any'}"

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
