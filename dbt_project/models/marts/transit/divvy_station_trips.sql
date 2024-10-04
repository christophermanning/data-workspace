with

trips as (

  select * from {{ ref('stg_divvy__trips') }}

)

, final as (

  select
    start_station_id
    , end_station_id
  from trips

  where
    start_station_id is not null
    and end_station_id is not null
    and start_station_id != end_station_id

)

select * from final
