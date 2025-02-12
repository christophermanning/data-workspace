with

amtrak_stations as (

  select * from {{ ref('stg_dot__amtrak_stations') }}

)

, bikeshare as (

  select * from {{ ref('stg_dot__bikeshare') }}

)

, final as (

  select
    s.code
    , s.name as station_name
    , s.location as station_location
    , st_x(s.geom) as station_lat
    , st_y(s.geom) as station_lon
    , b.name as bikeshare_name
    , st_x(b.geom) as bikeshare_lat
    , st_y(b.geom) as bikeshare_lon
    , st_distance_sphere(b.geom, s.geom)::int as dist

  from amtrak_stations s
  left join bikeshare b on 1 = 1

  where
    -- bikeshare farther than a mile from an amtrack station isn't relevant
    dist <= 1600

    and station_type = 'TRAIN'

  order by dist
)

select * from final
