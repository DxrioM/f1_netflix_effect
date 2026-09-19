"""
Etapa 4 — Ejecutar EDA en SQL y exportar a JSON
"""
import sqlite3
import pandas as pd
import json
import re

DB_PATH = "/home/claude/f1_portfolio/data/processed/f1.db"
SQL_PATH = "/home/claude/f1_portfolio/sql/02_eda_queries.sql"
OUT_PATH = "/home/claude/f1_portfolio/data/processed/eda_results.json"

conn = sqlite3.connect(DB_PATH)
with open(SQL_PATH) as f:
    content = f.read()

blocks = re.split(r'-- \d+\.', content)[1:]
keys = ["us_viewership_serie", "global_tv_serie", "attendance_serie",
        "social_serie", "dts_tomatometer", "comparativa_before_after"]

results = {}
for key, block in zip(keys, blocks):
    idx = block.upper().find("SELECT")
    query = block[idx:].strip().rstrip(";")
    df = pd.read_sql(query, conn)
    # pandas.to_json() convierte NaN -> null correctamente; to_dict()+json.dump()
    # no lo hace porque asignar None a una columna float64 revierte a NaN.
    results[key] = json.loads(df.to_json(orient="records"))
    print(f"{key}: {len(df)} filas")

conn.close()
with open(OUT_PATH, "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)
print(f"\nGuardado en: {OUT_PATH}")
