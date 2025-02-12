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
    , TRIM(REGEXP_REPLACE(system_name, '\((.*)\)', '')) as name
    , TRIM(REGEXP_EXTRACT(system_name, '.*\((.*)\)', 1)) as info
    , bike_id as bike_id
    , city as city
    , state as state

  from source

)

, filtered as (

  select * from renamed
  where year = '2024'

)

select * from filtered
