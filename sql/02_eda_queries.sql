-- ============================================================
-- Análisis Exploratorio — El Efecto Netflix en F1
-- ============================================================

-- 1. Serie completa de audiencia EE.UU. con crecimiento interanual
SELECT year, viewers, es_estimado, yoy_growth_pct FROM us_viewership ORDER BY year;

-- 2. Audiencia global acumulada por año
SELECT year, billones, es_estimado FROM global_tv ORDER BY year;

-- 3. Asistencia total por temporada
SELECT year, millones FROM attendance ORDER BY year;

-- 4. Seguidores en redes sociales
SELECT year, millones FROM social_followers ORDER BY year;

-- 5. Temporadas de Drive to Survive: Tomatometer
SELECT temporada, año, tomatometer, num_reviews FROM dts_seasons ORDER BY temporada;

-- 6. Comparativa 2018 vs 2024 (todas las metricas, para el KPI de "antes/despues")
SELECT
  (SELECT viewers FROM us_viewership WHERE year=2018) AS us_2018,
  (SELECT viewers FROM us_viewership WHERE year=2024) AS us_2024,
  (SELECT millones FROM attendance WHERE year=2019) AS asistencia_2019,
  (SELECT millones FROM attendance WHERE year=2025) AS asistencia_2025,
  (SELECT millones FROM social_followers WHERE year=2020) AS social_2020,
  (SELECT millones FROM social_followers WHERE year=2024) AS social_2024;

-- 7. Engagement vs. seguidores por piloto
SELECT piloto, seguidores_millones, engagement_pct, valor_post_usd
FROM driver_engagement
ORDER BY seguidores_millones DESC;

-- 8. Cuenta oficial de F1 en Instagram por año
SELECT year, millones FROM f1_account_instagram ORDER BY year;
