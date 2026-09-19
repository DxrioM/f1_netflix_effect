"""
Etapa 3 — Carga a SQLite
"""
import sqlite3
import pandas as pd

DB_PATH = "/home/claude/f1_portfolio/data/processed/f1.db"
SCHEMA_PATH = "/home/claude/f1_portfolio/sql/01_schema.sql"
PROC = "/home/claude/f1_portfolio/data/processed/"

us_view = pd.read_csv(PROC + "us_viewership.csv")
us_view["es_estimado"] = us_view["es_estimado"].astype(int)
global_tv = pd.read_csv(PROC + "global_tv.csv")
global_tv["es_estimado"] = global_tv["es_estimado"].astype(int)
attendance = pd.read_csv(PROC + "attendance.csv")
social = pd.read_csv(PROC + "social_followers.csv")
dts = pd.read_csv(PROC + "dts_seasons.csv")

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()
with open(SCHEMA_PATH) as f:
    cur.executescript(f.read())

us_view.to_sql("us_viewership", conn, if_exists="append", index=False)
global_tv.to_sql("global_tv", conn, if_exists="append", index=False)
attendance.to_sql("attendance", conn, if_exists="append", index=False)
social.to_sql("social_followers", conn, if_exists="append", index=False)
dts.to_sql("dts_seasons", conn, if_exists="append", index=False)
conn.commit()

for t in ["us_viewership", "global_tv", "attendance", "social_followers", "dts_seasons"]:
    n = cur.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
    print(f"  {t}: {n} filas")
conn.close()
print(f"\nBase de datos creada en: {DB_PATH}")
