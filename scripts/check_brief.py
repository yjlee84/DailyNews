#!/usr/bin/env python3
"""Publishing gates for a Daily News brief.

Usage: python3 scripts/check_brief.py YYYY-MM-DD

Exits 0 if every gate passes, 1 otherwise, printing one line per gate.
Run from the repository root. Hugo must be installed (the build gate runs it).
"""
import datetime as dt
import os
import re
import subprocess
import sys
from zoneinfo import ZoneInfo

ALLOWED_LICENSES = {"public domain", "cc0", "cc by", "cc by-sa"}
TOPIC_AREAS = {
    "Conflict and diplomacy", "Economy and markets", "Health", "Science and space", "Technology",
    "Climate and disasters", "Politics and law", "Society and culture", "Crime and security",
    "Other",
}
FIRST_PERSON = re.compile(r"\b(I|me|my|mine|we|We|us|our|Our|ours|myself|ourselves)\b")


def front_matter(text):
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.S)
    if not m:
        return None, text
    return m.group(1), m.group(2)


def scalar(fm, key, indent=""):
    m = re.search(rf"^{indent}{key}:[ \t]*(.*)$", fm, re.M)
    if not m:
        return ""
    v = m.group(1).strip()
    if len(v) >= 2 and v[0] == v[-1] and v[0] in "\"'":
        v = v[1:-1]
    return v


def jpeg_size(path):
    """Return (width, height) of a JPEG by reading its frame header, or None."""
    with open(path, "rb") as f:
        data = f.read()
    if data[:2] != b"\xff\xd8":
        return None
    i = 2
    while i + 9 < len(data):
        if data[i] != 0xFF:
            i += 1
            continue
        marker = data[i + 1]
        if marker in (0xD8, 0x01) or 0xD0 <= marker <= 0xD7:
            i += 2
            continue
        length = int.from_bytes(data[i + 2:i + 4], "big")
        if marker in (0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7, 0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF):
            h = int.from_bytes(data[i + 5:i + 7], "big")
            w = int.from_bytes(data[i + 7:i + 9], "big")
            return w, h
        i += 2 + length
    return None


def strip_quotes(text):
    # Quoted speech from sources may use first person; only the brief's own voice is checked.
    text = re.sub(r"“[^”]*”", " ", text)
    text = re.sub(r'"[^"\n]*"', " ", text)
    return text


def main():
    if len(sys.argv) != 2 or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", sys.argv[1]):
        print("usage: check_brief.py YYYY-MM-DD")
        return 1
    date = sys.argv[1]
    path = f"content/news/{date}.md"
    results = []

    def gate(name, ok, detail=""):
        results.append((ok, name, detail))

    if not os.path.exists(path):
        print(f"FAIL  brief file exists ({path})")
        return 1
    text = open(path, encoding="utf-8").read()
    fm, body = front_matter(text)
    gate("front matter present", fm is not None)
    if fm is None:
        fm = ""

    title = scalar(fm, "title")
    desc = scalar(fm, "description")
    gate("title present", bool(title))
    gate("headline has no closing period", bool(title) and not title.endswith("."), title)
    gate("description present", bool(desc))
    gate("not a draft", not re.search(r"^draft:\s*true", fm, re.M))

    issue = scalar(fm, "issue")
    gate("issue number present", issue.isdigit(), issue)

    # Variety labels are required from 2026-11-18 on (earlier briefs are labelled only for the last seven days).
    if date >= "2026-11-18":
        storyline = scalar(fm, "storyline")
        topic = scalar(fm, "topic")
        gate("storyline label present", bool(storyline))
        gate("topic area is one of the allowed values", topic in TOPIC_AREAS, topic or "(missing)")

    raw_date = scalar(fm, "date")
    try:
        when = dt.datetime.fromisoformat(raw_date.replace("Z", "+00:00"))
        gate("date matches file name (Berlin time)", when.astimezone(ZoneInfo("Europe/Berlin")).date().isoformat() == date, raw_date)
        gate("date is not in the future", when <= dt.datetime.now(dt.timezone.utc), raw_date)
    except ValueError:
        gate("date is valid", False, raw_date)

    src = scalar(fm, "src", "  ")
    gate("image path set", src.startswith("/news/img/"), src)
    img = os.path.join("static", src.lstrip("/"))
    exists = bool(src) and os.path.exists(img)
    gate("image file exists", exists, img)
    if exists:
        size = jpeg_size(img)
        if size:
            w, h = size
            gate("image is 4:3", abs(w / h - 4 / 3) < 0.01, f"{w}x{h}")
            gate("image width/height match front matter",
                 str(w) == scalar(fm, "width", "  ") and str(h) == scalar(fm, "height", "  "), f"{w}x{h}")
        else:
            gate("image is a readable JPEG", False, img)
    gate("image alt text present", bool(scalar(fm, "alt", "  ")))
    credit = scalar(fm, "credit", "  ")
    gate("photo credit present", "Photo:" in credit, credit[:80])
    lic = scalar(fm, "license", "  ").lower()
    gate("photo license allowed", lic in ALLOWED_LICENSES, lic or "(missing)")

    urls = re.findall(r"^\s+url:\s*(https?://\S+)\s*$", fm, re.M)
    names = re.findall(r"^\s+- name:\s*(.+)$", fm, re.M)
    gate("at least two sources with links", len(urls) >= 2 and len(names) >= 2, f"{len(urls)} links")
    domains = {re.sub(r"^www\.", "", u.split("/")[2]) for u in urls}
    gate("sources from at least two different sites", len(domains) >= 2, ", ".join(sorted(domains)))

    gate("has 'Why it matters' section", re.search(r"^## Why it matters\s*$", body, re.M) is not None)
    voice = strip_quotes(" ".join([title, desc, body]))
    hits = sorted(set(FIRST_PERSON.findall(voice)))
    gate("no first person in the brief's own voice", not hits, ", ".join(hits))

    # Soft style warnings. They are printed but never fail the brief. The skill asks for plain
    # punctuation: no em dashes, and at most one semicolon or colon (none is better), outside quotes.
    plain = re.sub(r"https?://\S+|\d:\d\d?", " ", voice)
    warnings = []
    dashes = plain.count("—")
    if dashes:
        warnings.append(f"em dash used {dashes}x (never allowed in a brief)")
    marks = plain.count(";") + plain.count(":")
    if marks > 1:
        warnings.append(f"{marks} semicolons or colons outside quotes (limit one, none is better)")

    build = subprocess.run(["hugo", "build", "--quiet", "--destination", "/tmp/brief-check-public"],
                           capture_output=True, text=True)
    gate("site builds", build.returncode == 0, (build.stderr or build.stdout).strip()[:200])
    gate("brief page generated", os.path.exists(f"/tmp/brief-check-public/news/{date}.html"))

    failed = 0
    for ok, name, detail in results:
        print(f"{'PASS' if ok else 'FAIL'}  {name}" + (f"  [{detail}]" if detail and not ok else ""))
        failed += not ok
    print(f"\n{len(results) - failed}/{len(results)} gates passed")
    for w in warnings:
        print(f"WARN  {w}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
