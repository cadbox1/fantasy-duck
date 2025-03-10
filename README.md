# Fantasy Duck 🔮🦆

Download data from AFL Fantasy Draft and processes it with DuckDB.

I want to see the highest performing free agents that are playing this week so I can recruit them.

There's no way to filter by playing status in the new UI but we can pull all the data down and process it ourselves.

## Quick Start

```
LEAGUE=4465 COOKIE= sh run.sh
```

Other Commands

```
LEAGUE=4465 COOKIE= sh download.sh
duckdb
.read query.sql
```

## Getting Started

1. Install DuckDB.

```
curl https://install.duckdb.org | sh
```

1. Login to your draft competition in Chrome.
1. Open Chrome Dev Tools.
1. Go to the Application Tab, Cookies and copy the X-SID value.
1. Run the application with your league and cookie. Replace 111 and FFF.

```
LEAGUE=111 COOKIE=FFF sh run.sh
```
