# Editorial log — Tuesday, November 24, 2026

**Status:** Published No. 025  
**Live:** https://euleridentity.com/news/2026-11-24  
**Request indexing:** open https://search.google.com/search-console?resource_id=sc-domain%3Aeuleridentity.com , paste `https://euleridentity.com/news/2026-11-24` into the inspect bar at the top, press Enter, then click "Request indexing" (only needed if the automatic request failed)

## How today's candidates compare

| Story | Storyline · topic area | Reach | Severity | Duration | Changed today? |
|---|---|---|---|---|---|
| **Nvidia reinstates Jensen Huang; Nvidia +31%, Nasdaq +6.5%, S&P 500 +4.7%** | Nvidia leadership crisis · Technology | Very high (world’s most valuable chipmaker, index weight, global markets) | Medium-high | High (hearings Dec 1–3, board and SEC inquiries) | Yes: board decision Monday, record one-day value gain |
| Fighting near an Ituri hospital traps Ebola responders | Congo Ebola outbreak · Health | High regionally | Very high | High | Yes: clashes Sunday, staff sheltered over 24 hours |
| Indonesia candy factory fire, 24 dead and about 30 missing | Banten factory fire (new) · Climate and disasters | Low-medium | High | Low-medium | Yes: toll rose to 24 on Monday |
| CrowdStrike to buy Zscaler for $43.9 billion | Cybersecurity mergers (new) · Economy and markets | Medium | Low | Medium | Yes: deal announced (not verified) |
| Trump orders Justice Department to seek death penalty for child murders | US death penalty policy (new) · Politics and law | Medium | Medium | Medium | Yes (not verified) |
| UN calls for inquiry into attacks at Benghazi port | Libya conflict (new) · Conflict and diplomacy | Low-medium | Medium | Medium | Yes (not verified) |

Last seven briefs: Nov 17: Congo Ebola outbreak · Health; Nov 18: Nvidia leadership crisis · Technology; Nov 19: US measles resurgence · Health; Nov 20: Rohingya genocide case · Politics and law; Nov 21: AI stock selloff · Economy and markets; Nov 22: Chapo Isidro arrest · Crime and security; Nov 23: COP31 climate talks · Climate and disasters. Variety rules: no storyline is at its limit. “Nvidia leadership crisis” was used once in the previous six days (Nov 18), not yesterday, so today is its second and last use this week. Technology has one brief this week, Health two. No topic area is at its limit. The reinstatement is a board decision that reverses the Nov 18 position, so it is a major new event in any case.

## Why this story
The board’s reversal is a concrete decision with the widest reach today: it moved Nvidia by about 31% and lifted the Nasdaq 6.5% and the S&P 500 4.7%, after a week in which AI stocks had pushed indexes into a correction. It also raises open governance and national-security questions, with congressional hearings set for December 1 to 3. The Ebola story in Ituri ranked second on severity but its new development (staff trapped during clashes) is narrower in reach; it remains a strong candidate for later in the week, as the storyline has not run since Nov 17.

## Sources for key facts
- Board unanimously reinstated Huang as president and CEO, effective immediately — Nvidia 8-K press release (SEC), CNBC, NBC News, TechCrunch
- Board cited input from senior levels of the US government and no national security risk — Nvidia 8-K, CNBC, NBC News, TechCrunch
- Huang resigned less than two weeks earlier after admitting affairs, one with a woman US intelligence suspects is a Chinese spy — CNBC, NBC News, TechCrunch (resignation date differs: Nov 13 in CNBC, Nov 12 in TechCrunch and an NBC caption, so no exact date was used)
- Kress returns to CFO role — Nvidia 8-K, CNBC, TechCrunch
- Nvidia shares closed up about 31% — CNBC, NBC News, CBS News (hosted on Yahoo Finance), Investopedia (hosted on Yahoo Finance)
- Nasdaq +6.5%, S&P 500 +4.7% — CBS News (Yahoo Finance), Investopedia (Yahoo Finance)
- Close to $1 trillion in market value added — CBS News (“roughly $1 trillion”), Investopedia (“about $950 billion”)
- Friday tech selloff before the rally — NBC News, CBS News
- Huang quote “I take this responsibility with the greatest humility and renewed commitment” — CNBC, TechCrunch
- Jones said last week the board did not intend to reinstate him — NBC News, TechCrunch (and No. 019)
- Trump: “national treasure”, “did nothing wrong” — CNBC, NBC News
- Warren called the decision reckless — CNBC, NBC News
- Independent committee investigating reports Huang was targeted by a foreign intelligence effort — Nvidia 8-K, CNBC
- Closed-door interview with House committees Dec 1, public Senate Banking testimony Dec 3 — CNBC, NBC News
- No wire agency text in any of these articles.

## Photo
https://commons.wikimedia.org/wiki/File:Jensen_huang_stanford_2026-04-30_035.jpg · CC BY 4.0 (Commons notes a personality-rights restriction; used editorially, no endorsement implied) · credit used: Jensen Huang at Stanford University, 2026. Photo: Anders Eidesvik, CC BY 4.0. Saved as `static/news/img/jensen-huang-stanford-lecture-room-2026.jpg`.

## Check this
- **File-name collision, fixed.** The first commit (5a897dc) saved today’s photo as `jensen-huang-stanford-2026.jpg`, a name already used by No. 015 (Nov 14), and overwrote that image for about one minute. A follow-up commit (5475c29) restored the original file byte-for-byte from 4ac2cc6 and moved today’s photo to a new name. Both live images were checked against the repo by checksum after deploy. No history was rewritten. Consider adding a gate to `check_brief.py` that fails when a new brief’s image path already exists in git.
- Hugo could not be installed in this run (the install command was blocked by the environment), so no local build was attempted; the Action built and deployed the page successfully.
- Huang’s exact resignation date differs between outlets (Nov 12 vs Nov 13); the brief avoids it.
- S&P 500 “best day since April 2025” and Nvidia’s “biggest gain since 2003” were reported by Investopedia but not confirmed by a second full article, so they were left out.

## Run
- Gates: 21/21 passed (build gates skipped, no Hugo site in this repo)
- Pushed: 05:08 UTC (brief), 05:08:20 UTC (photo fix) · Verified live: 05:08:56 UTC, final version 05:09:03 UTC · Hub: 204
