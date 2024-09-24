with

source as (

    select * from {{ source('dot','amtrak_stations') }}

),

renamed as (

    select
      lon as longitude
    , lat as latitude
    , Code as code
    , StnType as station_type
    , StationName as station_name

    from source

),

filtered as (

  select * from renamed

)

select * from filtered
