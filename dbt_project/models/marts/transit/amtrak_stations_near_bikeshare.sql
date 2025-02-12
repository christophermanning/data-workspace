with

amtrak_stations as (

  select * from {{ ref('stg_dot__amtrak_stations') }}

)

, bikeshare as (

  select * from {{ ref('stg_dot__bikeshare') }}

)

, final as (

  select
    code as station_id
    , station_name as name
    , station_location as location
    , station_lat as lat
    , station_lon as lon
    , bikeshare_name
    , bikeshare_lat
    , bikeshare_lon
    , dist
  from {{ ref('int_amtrak_stations_to_bikeshare') }}

  -- one lap of a standard running track is the threshold for considering it to be nearby
  where dist <= 400

  group by 1, 2, 3, 4, 5, 6, 7, 8, 9
  order by code

)

select * from final
