"""
Etapa 2 — Limpieza y transformacion
======================================
"""
import sys, os
sys.path.insert(0, "/home/claude/f1_portfolio/data/raw")
import f1_netflix_effect_data as raw
import pandas as pd
import numpy as np

OUT_DIR = "/home/claude/f1_portfolio/data/processed"
os.makedirs(OUT_DIR, exist_ok=True)

us_view = pd.DataFrame(raw.US_VIEWERSHIP, columns=["year", "viewers", "es_estimado", "fuente"])
global_tv = pd.DataFrame(raw.GLOBAL_TV_AUDIENCE, columns=["year", "billones", "es_estimado", "fuente"])
attendance = pd.DataFrame(raw.SEASON_ATTENDANCE, columns=["year", "millones", "fuente"])
social = pd.DataFrame(raw.SOCIAL_FOLLOWERS, columns=["year", "millones", "fuente"])
dts = pd.DataFrame(raw.DTS_SEASONS, columns=["temporada", "año", "tomatometer", "num_reviews", "descripcion_es", "descripcion_en"])

# --- datos nuevos: engagement de pilotos + cuenta oficial de F1 ---
sys.path.insert(0, "/home/claude/f1_portfolio/data/raw")
import f1_social_drivers_data as social_raw
driver_eng = pd.DataFrame(social_raw.DRIVER_ENGAGEMENT, columns=["piloto", "seguidores_millones", "engagement_pct", "valor_post_usd"])
f1_ig = pd.DataFrame(social_raw.F1_ACCOUNT_INSTAGRAM, columns=["year", "millones", "fuente"])

# tasa de crecimiento interanual de audiencia EE.UU. (para correlacionar con recepcion de DTS)
us_view["yoy_growth_pct"] = us_view["viewers"].pct_change() * 100

# cruzar: crecimiento de audiencia del AÑO SIGUIENTE al estreno de cada temporada de DTS
# (la temporada X se estrena en año Y, su efecto se mide en el crecimiento de Y a Y+1)
dts_effect = []
for _, row in dts.iterrows():
    yr = row["año"]
    match = us_view[us_view["year"] == yr + 1]
    if not match.empty:
        dts_effect.append({
            "temporada": int(row["temporada"]), "año_estreno": int(yr),
            "tomatometer": int(row["tomatometer"]),
            "crecimiento_audiencia_año_siguiente_pct": round(float(match.iloc[0]["yoy_growth_pct"]), 1)
                if pd.notna(match.iloc[0]["yoy_growth_pct"]) else None,
        })
dts_effect_df = pd.DataFrame(dts_effect)

us_view.to_csv(f"{OUT_DIR}/us_viewership.csv", index=False)
global_tv.to_csv(f"{OUT_DIR}/global_tv.csv", index=False)
attendance.to_csv(f"{OUT_DIR}/attendance.csv", index=False)
social.to_csv(f"{OUT_DIR}/social_followers.csv", index=False)
dts.to_csv(f"{OUT_DIR}/dts_seasons.csv", index=False)
dts_effect_df.to_csv(f"{OUT_DIR}/dts_effect.csv", index=False)
driver_eng.to_csv(f"{OUT_DIR}/driver_engagement.csv", index=False)
f1_ig.to_csv(f"{OUT_DIR}/f1_account_instagram.csv", index=False)

print("Audiencia EE.UU. con crecimiento YoY:")
print(us_view[["year","viewers","yoy_growth_pct"]].to_string(index=False))
print("\nTomatometer vs. crecimiento de audiencia del año siguiente:")
print(dts_effect_df.to_string(index=False))
