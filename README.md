# 🏎️ El Efecto Netflix en F1 — Portafolio de Data Science

**🌐 [Read this in English](README.en.md)**

Cómo *Drive to Survive* transformó a la Fórmula 1 de un nicho europeo a un fenómeno de marketing global — analizado con datos oficiales, IA de análisis de sentimiento (VADER) y forecasting (Prophet).

**🔴 Demo:** [Español](https://dxriom.github.io/f1_netflix_effect/) · [English](https://dxriom.github.io/f1_netflix_effect/dashboard_en.html)

**📁 Repositorio:** [github.com/DxrioM/f1_netflix_effect](https://github.com/DxrioM/f1_netflix_effect)

---

## El hallazgo central

Desde el debut de *Drive to Survive* en 2019, F1 vivió un crecimiento medible en cada métrica de marketing relevante:

| Métrica | Antes | Después | Crecimiento |
|---|---|---|---|
| Audiencia ESPN (EE.UU.) | 554K (2018) | 1.13M (2024) | +104% |
| Asistencia por temporada | 4.2M (2019) | 6.7M (2025) | +60% |
| Seguidores en redes | 35M (2020) | 97M (2024) | +177% |
| Patrocinio anual | — | $2.04B (2024, récord) | — |

## El hallazgo que sorprende: la calidad de la serie ya no importa

Comparé el **Tomatometer real** de cada temporada de Drive to Survive contra mi propio análisis de sentimiento con IA (VADER) sobre reseñas de críticos — y contra el crecimiento de audiencia del año siguiente a cada estreno:

- Temporada 4 (2022) tuvo un Tomatometer de apenas **22%** — una de las peores recepciones críticas de la serie
- A pesar de eso, 2022 fue un año de **crecimiento récord** para F1 (audiencia en EE.UU. subió 28% ese año, asistencia alcanzó su entonces-récord)

Esto sugiere que el "efecto Netflix" ya generó un efecto de marca autosuficiente — la audiencia ya no depende de que cada temporada de la serie sea buena. La correlación entre Tomatometer y crecimiento de audiencia del año siguiente es prácticamente nula (y no significativa, dado el tamaño de muestra n=4).

## El efecto Netflix también hizo estrellas a los pilotos

Drive to Survive no solo hizo crecer a F1 como marca — convirtió a varios pilotos en celebridades de redes sociales por derecho propio. Dos hallazgos reales, con datos del mismo estudio (tonybet/Social Blade vía GrandPrix247, mayo 2024) para asegurar metodología consistente:

- **Más seguidores no es más audiencia comprometida**: Lando Norris tiene 8.3M de seguidores en Instagram (menos de la cuarta parte de los 37M de Hamilton), pero su tasa de engagement es 11.70% — más del doble que la de Hamilton (4.52%) y Ricciardo (3.74%). La correlación entre seguidores y engagement es débil y no significativa (r=-0.35, p=0.65, n=4), pero el patrón cualitativo es contundente.
- **La marca de un piloto puede superar a la del propio deporte**: la cuenta oficial de F1 en Instagram pasó de 5.6M (2018) a 21.6M (2022). Para 2023, Lewis Hamilton ya tenía 44% más seguidores en Instagram que la cuenta oficial de F1 — y para 2024 su cuenta alcanzó 37M, muy por encima de la del propio deporte que lo hizo famoso.

## Las dos técnicas de IA

1. **VADER** (Valence Aware Dictionary and sEntiment Reasoner) — analizador de sentimiento léxico validado en investigación académica (Hutto & Gilbert, 2014). Se aplicó a descripciones parafraseadas de la recepción crítica de cada temporada, y se comparó contra el Tomatometer real de Rotten Tomatoes. Hallazgo honesto: la correlación (r=0.50) no es estadísticamente significativa con una muestra de solo 4 temporadas — una limitación real del análisis de sentimiento léxico frente al consenso profesional de críticos.
2. **Prophet** (modelo de forecasting de series de tiempo de Meta) — proyecta la audiencia en EE.UU. y la asistencia total hacia 2026-2028, con intervalos de confianza del 80%, sobre las tendencias históricas reales.

## Nota sobre la calidad de los datos

A diferencia de un proyecto anterior donde tuve que descartar una fuente completa (gasto publicitario digital global) por inconsistencias severas entre sitios, aquí las cifras de audiencia SÍ son consistentes entre fuentes independientes: ESPN Press Room, Formula1.com, y los reportes financieros trimestrales de Liberty Media Corporation coinciden en el mismo orden de magnitud y la misma tendencia. Donde no tenía un dato directo para un año específico (ej. audiencia global 2020), lo derivé matemáticamente de un porcentaje de crecimiento oficialmente reportado, y lo marqué explícitamente como estimado.

## Estructura del proyecto

```
f1_portfolio/
├── data/
│   ├── raw/f1_netflix_effect_data.py   # datos crudos verificados
│   ├── raw/f1_social_drivers_data.py   # engagement de pilotos + cuenta de F1
│   └── processed/                       # CSV/JSON limpios + base SQLite
├── sql/
│   ├── 01_schema.sql
│   └── 02_eda_queries.sql               # 6 queries de análisis exploratorio
├── scripts/
│   ├── 01_clean_transform.py            # limpieza + cálculo de crecimiento YoY
│   ├── 02_load_db.py                    # carga a SQLite
│   ├── 03_run_eda.py                    # ejecuta las queries SQL → JSON
│   ├── 04_ai_analysis.py                # VADER sentiment + Prophet forecasting
│   └── 06_build_dashboards.py           # inyecta datos + Chart.js en las plantillas ES/EN
├── lib/
│   ├── chart.umd.min.js
│   └── dashboard_template_i18n.html     # plantilla bilingüe
├── docs/
│   ├── index.html                       # ⭐ producto final en Español
│   └── dashboard_en.html                # ⭐ producto final en Inglés
├── README.md                            # este archivo, en español
└── README.en.md                         # este archivo, en inglés
```

## Cómo reproducirlo

```bash
pip install pandas numpy scipy vaderSentiment prophet
cd scripts
python3 01_clean_transform.py
python3 02_load_db.py
python3 03_run_eda.py
python3 04_ai_analysis.py
python3 06_build_dashboards.py
cp ../outputs/*.html ../docs/
```

## Stack técnico

`Python` · `pandas` · `VADER` (análisis de sentimiento) · `Prophet` (forecasting de series de tiempo) · `SciPy` (correlación de Pearson) · `SQL` · `SQLite` · `HTML/CSS/JS` · `Chart.js`

---

*Datos reales de ESPN Press Room, Formula1.com, Liberty Media Corporation (reportes financieros trimestrales) y Rotten Tomatoes.*
