with

source as (

  select
    id
    , ST_GEOMFROMGEOJSON(geom) as geom
  from {{ source('census','census_geo_boundaries') }}

)

select * from source
