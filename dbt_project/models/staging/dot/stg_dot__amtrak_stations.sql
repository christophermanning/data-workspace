with

source as (

  select * from {{ source('dot','amtrak_stations') }}

)

, renamed as (

  select
    lat as latitude
    , lon as longitude
    , ST_POINT(lat, lon) as geom
    , TRIM(code) as code
    , TRIM(stntype) as station_type
    , TRIM(name) as name
    , TRIM(stationname) as location

  from source

)

, filtered as (

  select * from renamed

)

select * from filtered
