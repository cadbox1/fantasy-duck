sh download.sh;
npm run scrape;
duckdb < playing.sql;
duckdb < returning.sql;