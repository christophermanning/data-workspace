with

chicago_wards as (

  select * from {{ ref('stg_chicago__wards') }}

)

, chicago_boundary as (

  select
    'chicago' as id
    , st_union_agg(geom) as geom
  from chicago_wards
  group by 1

)

, final as (

  select * from chicago_boundary

)

select * from final
