with

source as (

  select * from {{ source('dot','bikeshare') }}

)

, renamed as (

  select
    longitude
    , latitude
    , year
    , system_name

  from source

)

, filtered as (

  select * from renamed
  where year = '2024'

)

select * from filtered
