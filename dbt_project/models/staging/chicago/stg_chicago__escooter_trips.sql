with

source as (

  select * from {{ source('chicago','chicago_escooter_trips') }}

)

select * from source
