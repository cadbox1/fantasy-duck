sh download.sh;
npm run scrape;
duckdb database.duckdb < players.sql;
duckdb database.duckdb < playing.sql;
duckdb database.duckdb < returning.sql;