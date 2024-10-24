with

source as (

  select * from {{ source('chicago', 'chicago_wards') }}

)

, transform as (

  select
    ward_id as id
    , the_geom::GEOMETRY as geom
  from source

)

select * from transform
