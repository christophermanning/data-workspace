with

source as (

  select * from {{ source('dot','amtrak_stations') }}

)

, renamed as (

  select
    lat as latitude
    , lon as longitude
    , ST_POINT(lat, lon) as geom
    , code as code
    , stntype as station_type
    , stationname as name

  from source

)

, filtered as (

  select * from renamed

)

select * from filtered
