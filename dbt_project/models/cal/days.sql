{{ config(materialized='table') }}

-- generate one row per day

{% set START_DATE = '2024-01-01' %}
{% set END_DATE = '2025-12-31' %}

select

  i + 1 as id
  , (DATE '{{ START_DATE }}' + (INTERVAL(i) DAY))::DATE as date

from UNNEST(GENERATE_SERIES(0, DATE '{{ END_DATE }}' - DATE '{{ START_DATE }}')) s (i)
