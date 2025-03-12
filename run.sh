sh download.sh;
npm run scrape;
duckdb database.db < players.sql;
duckdb database.db < playing.sql;
duckdb database.db < returning.sql;