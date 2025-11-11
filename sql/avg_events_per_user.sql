SELECT
  COUNT(*) / COUNT(DISTINCT user_pseudo_id) AS avg_events_per_user
FROM
  `gcp-project.andrea_monforte_dataset.ga4_data`