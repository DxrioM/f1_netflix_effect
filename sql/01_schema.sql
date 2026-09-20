-- ============================================================
-- Esquema — El Efecto Netflix en F1
-- ============================================================
DROP TABLE IF EXISTS us_viewership;
DROP TABLE IF EXISTS global_tv;
DROP TABLE IF EXISTS attendance;
DROP TABLE IF EXISTS social_followers;
DROP TABLE IF EXISTS dts_seasons;

CREATE TABLE us_viewership (
    year INTEGER PRIMARY KEY, viewers INTEGER NOT NULL,
    es_estimado INTEGER NOT NULL, fuente TEXT, yoy_growth_pct REAL
);
CREATE TABLE global_tv (
    year INTEGER PRIMARY KEY, billones REAL NOT NULL,
    es_estimado INTEGER NOT NULL, fuente TEXT
);
CREATE TABLE attendance (
    year INTEGER PRIMARY KEY, millones REAL NOT NULL, fuente TEXT
);
CREATE TABLE social_followers (
    year INTEGER PRIMARY KEY, millones REAL NOT NULL, fuente TEXT
);
CREATE TABLE dts_seasons (
    temporada INTEGER PRIMARY KEY, año INTEGER NOT NULL,
    tomatometer INTEGER NOT NULL, num_reviews INTEGER,
    descripcion_es TEXT, descripcion_en TEXT
);
CREATE TABLE driver_engagement (
    piloto TEXT PRIMARY KEY, seguidores_millones REAL NOT NULL,
    engagement_pct REAL NOT NULL, valor_post_usd INTEGER
);
CREATE TABLE f1_account_instagram (
    year INTEGER PRIMARY KEY, millones REAL NOT NULL, fuente TEXT
);
