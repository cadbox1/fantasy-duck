# Fantasy Duck

Download data from AFL Fantasy Draft and processes it with DuckDB.

I want to see players with the highest average score that are playing this week but the new UI doesn't let you.

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
