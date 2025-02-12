with

source as (

  select * from {{ source('dot','amtrak_routes') }}

)

, optimized as (

  select
    name
    -- make all geoms MultiLineString for consistent access
    , ST_MULTI(ST_SIMPLIFY(geom, 0.1)) as geom

  from source

)

select * from optimized
