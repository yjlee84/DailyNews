# DailyNews

The Daily News briefs for https://euleridentity.com/news/. One issue a day: the highest-impact story, explained in two minutes, with sources.

## What is here

- `content/news/`: the issues (`YYYY-MM-DD.md`) and the section page `_index.md`
- `static/news/img/`: one photo per issue
- `docs/editorial.md`: voice, story selection, sourcing and photo rules
- `archetypes/news.md`: template for a new issue
- `.claude/skills/daily-brief/SKILL.md`: instructions for the scheduled agent that writes and publishes each issue
- `scripts/check_brief.py`: quality gates every brief must pass
- `scripts/notify-hub.sh`: WebSub ping after publishing
- `editorial-log.md`: the latest run's note (overwritten daily)
- `.github/workflows/rebuild-site.yml`: rebuilds the website when news changes

## How it reaches the website

The website is a separate repo, `yjlee84/Euleridentity`. It holds the Hugo site (layouts, config, the Lab pages) and includes this repo as the `daily-news` git submodule. Its `hugo.toml` mounts the news content, photos and archetype from there.

1. The 06:00 Berlin routine (a claude.ai routine named "euleridentity daily brief") runs the `daily-brief` skill in this repo and pushes the issue to `main`.
2. The "Rebuild euleridentity.com" workflow builds the site with the new content. If the build fails, nothing deploys and the live site keeps its last good version.
3. If the build passes, the workflow moves the `daily-news` pin in Euleridentity to the new commit and pushes it to Euleridentity `main`.
4. Cloudflare Pages builds and deploys that commit.

The workflow needs a repository secret named `EULERIDENTITY_TOKEN`: a fine-grained personal access token with Contents: Read and write on `yjlee84/Euleridentity`.

## Working on it

This repo has no Hugo site, so `scripts/check_brief.py` skips its two build gates here. To preview locally, work in a checkout of Euleridentity with this repo as its `daily-news` submodule.

Open work is in `TODO.md`.
