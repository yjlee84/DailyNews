# TODO

Daily News moved out of Euleridentity on 2026-11-20. The site now builds with this repo as the `daily-news` submodule. The 06:00 Berlin routine (`trig_01CsBHMjicfypUAmxbEsLHkz`, https://claude.ai/code/routines/trig_01CsBHMjicfypUAmxbEsLHkz) was repointed to this repo on the same day. See `MIGRATION.md` for the background.

## 1. Check the first run through this repo (2026-11-21, 06:00 Berlin)

- The brief is in this repo on `main` (`content/news/2026-11-21.md` and its image).
- The "Rebuild euleridentity.com" workflow ran and passed.
- Euleridentity `main` has a new "Update Daily News to <sha>" commit, and the Cloudflare Pages check on it succeeded.
- `https://euleridentity.com/news/2026-11-21` shows the issue.
- If something failed, read the routine's run log first (`list_runs`, then `get_run_log` on the routine above). The likeliest causes are the routine not being able to push to this repo, or the workflow rejecting the build.

## 2. Delete the originals from Euleridentity (only after step 1 passes)

Remove from `~/Work/Projects/Euleridentity`:

- `content/news/`
- `static/news/img/`
- `docs/editorial.md` and `docs/daily-brief.md`
- `editorial-log.md`
- `archetypes/news.md`
- `scripts/check_brief.py` and `scripts/notify-hub.sh`
- `.claude/skills/daily-brief/`

Keep the `daily-news` submodule and the `[module]` mounts in `hugo.toml`. Also update the Euleridentity `README.md` structure section, which still describes these files as local. Run `hugo` afterwards and compare `/news/` with the live site before pushing.

## 3. Reminders

- The `EULERIDENTITY_TOKEN` secret (a fine-grained token with Contents: Read and write on Euleridentity) expires on the date chosen when it was created. Renew it and update the secret in this repo's Actions settings before then. When it expires, the rebuild workflow fails at checkout and new issues stop deploying.
- The Google indexing job (`scripts/index-on-login.sh`) stays in Euleridentity. It is a launchd agent pinned to that path.

## 4. Optional

- Bump `actions/checkout@v4` in `.github/workflows/rebuild-site.yml`. GitHub warns that Node.js 20 is deprecated.
- Decide whether `DRY RUN` still needs a preview. It has none now, because the rebuild workflow only runs on `main`.
