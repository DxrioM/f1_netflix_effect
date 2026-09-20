"""
Etapa 1b — Datos crudos adicionales: Redes Sociales de Pilotos
====================================================================
Fuentes: estudio tonybet/Social Blade via GrandPrix247 (mayo 2024,
Instagram, mismo estudio y misma fecha de corte para los 4 pilotos --
metodologia consistente), y Blinkfire Analytics (marzo 2023, cuenta
oficial de F1 en Instagram + comparativa directa con Hamilton).
"""

# ============================================================
# ENGAGEMENT VS. SEGUIDORES POR PILOTO (Instagram, mayo 2024)
# Mismo estudio, misma fecha de corte para los 4 -- comparable entre si.
# ============================================================
# (piloto, seguidores_millones, engagement_rate_pct, valor_post_usd)
DRIVER_ENGAGEMENT = [
    ("Lewis Hamilton", 37.0, 4.52, 177654),
    ("Max Verstappen", 12.1, 4.44, 38540),
    ("Daniel Ricciardo", 9.1, 3.74, 29174),
    ("Lando Norris", 8.3, 11.70, 26489),
]

# ============================================================
# MARCA DEL PILOTO VS. MARCA DE F1 (Instagram)
# ============================================================
F1_ACCOUNT_INSTAGRAM = [
    (2018, 5.6, "Blinkfire Analytics"),
    (2022, 21.6, "Blinkfire Analytics (fin de año, +283% vs. 2018)"),
]
# Hamilton tenia "44% mas seguidores en Instagram que la cuenta oficial
# de F1" segun el mismo articulo de Blinkfire (marzo 2023) -- se deriva
# su cifra aproximada de esa fecha; la cifra de 2024 es directa (mismo
# estudio que DRIVER_ENGAGEMENT arriba).
HAMILTON_VS_F1 = {
    "f1_account_2022_m": 21.6,
    "hamilton_premium_pct_2023": 44,  # declarado directamente en la fuente
    "hamilton_derived_2023_m": round(21.6 * 1.44, 1),
    "hamilton_actual_2024_m": 37.0,  # del mismo estudio que arriba
}

if __name__ == "__main__":
    print("Engagement vs. seguidores:")
    for d in DRIVER_ENGAGEMENT:
        print(f"  {d[0]}: {d[1]}M seguidores, {d[2]}% engagement")
    print(f"\nHamilton vs. cuenta oficial de F1:")
    print(f"  F1 (2022): {HAMILTON_VS_F1['f1_account_2022_m']}M")
    print(f"  Hamilton (~2023, derivado de +44%): {HAMILTON_VS_F1['hamilton_derived_2023_m']}M")
    print(f"  Hamilton (2024, real): {HAMILTON_VS_F1['hamilton_actual_2024_m']}M")
