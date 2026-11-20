# Moving Daily News out of Euleridentity

This repo was created on 2026-11-20 as a copy of the Daily News parts of Euleridentity. Euleridentity is unchanged and still publishes. Nothing here is live until the cutover below is done.

## What is in this repo

- `content/news/`: the issues (`YYYY-MM-DD.md`) and `_index.md`
- `static/news/img/`: issue photos
- `docs/editorial.md`, `docs/daily-brief.md`: editorial rules and a pointer to the skill
- `archetypes/news.md`: template for a new issue
- `.claude/skills/daily-brief/SKILL.md`: instructions for the scheduled agent
- `scripts/check_brief.py`, `scripts/notify-hub.sh`: checks and WebSub ping
- `editorial-log.md`: latest run note

## What stays in Euleridentity

The Hugo site (`hugo.toml`, `layouts/`, `static/` other than `news/`), the Lab content, and the Google indexing job (`scripts/index-on-login.sh`, `.claude/skills/index-site/`, `indexing-log.md`). The indexing job is a launchd agent pinned to the Euleridentity path.

## Verified

A scratch copy of Euleridentity with `content/news` and `static/news` removed and mounted from this repo builds byte-identical output to the current site (checked with `diff -r`). Mount config used:

```toml
[module]
  [[module.mounts]]
    source = "content"
    target = "content"
  [[module.mounts]]
    source = "static"
    target = "static"
  [[module.mounts]]
    source = "layouts"
    target = "layouts"
  [[module.mounts]]
    source = "archetypes"
    target = "archetypes"
  [[module.mounts]]
    source = "<path to this repo>/content/news"
    target = "content/news"
  [[module.mounts]]
    source = "<path to this repo>/static/news"
    target = "static/news"
  [[module.mounts]]
    source = "<path to this repo>/archetypes"
    target = "archetypes"
```

## Cutover (not done)

1. Create a GitHub remote for this repo and push `main`.
2. Make Cloudflare Pages build see both repos. A relative mount path does not work across two clones, so add this repo to Euleridentity as a git submodule (for example at `daily-news/`) and mount from there.
3. Repoint the scheduled daily-brief agent to this repo. Its paths (`content/news/`, `static/news/img/`) already match this layout. It must also trigger an Euleridentity rebuild after pushing, because the site builds from the other repo.
4. Check that `scripts/check_brief.py` and the skill's `hugo` verification step still work, since this repo has no layouts of its own.
5. After one successful publish through the new setup, delete the originals from Euleridentity.
