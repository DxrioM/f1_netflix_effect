"""
Etapa 5 — IA aplicada: VADER sentiment + Prophet forecasting
================================================================
1) VADER (analizador de sentimiento lexico, Hutto & Gilbert 2014):
   analiza las descripciones parafraseadas de la recepcion critica de
   cada temporada de Drive to Survive, y se valida contra el Tomatometer
   REAL de Rotten Tomatoes -- ¿el sentimiento de mi analisis de texto
   coincide con el consenso real de criticos?

2) Prophet (modelo de forecasting de Meta, usa un modelo aditivo de
   series de tiempo con tendencia + estacionalidad): proyecta el
   crecimiento de audiencia en EE.UU. y de asistencia hacia 2025-2028.
"""
import pandas as pd
import numpy as np
import json
import warnings
warnings.filterwarnings("ignore")
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from scipy import stats

PROC = "/home/claude/f1_portfolio/data/processed/"
dts = pd.read_csv(PROC + "dts_seasons.csv")
us_view = pd.read_csv(PROC + "us_viewership.csv")
attendance = pd.read_csv(PROC + "attendance.csv")

# ============================================================
# 1) VADER SENTIMENT — validado contra Tomatometer real
# ============================================================
print("[1/2] VADER sentiment analysis...")
analyzer = SentimentIntensityAnalyzer()
dts["vader_compound"] = dts["descripcion_en"].apply(lambda t: analyzer.polarity_scores(t)["compound"])
dts["vader_score_0_100"] = ((dts["vader_compound"] + 1) / 2 * 100).round(1)

r_vader, p_vader = stats.pearsonr(dts["tomatometer"], dts["vader_score_0_100"])
print(f"  Correlacion VADER vs. Tomatometer real: r={r_vader:.3f} (p={p_vader:.3f}, n={len(dts)})")
print(dts[["temporada", "tomatometer", "vader_score_0_100"]].to_string(index=False))

# ============================================================
# 2) PROPHET FORECASTING
# ============================================================
print("\n[2/2] Prophet forecasting...")
from prophet import Prophet

def forecast_series(df, value_col, periods, freq="YS"):
    prophet_df = df[["year", value_col]].copy()
    prophet_df["ds"] = pd.to_datetime(prophet_df["year"], format="%Y")
    prophet_df["y"] = prophet_df[value_col]
    m = Prophet(yearly_seasonality=False, weekly_seasonality=False, daily_seasonality=False,
                interval_width=0.80)
    m.fit(prophet_df[["ds", "y"]])
    future = m.make_future_dataframe(periods=periods, freq=freq)
    fcst = m.predict(future)
    fcst["year"] = fcst["ds"].dt.year
    hist_years = set(df["year"])
    future_only = fcst[~fcst["year"].isin(hist_years)][["year", "yhat", "yhat_lower", "yhat_upper"]]
    return future_only

us_forecast = forecast_series(us_view, "viewers", periods=4)
us_forecast_list = [
    {"year": int(r.year), "pred": round(float(r.yhat)), "lower": round(float(r.yhat_lower)), "upper": round(float(r.yhat_upper))}
    for r in us_forecast.itertuples()
]
print("  Proyeccion audiencia EE.UU.:")
for f in us_forecast_list:
    print(f"    {f['year']}: {f['pred']:,} (IC80%: {f['lower']:,} - {f['upper']:,})")

att_forecast = forecast_series(attendance, "millones", periods=3)
att_forecast_list = [
    {"year": int(r.year), "pred": round(float(r.yhat), 2), "lower": round(float(r.yhat_lower), 2), "upper": round(float(r.yhat_upper), 2)}
    for r in att_forecast.itertuples()
]
print("  Proyeccion asistencia:")
for f in att_forecast_list:
    print(f"    {f['year']}: {f['pred']}M (IC80%: {f['lower']}M - {f['upper']}M)")

# ============================================================
# 3) ENGAGEMENT VS. SEGUIDORES POR PILOTO
# ============================================================
print("\n[3/3] Correlacion engagement vs. seguidores...")
driver_eng = pd.read_csv(PROC + "driver_engagement.csv")
r_eng, p_eng = stats.pearsonr(driver_eng["seguidores_millones"], driver_eng["engagement_pct"])
print(f"  Correlacion seguidores vs. engagement: r={r_eng:.3f} (p={p_eng:.3f}, n={len(driver_eng)})")
print(driver_eng.to_string(index=False))

dts.to_csv(PROC + "dts_seasons.csv", index=False)  # ahora incluye columnas vader

metrics = {
    "vader_correlation": {"r": round(float(r_vader), 3), "p": round(float(p_vader), 3), "n": int(len(dts))},
    "dts_seasons_sentiment": dts[["temporada", "año", "tomatometer", "vader_score_0_100"]].to_dict(orient="records"),
    "us_viewership_forecast": us_forecast_list,
    "attendance_forecast": att_forecast_list,
    "engagement_correlation": {"r": round(float(r_eng), 3), "p": round(float(p_eng), 3), "n": int(len(driver_eng))},
}
with open(PROC + "ai_metrics.json", "w", encoding="utf-8") as f:
    json.dump(metrics, f, indent=2, ensure_ascii=False)
print("\nGuardado: ai_metrics.json")
