with

source as (

  select * from {{ source('chicago','escooter_trips') }}

)

select * from source
