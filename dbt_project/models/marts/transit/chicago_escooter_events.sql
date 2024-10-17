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
    , start_centroid_latitude as lat
    , start_centroid_longitude as lon
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
    , end_centroid_latitude as lat
    , end_centroid_longitude as lon
    , 'end' as event_action

  from trips

  where end_centroid_latitude is not null
)

, final as (

  select * from unioned

)

select * from final
