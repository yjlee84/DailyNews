---
name: daily-brief
description: Research, write and publish one Daily News brief for euleridentity.com, then write the editorial note. Used by the 06:00 Berlin scheduled routine, and manually for dry runs.
disable-model-invocation: true
argument-hint: "[LIVE | DRY RUN]"
---

# Daily brief

These are the complete instructions for writing and publishing one Daily News brief for euleridentity.com. You may start with no other context: read this file, then `docs/editorial.md`, and follow both exactly.

The run either **publishes** one brief or **skips** with a reason. In both cases it ends by overwriting `editorial-log.md` at the repository root.

## Mode

- **LIVE**: used when the prompt says `LIVE` (the scheduled routine). Publish to `main`, which deploys to https://euleridentity.com. No approval step.
- **INTERACTIVE**: used when the prompt names no mode, i.e. a person is running this in a session. Do Steps 0 to 5, then stop and show the brief, the gate results and the note draft. Commit and push only after the person says yes.
- **DRY RUN**: used when the prompt says `DRY RUN`. Do everything the same, but push to a new branch `dry-run/<date>` instead of `main`, skip the live check and the hub notification, and say "DRY RUN" at the top of the note. Cloudflare builds a preview of that branch at `https://dry-run-<date>.euleridentity.pages.dev`; check that address instead of the live site (it may take up to two minutes).

## Step 0: Set up

1. `DATE=$(TZ=Europe/Berlin date +%F)`. This is the issue date and file name.
2. If `content/news/$DATE.md` already exists on `main`:
   - LIVE: stop. Write a note saying today's brief already exists, and do nothing else.
   - DRY RUN: continue, and on the dry-run branch replace that file with your own brief (keep its `issue` number and remove its old image only on that branch). Never touch `main`.
3. Install Hugo 0.168.0 (extended) if `hugo version` does not report it:
   ```sh
   curl -sL -o /tmp/hugo.tgz https://github.com/gohugoio/hugo/releases/download/v0.168.0/hugo_extended_0.168.0_linux-amd64.tar.gz
   tar -xzf /tmp/hugo.tgz -C /tmp hugo && sudo mv /tmp/hugo /usr/local/bin/ 2>/dev/null || mv /tmp/hugo ~/bin/ 2>/dev/null || export PATH=/tmp:$PATH
   hugo version
   ```
4. Make sure Python can crop images: `python3 -c "from PIL import Image"`. If that fails (the system Pillow in the cloud environment is known to be broken), use a virtualenv: `python3 -m venv /tmp/venv && /tmp/venv/bin/pip install -q pillow`, then run image scripts with `/tmp/venv/bin/python`.
5. Git identity for commits: `git config user.name "euleridentity daily brief"` and `git config user.email "72490099+yjlee84@users.noreply.github.com"`.

## Step 1: Find candidates

