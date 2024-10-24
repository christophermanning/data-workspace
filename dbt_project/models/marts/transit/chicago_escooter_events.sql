with

trips as (

  select * from {{ ref('stg_chicago__escooter_trips') }}

)

, unioned as (

  select
    trip_id
    , start_time as event_at
    , trip_distance
    , trip_duration
    , vendor
    , start_community_area_name as community_area_name
    , start_community_area_number as commmunity_area_number
    , ST_POINT(start_centroid_longitude, start_centroid_latitude)::GEOMETRY as geom
    , 'start' as event_action

  from trips

  where start_centroid_latitude is not null

  union all

  select
    trip_id
    , end_time as event_at
    , trip_distance
    , trip_duration
    , vendor
    , end_community_area_name as community_area_name
    , end_community_area_number as commmunity_area_number
    , ST_POINT(end_centroid_longitude, end_centroid_latitude)::GEOMETRY as geom
    , 'end' as event_action

  from trips

  where end_centroid_latitude is not null
)

, final as (

  select * from unioned

)

select * from final
