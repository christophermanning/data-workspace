#!/bin/bash
duckdb -c "
ATTACH '/duckdb/dev.duckdb' AS duckdb;
ATTACH '/tmp/sqlite.sqlite3' AS sqlite3 (TYPE SQLITE);
INSTALL spatial;
LOAD spatial;

CREATE TABLE sqlite3.amtrak_stations AS (
  select
  station_id
  , location
  , lat
  , lon
  , bikeshare_name
  from duckdb.amtrak_stations_near_bikeshare
  group by 1,2,3,4,5
);
CREATE TABLE sqlite3.amtrak_routes AS (
  select
  name
  , ST_AsGeoJSON(geom) as geom
  from duckdb.amtrak_routes
);
CREATE TABLE sqlite3.bikeshare_stations AS (
  select
  station_id
  , bikeshare_lat
  , bikeshare_lon
  , dist
  from duckdb.amtrak_stations_near_bikeshare
  group by 1,2,3,4
);
"
cat /tmp/sqlite.sqlite3
rm /tmp/sqlite.sqlite3
