SELECT 
  event_date,
  COUNT(DISTINCT user_pseudo_id) AS unique_users
FROM
  `gcp-project.andrea_monforte_dataset.ga4_data`
GROUP BY
  event_date
ORDER BY
  event_date
