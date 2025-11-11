SELECT
  event_name,
  COUNT(*) AS event_count
FROM
  `gcp-project.andrea_monforte_dataset.ga4_data`
GROUP BY
  event_name
ORDER BY
  event_count DESC