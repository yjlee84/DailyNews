#!/bin/sh
# Tell the WebSub hub that the feed changed, so subscribers (including Google) re-fetch it.
# Run after a push, once the new version is live on euleridentity.com.
set -e
FEED="https://euleridentity.com/feed.xml"
HUB="https://pubsubhubbub.appspot.com/"
code=$(curl -s -o /dev/null -w '%{http_code}' -X POST "$HUB" \
  --data-urlencode "hub.mode=publish" --data-urlencode "hub.url=$FEED")
if [ "$code" = "204" ]; then echo "Hub notified ($code)"; else echo "Hub returned $code" >&2; exit 1; fi
