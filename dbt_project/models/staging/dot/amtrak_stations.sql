with

source as (

  select * from {{ source('dot','amtrak_stations') }}

)

, renamed as (

  select
    lon as longitude
    , lat as latitude
    , code as code
    , stntype as station_type
    , stationname as station_name

  from source

)

, filtered as (

  select * from renamed

)

select * from filtered
