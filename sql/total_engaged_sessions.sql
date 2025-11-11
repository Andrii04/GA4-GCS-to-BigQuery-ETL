WITH flattened AS (
  SELECT
    event_timestamp,
    param.key AS paramKey,
    param.value.string_value AS string_value,
    SAFE_CAST(param.value.int_value AS INT64) AS int_value
  FROM
    `gcp-project.andrea_monforte_dataset.ga4_data`,
    UNNEST(event_params) AS param
),
pivoted AS (
  SELECT
    event_timestamp,
    MAX(CASE WHEN paramKey = 'session_engaged' THEN string_value END) AS session_engaged,
    MAX(CASE WHEN paramKey = 'ga_session_id' THEN int_value END) AS ga_session_id
  FROM
    flattened
  GROUP BY
    event_timestamp
)
SELECT
  COUNT(DISTINCT ga_session_id) AS engaged_sessions
FROM
  pivoted
WHERE
  session_engaged = '1'
  AND ga_session_id IS NOT NULL;