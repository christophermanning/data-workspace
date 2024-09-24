with

source as (

  select * from {{ source('dot','bikeshare') }}

)

, renamed as (

  select
    latitude as lat
    , longitude as lon
    , ST_POINT(lat, lon) as geom
    , year
    , system_name as name

  from source

)

, filtered as (

  select * from renamed
  where year = '2024'

)

select * from filtered
