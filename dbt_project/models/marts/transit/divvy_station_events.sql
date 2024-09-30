with

trips as (

  select * from {{ ref('stg_divvy__trips') }}

)

, unioned as (

  select
    start_station_name as station_name
    , start_station_id as station_id
    , started_at as event_at
    , start_lat as lat
    , start_lng as lon
    , ST_POINT(lat, lon) as geom
    , rideable_type
    , 'start' as event_action
    , member_casual

  from trips

  union all

  select
    end_station_name as station_name
    , end_station_id as station_id
    , ended_at as event_at
    , end_lat as lat
    , end_lng as lon
    , ST_POINT(lat, lon) as geom
    , rideable_type
    , 'end' as event_action
    , member_casual

  from trips

)

, final as (

  select * from unioned

  -- ignore outside of station docks/unlocks
  where station_id is not null

)

select * from final
