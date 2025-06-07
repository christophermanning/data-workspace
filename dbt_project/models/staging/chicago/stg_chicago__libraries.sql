with

source as (

  select * from {{ source('chicago', 'chicago_libraries') }}

)

, transform as (

  select
    case
      -- fix misspelled branch name
      when branch_ = 'Harold Washtington Library Center'
        then
          'Harold Washington Library Center'
      else
        branch_
    end as branch
    , ST_GEOMFROMTEXT('POINT' || REGEXP_EXTRACT(REPLACE(location, ',', ''), '\(.*?\)'))
      as geom
  from source

)

select * from transform