Search broadly before choosing. At minimum run these searches (replace the date with today's, in words):
- top news <date>
- world news <date>
- markets oil stocks <date>
- the latest on any story the previous three briefs covered (read `content/news/` for them)
- at least three searches in topic areas and regions that the last seven briefs did not cover. Choose them after reading the briefs. Rotate through areas such as health, science and space, technology, climate and disasters, economy beyond markets, society and culture, and regions such as Africa, Latin America, South and Southeast Asia, the Middle East, Europe

First read the `storyline:` and `topic:` front matter of the last seven briefs in `content/news/` (dated within the previous seven days) and write the list down for the note. Use the stored labels as they are and do not relabel earlier briefs. If a brief in that window has no labels, label it yourself in the note only and do not edit the file. Do not assume any fixed list of subjects.

List five to seven candidate stories. At least two must come from a storyline and topic area that the last seven briefs did not use. Give each candidate a storyline name and a topic area. Score each on the four tests in `docs/editorial.md`: reach, severity, duration, and whether something changed in the last 24 hours (or, for a slow story the site has not covered in seven days, whether there is a new development). Ease of sourcing must not influence the choice.

Pick the highest-impact story that is allowed by the variety rules in `docs/editorial.md`: no storyline more than twice in seven days and not two days in a row unless there is a major new event, and no more than three briefs from one topic area in seven days (Other is not counted) unless no candidate from another area is close in impact. A continuing storyline that is not at its limit can still be picked if it clearly is the biggest story and something new happened. If the top candidate is blocked by a rule, say so in the note and pick the best remaining candidate.

If no candidate can be confirmed twice in Step 2, move to the next-ranked candidate. Do not fall back to a "where things stand" brief on a storyline that is at its limit.

## Step 2: Verify

- Open (fetch) the actual articles, not just search summaries. Every fact in the brief must appear in at least one article you read in full **and** be confirmed by a second, independent source (a different outlet, not a copy of the same wire story under another name where avoidable).
- Attribute claims from unnamed officials ("according to US officials who spoke to…").
- Leave out anything that cannot be confirmed twice, including prices and casualty figures. Both confirmations must come from articles read in full today; search-result summaries and sources from earlier briefs do not count.
- If sources conflict on a fact, either say so plainly in the brief or leave the fact out.
- Keep a list of every key fact and the sources that confirmed it, for the note. Note which wire agency, if any, each article came from.

**Skip rule:** if no candidate can be confirmed by two independent sources, do not publish. Go to Step 7 and write a SKIPPED note.

## Step 3: Photo

- Search Wikimedia Commons through its API (`https://commons.wikimedia.org/w/api.php`, generator=search, namespace 6, prop=imageinfo with extmetadata). Send the header `User-Agent: euleridentity-site/1.0` and nothing else identifying.
- Allowed licenses only: **public domain, CC0, CC BY, CC BY-SA**. Read the license from the file's metadata, not from guesses. No logos, no photos that imply endorsement, no images of private individuals as the subject.
- Prefer a photo directly related to the story: the place, the institution, or the subject. A good satellite image (NASA, ESA with CC BY) is fine for geography.
- Download from `upload.wikimedia.org`, then crop to exactly 4:3 and resize to 1440×1080 with Pillow, keeping the subject in frame. Save as JPEG (quality about 82) to `static/news/img/<short-descriptive-name>.jpg`.
- Credit (caption) format:
  - Licensed: `Place, year. Photo: <a href="COMMONS_FILE_PAGE" target="_blank" rel="noopener">Author</a>, <a href="LICENSE_DEED_URL" target="_blank" rel="noopener">CC BY 4.0</a>.`
  - Public domain (e.g. NASA): `Place, year. Photo: <a href="COMMONS_FILE_PAGE" target="_blank" rel="noopener">NASA</a>.` with no license text.
  - Credit government photos to the agency or institution (e.g. NASA, Architect of the Capitol, U.S. Navy), not to the uploader or Flickr account name.
- Wikimedia sometimes answers HTTP 429 (rate limit). Wait 20 seconds and retry, up to five times.

**Skip rule:** if no suitable freely licensed photo exists, do not publish. Go to Step 7 and write a SKIPPED note.

## Step 4: Write

Create `content/news/$DATE.md`. Copy the structure of the most recent brief in `content/news/` exactly. Front matter:

```yaml
---
title: "Headline without a closing period"
description: "One or two sentences used in the issue list, search results and the feed."
date: <current UTC time minus 5 minutes, e.g. 2026-11-04T04:55:00Z>
issue: <highest existing issue number + 1>
storyline: "<short noun phrase; reuse an existing name from the last seven briefs if this is more of the same story>"
topic: "<exactly one allowed value from the Variety section of docs/editorial.md>"
readTime: 2
image:
  src: /news/img/<file>.jpg
  width: 1440
  height: 1080
  alt: "Plain description of what the photo shows."
  license: public domain | cc0 | cc by | cc by-sa
  credit: '<caption, see Step 3>'
sources:
  - name: "Outlet name"
    url: https://...
  - name: "Outlet name"
    url: https://...
---
```

Body, about 300 words, following `docs/editorial.md`:
1. Paragraph 1: what happened, with figures.
2. Paragraph 2: context, reactions, what is disputed.
3. `## Why it matters`, then one paragraph starting "This is today’s highest-impact story because…", ending with what is still uncertain or what to watch.

### Style: write like a wire reporter

The brief should read like a human news writer: plain, direct, specific.

- **Lede:** the first sentence states what happened in 30 words or fewer, with the actor and the main figure. Attribution and detail follow in later sentences.
- **Sentences:** vary the length, but keep nearly all under 35 words. Split a sentence that carries three figures.
- **Punctuation:** avoid semicolons and colons in the body. Use a full stop and start a new sentence. Allowed: a colon inside a quotation, a time (09:30), or a ratio. Never use em dashes (—). At most one semicolon or colon per brief, and none is better. Rewrite instead of squeezing a list into one sentence.
- **Transitions:** prefer plain connectors (“But”, “Meanwhile”, “On Monday”) over stock phrases (“Separately,”, “Traders focused on…”, “It is worth noting”, “amid”, “landscape”, “navigate”, “underscores”).
- **Quotes:** use one short direct quotation from a named person when a source article has a good one. Do not invent or paraphrase inside quotation marks.
- **Why it matters:** keep the required opening (“This is today’s highest-impact story because…”). End with the open questions as a plain sentence such as “Still unclear is whether…” or “Watch for…”, not “What is still uncertain:”.
- **Read it back:** read the finished brief aloud in your head. Reword anything a reporter would not say, and avoid repeated sentence openings. Do this before running the gates, and never change a figure, name or attribution while rewording.

House rules that are easy to miss: no first person (I, we, my, our, us) outside direct quotes; curly quotes and apostrophes (“ ” ’); no bold lead paragraph; no inline source tags; the `date` must not be in the future or Hugo silently drops the page.

`sources` names are the outlet whose page the link opens, not the wire agency: `"PBS NewsHour"`, not `"AP"` or `"AP via PBS NewsHour"`. One exception: a Reuters story is named `"Reuters"` wherever it is hosted, as long as the page itself credits Reuters. Never write "via".

## Step 5: Check

Run `python3 scripts/check_brief.py $DATE`. Every gate must pass. Fix what you can and re-run. Lines starting with `WARN` are style warnings, not gates (no em dashes, at most one semicolon or colon outside quotes). Fix them if it is easy and does not change a figure, name or attribution, but they never block publishing. If a gate still fails, do not publish: go to Step 7 and write a SKIPPED note listing the failed gates. Never edit the check script to make a brief pass.

## Step 6: Publish

(INTERACTIVE: only after the person approves, then treat it as LIVE.)

1. Commit only the new brief and its image:
   `git add content/news/$DATE.md static/news/img/<file>.jpg`
   Commit message: `Daily News No. NNN: <headline>`
2. LIVE: `git push origin main`. DRY RUN: `git push origin HEAD:dry-run/$DATE`.
3. Verify: poll the page every 15 seconds for up to 4 minutes until it returns 200 and contains `No. NNN`:
   - LIVE: `https://euleridentity.com/news/$DATE`
   - DRY RUN: `https://dry-run-$DATE.euleridentity.pages.dev/news/$DATE`
4. LIVE only, once the page is verified: run `sh scripts/notify-hub.sh` (expects "Hub notified (204)").

Never force-push, never rewrite history, never edit earlier briefs or any other file.

## Step 7: Write the note

Overwrite `editorial-log.md` at the repository root (only today's note is kept; replace the whole file). Use this format:

```markdown
# Editorial log — <Weekday, Month D, YYYY>

**Status:** Published No. NNN | SKIPPED | DRY RUN  
**Live:** https://euleridentity.com/news/<DATE>  
**Request indexing:** open https://search.google.com/search-console?resource_id=sc-domain%3Aeuleridentity.com , paste `https://euleridentity.com/news/<DATE>` into the inspect bar at the top, press Enter, then click "Request indexing" (only needed if the automatic request failed)

## How today's candidates compare

| Story | Storyline · topic area | Reach | Severity | Duration | Changed today? |
|---|---|---|---|---|---|
| **<chosen story>** | … | … | … | … | … |
| <runner-up> | … | … | … | … | … |

Last seven briefs: <date: storyline · topic area, one entry per brief>. Variety rules: <which storylines or topic areas are at their limit, and whether a major new event lifted one>.

## Why this story
<two or three sentences; if a higher-ranked candidate was blocked by the variety rule, say which and why>

## Sources for key facts
- <fact> — <outlet>, <outlet> (name the wire agency where there is one, and the host for a Reuters story, e.g. "PBS NewsHour (AP)", "Reuters (hosted on Al Jazeera)")

## Photo
<Commons file page> · <license> · credit used: <caption text>

## Check this
- <anything uncertain, conflicting, or likely to change today; "Nothing flagged." if none>

## Run
- Gates: <N>/<N> passed
- Pushed: <UTC time> · Verified live: <UTC time> · Hub: <204 or reason>
```

For a SKIPPED run, keep the candidates table and replace the sources and photo sections with **Why it was skipped**, listing the exact reason (no story confirmed twice, no licensed photo, or the failed gates).

Commit and push the note the same way as the brief (LIVE: to `main`; DRY RUN: to the `dry-run/<date>` branch). Commit message: `Editorial log <DATE>`.
