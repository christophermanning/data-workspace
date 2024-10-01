with

bikeshare as (

  select * from {{ ref('stg_dot__bikeshare') }}

)

, final as (

  select
    name
    , year
    , COUNT(*) as num_stations
  from bikeshare

  group by 1, 2

  order by name
)

select * from final
