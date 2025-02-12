with

final as (

  select * from {{ ref('stg_dot__amtrak_routes') }}

)

select * from final
