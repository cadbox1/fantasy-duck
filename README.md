# Fantasy Duck Sauce 🔮🦆🍅

Download data from AFL Fantasy Draft and processes it with DuckDB.

I want to see the highest performing free agents that are playing this week so I can recruit them.

There's no way to filter by playing status in the new UI but we can pull all the data down and process it ourselves.

## Quick Start

```
LEAGUE=4465 COOKIE= sh run.sh
```
```
streamlit run app.py
```

Other Commands
```
duckdb database.duckdb
.read players.sql;
select * from players;
```
```
duckdb database.duckdb
.read playing.sql;
```
```
duckdb database.duckdb
.read returning.sql;
```
```
LEAGUE=4465 COOKIE= sh download.sh
```
```
npm install
npm run scrape
```

## Getting Started

1. Install DuckDB.

```
curl https://install.duckdb.org | sh
```
1. Install node dependencies.
```
npm install
```
1. Install python dependencies.
```
pip install -r requirements.txt
```
1. Login to your draft competition in Chrome.
1. Open Chrome Dev Tools.
1. Go to the Application Tab, Cookies and copy the X-SID value.
1. Run the application with your league and cookie. Replace 111 and FFF.

```
LEAGUE=111 COOKIE=FFF sh run.sh
```
