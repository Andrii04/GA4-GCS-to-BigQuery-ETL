SELECT
  event_date,
  COUNT(*) AS total_events
FROM 
  `gcp-project.andrea_monforte_dataset.ga4_data`
GROUP BY
  event_date
ORDER BY
  total_events
  DESC