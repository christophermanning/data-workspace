with

amtrak_stations as (

  select * from {{ ref('stg_dot__amtrak_stations') }}

)

, bikeshare as (

  select * from {{ ref('stg_dot__bikeshare') }}

)

, stations as (

  select
    s.code
    , s.name as station_name
    , b.name
    , ST_DISTANCE_SPHERE(b.geom, s.geom)::int as dist

  from amtrak_stations s
  left join bikeshare b on 1 = 1

  where
    dist < 400

    and station_type = 'TRAIN'

  order by dist
)

, final as (

  select
    code
    , station_name
    , name
    , COUNT(*) as num_stations
    , MIN(dist) as min_distance
  from stations
  group by 1, 2, 3
  order by code

)

select * from final
