-- the GTFS feed doesn't contain all the historical stations so derive them from the trip data
with

events as (

  select * from {{ ref('divvy_station_events') }}

)

, stations as (
  select * from {{ source('divvy','divvy_stations') }}

)

, stations_from_classic as (
  -- classic bikes report their lat/lon based on the station lat/lon so it's consistent
  select

    station_id
    , first(station_name) as name
    , avg(lat) as lat
    , avg(lon) as lon

  from events e
  where rideable_type = 'classic_bike'

  group by 1
  order by 1
)

, stations_from_electric as (
  -- ebikes report their lat/lon based on it's GPS location, not the station lat/lon, so it's slightly variable for each station event
  select

    e.station_id
    , first(station_name) as name
    , avg(e.lat) as lat
    , avg(e.lon) as lon

  from events e
  left join stations_from_classic s on e.station_id = s.station_id

  where s.station_id is null

  group by 1
)

, unioned as (

  select * from stations_from_classic
  union all
  select * from stations_from_electric

)

, final as (

  -- use the fields from the GTFS feed if they exist
  select
    s.station_id
    , case when ds.station_id is null then null else ds.station_id end as gtfs_station_id
    , ds.station_id is not null as active
    , case when ds.name is null then s.name else ds.name end as name
    , case when ds.lat is null then s.lat else ds.lat end as lat
    , case when ds.lon is null then s.lon else ds.lon end as lon
    , case when ds.capacity is null then null else ds.capacity end as capacity
  from unioned s

  left join stations ds on ds.short_name = s.station_id

)


select * from final
