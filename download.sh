curl "https://fantasydraft.afl.com.au/json/draft/players.json" \
  -H "accept: application/json, text/plain, */*" \
  -b "X-SID=${COOKIE};" \
  --compressed \
  > data/players.json

curl "https://fantasydraft.afl.com.au/api/en/draft/league/teams/${LEAGUE}" \
  -H "accept: application/json, text/plain, */*" \
  -b "X-SID=${COOKIE};" \
  > data/teams.json

curl "https://fantasydraft.afl.com.au/api/en/draft/free-agents/list/${LEAGUE}" \
  -H "accept: application/json, text/plain, */*" \
  -b "X-SID=${COOKIE};" \
  > data/free-agents.json