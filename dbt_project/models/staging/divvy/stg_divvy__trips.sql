with

source as (

  select * from {{ source('divvy','divvy_trips') }}

)

select * from source
