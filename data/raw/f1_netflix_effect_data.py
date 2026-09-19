"""
Etapa 1 — Datos crudos: El Efecto Netflix en F1
====================================================================
Fuentes primarias: ESPN Press Room (audiencia EE.UU.), Formula1.com /
Liberty Media Corporation Q4 financial reports (audiencia global,
asistencia, seguidores, patrocinio), Rotten Tomatoes (Tomatometer real
y reseñas de criticos de cada temporada de Drive to Survive).

Nota de calidad de datos: se descarto la fuente de "gasto publicitario
digital global" en un proyecto anterior por inconsistencias severas
entre sitios. Aqui las cifras SI son consistentes entre fuentes
independientes (ESPN, F1 oficial, Liberty Media coinciden en el
mismo orden de magnitud y tendencia).
"""

# ============================================================
# AUDIENCIA EN EE.UU. (ESPN) — promedio de espectadores por carrera
# ============================================================
# (año, espectadores, es_estimado, fuente)
US_VIEWERSHIP = [
    (2018, 554_000, False, "ESPN Press Room (temporada base, regreso de F1 a ESPN)"),
    (2019, 672_000, False, "Audiense/multiple, +18% vs 2018 -- año de debut de Drive to Survive"),
    (2020, 598_700, True, "Estimado: derivado de '+56% en 2021 vs 2020' aplicado al valor de 2021"),
    (2021, 934_000, False, "ESPN/multiple fuentes coinciden ~934-946K"),
    (2022, 1_200_000, False, "ESPN Press Room -- record historico de la epoca"),
    (2023, 1_160_000, False, "BlackBook Motorsport, con datos de ESPN"),
    (2024, 1_130_000, False, "BlackBook Motorsport / ESPN Press Room"),
]

# ============================================================
# AUDIENCIA GLOBAL ACUMULADA (miles de millones de espectadores TV)
# ============================================================
GLOBAL_TV_AUDIENCE = [
    (2020, 1.49, True, "Estimado: derivado de '+4% en 2021 vs 2020'"),
    (2021, 1.55, False, "Formula1.com, comunicado oficial"),
    (2022, 1.54, False, "Liberty Media Corporation, reporte financiero Q4"),
    (2024, 1.60, False, "Liberty Media Corporation, reporte financiero Q4 2024"),
]

# ============================================================
# ASISTENCIA TOTAL POR TEMPORADA (millones de espectadores en vivo)
# ============================================================
SEASON_ATTENDANCE = [
    (2019, 4.2, "Formula 1 2025 Season Review (comparativa historica oficial)"),
    (2022, 5.7, "Liberty Media Corporation, reporte financiero"),
    (2023, 6.0, "Formula 1 2025 Season Review"),
    (2024, 6.5, "Liberty Media Corporation, reporte financiero Q4 2024 (+9% vs 2023)"),
    (2025, 6.7, "Formula 1 2025 Season Review -- record historico"),
]

# ============================================================
# SEGUIDORES EN REDES SOCIALES (millones, todas las plataformas)
# ============================================================
SOCIAL_FOLLOWERS = [
    (2020, 35.0, "Comunicado de prensa F1/Liberty Media"),
    (2022, 60.6, "Declaraciones de Stefano Domenicali (CEO F1), +23% vs 2021"),
    (2024, 97.0, "Liberty Media Corporation, reporte financiero Q4 2024"),
]

SPONSORSHIP_2024_USD_B = 2.04  # record historico, Onclusive/reportes de patrocinio 2024

# ============================================================
# DRIVE TO SURVIVE — Tomatometer real y reseñas de criticos por temporada
# (temporada, año_estreno, tomatometer_pct, num_reviews_rt, descripcion
#  parafraseada de la recepcion critica, en ES y EN)
# ============================================================
DTS_SEASONS = [
    (1, 2019, 92, 4,
     "Los críticos la describieron como accesible incluso para quienes no siguen el automovilismo, con una producción pulida que atrapa a los recién llegados sin distraer del deporte.",
     "Critics described it as accessible even to non-racing fans, with a polished production that hooks newcomers without distracting from the sport."),
    (4, 2022, 22, 2,
     "Muestra pequeña de solo 2 reseñas con opiniones opuestas: una la elogió por profundizar en los personajes, la otra fue mucho más dura. El promedio bajo refleja esa división, no un consenso amplio.",
     "A small sample of just 2 reviews with opposing opinions: one praised it for deepening the characters, the other was far harsher. The low average reflects that split, not a broad consensus."),
    (5, 2023, 83, None,
     "Los críticos notaron una mejora notable respecto a la temporada anterior, calificándola como una vuelta a una narrativa de carreras más genuina y satisfactoria.",
     "Critics noted a clear improvement over the previous season, calling it a return to more genuine and rewarding racing storytelling."),
    (6, 2024, 59, 4,
     "Recepción mixta: algunos críticos notaron que la serie sigue buscando historias dramáticas incluso cuando la temporada real no las ofrece, mientras otros la calificaron entre aburrida e indulgente.",
     "Mixed reception: some critics noted the series keeps hunting for dramatic storylines even when the real season doesn't offer them, while others called it boring to self-indulgent."),
]

CONTEXT_FACTS = {
    "serie_debut": "2019-03-08",
    "productora": "Netflix / Box to Box Films",
    "dueño_f1": "Liberty Media Corporation",
    "demografia_2020_16_35_pct": 75,  # % del crecimiento de audiencia 2020 que vino de edades 16-35
    "engagement_social_2020_yoy_pct": 99,  # crecimiento interanual de interacciones sociales en 2020
    "primer_gp_eeuu_post_dts_ticket_growth_pct": 15,  # crecimiento de venta de boletos primer GP de EE.UU. tras el debut de la serie
}

if __name__ == "__main__":
    print(f"Audiencia EE.UU.: {len(US_VIEWERSHIP)} años")
    print(f"Audiencia global: {len(GLOBAL_TV_AUDIENCE)} años")
    print(f"Asistencia: {len(SEASON_ATTENDANCE)} años")
    print(f"Seguidores sociales: {len(SOCIAL_FOLLOWERS)} años")
    print(f"Temporadas de Drive to Survive con Tomatometer: {len(DTS_SEASONS)}")
    crecimiento_us = (US_VIEWERSHIP[-1][1] / US_VIEWERSHIP[0][1] - 1) * 100
    print(f"Crecimiento audiencia EE.UU. 2018->2024: +{crecimiento_us:.1f}%")
