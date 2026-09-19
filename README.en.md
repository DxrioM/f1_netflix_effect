# 🏎️ F1's Netflix Effect — Data Science Portfolio

**🌐 [Leer esto en Español](README.md)**

How *Drive to Survive* transformed Formula 1 from a European niche into a global marketing phenomenon — analyzed with official data, AI-powered sentiment analysis (VADER), and forecasting (Prophet).

**🔴 Demo:** [Español](https://dxriom.github.io/f1_netflix_effect/) · [English](https://dxriom.github.io/f1_netflix_effect/dashboard_en.html)

**📁 Repository:** [github.com/DxrioM/f1_netflix_effect](https://github.com/DxrioM/f1_netflix_effect)

---

## The core finding

Since *Drive to Survive* debuted in 2019, F1 has seen measurable growth across every relevant marketing metric:

| Metric | Before | After | Growth |
|---|---|---|---|
| ESPN audience (US) | 554K (2018) | 1.13M (2024) | +104% |
| Season attendance | 4.2M (2019) | 6.7M (2025) | +60% |
| Social followers | 35M (2020) | 97M (2024) | +177% |
| Annual sponsorship | — | $2.04B (2024, record) | — |

## The surprising finding: the show's quality no longer matters

I compared the **real Tomatometer score** of each Drive to Survive season against my own AI-powered sentiment analysis (VADER) of critic reviews — and against the following year's audience growth:

- Season 4 (2022) had a Tomatometer of just **22%** — one of the show's worst critical receptions
- Despite that, 2022 was a **record growth year** for F1 (US audience rose 28% that year, attendance hit its then-record)

This suggests the "Netflix effect" has already produced a self-sustaining brand halo — audience growth no longer depends on each season of the show being good. The correlation between Tomatometer score and the following year's audience growth is essentially null (and not significant, given the n=4 sample size).

## The two AI techniques

1. **VADER** (Valence Aware Dictionary and sEntiment Reasoner) — a lexicon-based sentiment analyzer validated in academic research (Hutto & Gilbert, 2014). Applied to paraphrased descriptions of each season's critical reception, then compared against the real Rotten Tomatoes Tomatometer. Honest finding: the correlation (r=0.50) isn't statistically significant with a sample of only 4 seasons — a real limitation of lexicon-based sentiment analysis against professional critic consensus.
2. **Prophet** (Meta's time-series forecasting model) — projects US audience and total attendance through 2026-2028, with 80% confidence intervals, based on real historical trends.

## A note on data quality

Unlike an earlier project where I had to discard an entire data source (global digital ad spend) due to severe cross-site inconsistency, the audience figures here ARE consistent across independent sources: ESPN Press Room, Formula1.com, and Liberty Media Corporation's quarterly financial reports all agree on the same order of magnitude and the same trend. Where I didn't have a direct figure for a specific year (e.g., 2020 global audience), I derived it mathematically from an officially reported growth percentage, and flagged it explicitly as estimated.

## Project structure

```
f1_portfolio/
├── data/
│   ├── raw/f1_netflix_effect_data.py   # verified raw data
│   └── processed/                       # clean CSV/JSON + SQLite database
├── sql/
│   ├── 01_schema.sql
│   └── 02_eda_queries.sql               # 6 exploratory analysis queries
├── scripts/
│   ├── 01_clean_transform.py            # cleaning + YoY growth calculation
│   ├── 02_load_db.py                    # load into SQLite
│   ├── 03_run_eda.py                    # runs the SQL queries → JSON
│   ├── 04_ai_analysis.py                # VADER sentiment + Prophet forecasting
│   └── 06_build_dashboards.py           # injects data + Chart.js into the ES/EN templates
├── lib/
│   ├── chart.umd.min.js
│   └── dashboard_template_i18n.html     # bilingual template
├── docs/
│   ├── index.html                       # ⭐ final product in Spanish
│   └── dashboard_en.html                # ⭐ final product in English
├── README.md                            # this file, in Spanish
└── README.en.md                         # this file, in English
```

## How to reproduce it

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

## Tech stack

`Python` · `pandas` · `VADER` (sentiment analysis) · `Prophet` (time-series forecasting) · `SciPy` (Pearson correlation) · `SQL` · `SQLite` · `HTML/CSS/JS` · `Chart.js`

---

*Real data from ESPN Press Room, Formula1.com, Liberty Media Corporation (quarterly financial reports), and Rotten Tomatoes.*
