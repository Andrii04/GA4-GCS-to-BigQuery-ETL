WITH flattened AS (
  SELECT
    param.key AS key,
    param.value.string_value AS string_value
  FROM
    `gcp-project.andrea_monforte_dataset.ga4_data`,
    UNNEST(event_params) AS param
)
SELECT
  string_value AS page_title,
  COUNT(*) AS page_views
FROM
  flattened
WHERE
  key = 'page_title'
  AND string_value IS NOT NULL
GROUP BY
  page_title
ORDER BY
  page_views DESC;