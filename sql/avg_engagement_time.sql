WITH params AS (
  SELECT
    event_timestamp,
    param.key AS paramKey,
    param.value.string_value AS string_value,
    SAFE_CAST(param.value.int_value AS INT64) AS int_value,
    SAFE_CAST(param.value.double_value AS FLOAT64) AS double_value,

    (
      SELECT SAFE_CAST(p.value.int_value AS INT64)
      FROM UNNEST(event_params) AS p
      WHERE p.key = 'ga_session_id'
      LIMIT 1
    ) AS session_id_from_event
  FROM
    `gcp-project.andrea_monforte_dataset.ga4_data`,
    UNNEST(event_params) AS param
),

session_agg AS (
  SELECT
    session_id_from_event AS ga_session_id,
    MAX(CASE WHEN paramKey = 'session_engaged' THEN string_value END) AS session_engaged,
    SUM(CASE WHEN paramKey = 'engagement_time_msec' AND int_value IS NOT NULL THEN int_value ELSE 0 END) AS total_engagement_time_msec
  FROM
    params
  GROUP BY
    session_id_from_event
)

SELECT
  AVG(total_engagement_time_msec) / 1000.0 AS average_engagement_time_sec
FROM
  session_agg
WHERE
  session_engaged = '1'
  AND ga_session_id IS NOT NULL;
