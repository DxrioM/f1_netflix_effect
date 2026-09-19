"""
Infografia LinkedIn — El Efecto Netflix en F1 (v2)
========================================================
Diseño: minimalismo tipo Apple (fondo claro, un solo acento de color,
tipografia limpia, mucho espacio en blanco) combinado con lenguaje
visual GENERICO de F1 (rojo de carreras, secuencia de luces de largada,
medidores tipo velocimetro, grafico de telemetria) -- sin usar ningun
logo, escuderia o marca especifica.

Graficas nuevas (no usadas en el intento anterior):
1. Grafico de "telemetria" (linea con relleno degradado + marcador de
   luces de largada en 2019) como elemento signature.
2. Medidores tipo velocimetro (3) comparando la tasa de crecimiento de
   audiencia, asistencia y seguidores -- permite comparar de un vistazo
   cual metrica crecio mas.
3. Dispersion (scatter) de las 4 temporadas de Drive to Survive:
   Tomatometer vs. crecimiento de audiencia del año siguiente -- muestra
   el patron completo, no solo un par de puntos.
4. Hallazgo nuevo: la meseta/caida desde el pico de 2022 (-5.8%), un
   matiz que el diseño anterior no mencionaba.
"""
import cairosvg
import json
import os
import math
import textwrap
from xml.sax.saxutils import escape as xml_escape

PROC = "/home/claude/f1_portfolio/data/processed/"
OUT = "/home/claude/f1_portfolio/assets_linkedin"
os.makedirs(OUT, exist_ok=True)

P = {
    "bg": "#FFFFFF", "surface": "#F5F5F7", "border": "#D2D2D7",
    "text": "#1D1D1F", "text2": "#6E6E73", "text3": "#98989D",
    "red": "#E8362A", "track": "#1D1D1F", "green": "#2FA84F",
}

eda = json.load(open(PROC + "eda_results.json", encoding="utf-8"))
ai = json.load(open(PROC + "ai_metrics.json", encoding="utf-8"))
us_view = eda["us_viewership_serie"]
dts_rows = ai["dts_seasons_sentiment"]
dts_effect = json.load(open(PROC + "dts_seasons.csv".replace(".csv",".csv"), encoding="utf-8")) if False else None

import pandas as pd
dts_effect_df = pd.read_csv(PROC + "dts_effect.csv")

def esc(s):
    return xml_escape(str(s))

def wrap_tspans(text, x, width, font_size, dy_mult=1.3, anchor=None):
    wrapped = textwrap.wrap(esc(text), width=width)
    attrs = f' text-anchor="{anchor}"' if anchor else ''
    lines = "".join(f'<tspan x="{x}" dy="{0 if i==0 else font_size*dy_mult}"{attrs}>{ln}</tspan>' for i, ln in enumerate(wrapped))
    return lines, len(wrapped)

def start_lights(x, y, r=9, gap=26, lit=5):
    """Secuencia de luces de largada de F1 (5 circulos) -- icono generico
    del deporte, no de ninguna marca puntual."""
    svg = ""
    for i in range(5):
        color = P["red"] if i < lit else P["border"]
        svg += f'<circle cx="{x+i*gap}" cy="{y}" r="{r}" fill="{color}"/>'
    return svg

def speed_gauge(cx, cy, r, value_pct, max_val, label_lines, big_label):
    """Medidor semicircular tipo velocimetro."""
    start_theta = 180
    sweep = min(180, (value_pct/max_val)*180)
    end_theta = start_theta - sweep
    def pt(theta):
        rad = math.radians(theta)
        return (cx + r*math.cos(rad), cy - r*math.sin(rad))
    x0,y0 = pt(start_theta)
    x1,y1 = pt(end_theta)
    svg = f'<path d="M {x0:.1f} {y0:.1f} A {r} {r} 0 0 1 {cx+r:.1f} {cy:.1f}" fill="none" stroke="{P["surface"]}" stroke-width="14" stroke-linecap="round"/>'
    large_arc = 1 if sweep > 180 else 0
    svg += f'<path d="M {x0:.1f} {y0:.1f} A {r} {r} 0 {large_arc} 1 {x1:.1f} {y1:.1f}" fill="none" stroke="{P["red"]}" stroke-width="14" stroke-linecap="round"/>'
    # aguja
    needle_len = r*0.82
    nx,ny = cx+needle_len*math.cos(math.radians(end_theta)), cy-needle_len*math.sin(math.radians(end_theta))
    svg += f'<line x1="{cx}" y1="{cy}" x2="{nx:.1f}" y2="{ny:.1f}" stroke="{P["track"]}" stroke-width="2.5"/>'
    svg += f'<circle cx="{cx}" cy="{cy}" r="5" fill="{P["track"]}"/>'
    svg += f'<text x="{cx}" y="{cy-r-16:.0f}" font-family="DejaVu Sans Mono" font-size="26" font-weight="bold" fill="{P["text"]}" text-anchor="middle">{big_label}</text>'
    ll, _ = wrap_tspans(label_lines, cx, 22, 11, anchor="middle")
    svg += f'<text x="{cx}" y="{cy+28}" font-family="DejaVu Sans" font-size="11" font-weight="bold" fill="{P["text2"]}" text-anchor="middle">{ll}</text>'
    return svg

def build_svg(lang):
    if lang == "es":
        eyebrow = "PORTAFOLIO DE DATA SCIENCE · MARKETING + IA"
        title1, title2 = "El motor real", "fue Netflix"
        subtitle = "Cómo Drive to Survive transformó a la Fórmula 1 en un fenómeno de marketing global"
        s1_label = "AUDIENCIA PROMEDIO POR CARRERA EN EE.UU. (ESPN)"
        s1_marker = "Drive to Survive se estrena aquí"
        s2_title = "¿Cuál métrica creció más rápido?"
        s2_sub = "Tasa de crecimiento total de cada métrica, 2018/2019/2020 → 2024/2025"
        g1_lbl, g1_big = "Audiencia\nEE.UU.", "+104%"
        g2_lbl, g2_big = "Asistencia\na carreras", "+60%"
        g3_lbl, g3_big = "Seguidores\nen redes", "+177%"
        s3_eyebrow = "Un matiz que casi nadie menciona"
        s3_title = "Después del pico de 2022, la audiencia en EE.UU. se estancó"
        s3_text = "1.20M (2022) → 1.16M (2023) → 1.13M (2024) — una caída de 5.8% desde el récord. El crecimiento explosivo inicial ya se volvió una meseta madura, no una curva infinita."
        s4_eyebrow = "¿La calidad de la serie predice el crecimiento?"
        s4_title = "Las 4 temporadas, una al lado de la otra"
        s4_xlabel, s4_ylabel = "Tomatometer de la temporada (%)", "Crecimiento de audiencia el año siguiente (%)"
        s4_text = "Sin patrón claro — el punto con peor Tomatometer (Temporada 4, 22%) no tuvo el peor crecimiento posterior. La correlación real es débil y no significativa (r=0.50, n=4)."
        s5_label = "PROYECCIÓN CON IA (PROPHET) · 2025-2028"
        cta = "Explora el dashboard interactivo →"
        cta2 = "link en el post · ES / EN"
        footer = "Datos reales: ESPN Press Room, Formula1.com, Liberty Media Corporation, Rotten Tomatoes"
    else:
        eyebrow = "DATA SCIENCE PORTFOLIO · MARKETING + AI"
        title1, title2 = "The real engine", "was Netflix"
        subtitle = "How Drive to Survive turned Formula 1 into a global marketing phenomenon"
        s1_label = "AVERAGE US AUDIENCE PER RACE (ESPN)"
        s1_marker = "Drive to Survive premieres here"
        s2_title = "Which metric grew the fastest?"
        s2_sub = "Total growth rate for each metric, 2018/2019/2020 → 2024/2025"
        g1_lbl, g1_big = "US\nAudience", "+104%"
        g2_lbl, g2_big = "Race\nAttendance", "+60%"
        g3_lbl, g3_big = "Social\nFollowers", "+177%"
        s3_eyebrow = "A nuance almost no one mentions"
        s3_title = "After the 2022 peak, US audience plateaued"
        s3_text = "1.20M (2022) → 1.16M (2023) → 1.13M (2024) — a 5.8% drop from the record. The initial explosive growth has already matured into a plateau, not an infinite curve."
        s4_eyebrow = "Does the show's quality predict growth?"
        s4_title = "All 4 seasons, side by side"
        s4_xlabel, s4_ylabel = "Season Tomatometer (%)", "Next year's audience growth (%)"
        s4_text = "No clear pattern — the worst-reviewed season (Season 4, 22%) didn't have the worst subsequent growth. The real correlation is weak and not significant (r=0.50, n=4)."
        s5_label = "AI FORECAST (PROPHET) · 2025-2028"
        cta = "Explore the interactive dashboard →"
        cta2 = "link in the post · ES / EN"
        footer = "Real data: ESPN Press Room, Formula1.com, Liberty Media Corporation, Rotten Tomatoes"

    W = 1200
    svg_parts = [f'<rect width="{W}" height="__H__" fill="{P["bg"]}"/>']

    # ---------- HEADER ----------
    y = 64
    svg_parts.append(f'<text x="70" y="{y}" font-family="DejaVu Sans Mono" font-size="13" font-weight="bold" letter-spacing="1.2" fill="{P["red"]}">{esc(eyebrow)}</text>')
    y += 58
    svg_parts.append(f'<text x="66" y="{y}" font-family="DejaVu Sans" font-size="46" font-weight="bold" fill="{P["text"]}">{esc(title1)}</text>')
    y += 54
    svg_parts.append(f'<text x="66" y="{y}" font-family="DejaVu Sans" font-size="46" font-weight="bold" fill="{P["red"]}">{esc(title2)}</text>')
    y += 34
    sub_lines, nsub = wrap_tspans(subtitle, 70, 70, 17)
    svg_parts.append(f'<text x="70" y="{y}" font-family="DejaVu Sans" font-size="17" fill="{P["text2"]}">{sub_lines}</text>')
    y += nsub*17*1.3 + 40

    # ============ SECCION 1: TELEMETRIA (signature) ============
    svg_parts.append(f'<text x="70" y="{y}" font-family="DejaVu Sans Mono" font-size="12.5" font-weight="bold" letter-spacing="1" fill="{P["text2"]}">{esc(s1_label)}</text>')
    y += 26
    s1_h = 300
    svg_parts.append(f'<rect x="70" y="{y}" width="{W-140}" height="{s1_h}" rx="20" fill="{P["surface"]}"/>')
    chart_x, chart_y, chart_w, chart_h = 100, y+40, W-140-60, 175
    max_v = max(d["viewers"] for d in us_view)
    min_v = min(d["viewers"] for d in us_view)
    n = len(us_view)
    step = chart_w/(n-1)
    coords = [(chart_x+i*step, chart_y+chart_h-((d["viewers"]-min_v)/(max_v-min_v+1)*chart_h*0.9)-chart_h*0.05) for i,d in enumerate(us_view)]
    path_line = "M" + " L".join(f"{x:.1f},{yy:.1f}" for x,yy in coords)
    path_area = path_line + f" L{coords[-1][0]:.1f},{chart_y+chart_h} L{coords[0][0]:.1f},{chart_y+chart_h} Z"
    svg_parts.append(f'''<defs><linearGradient id="tGrad{lang}" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="{P["red"]}" stop-opacity="0.22"/>
      <stop offset="100%" stop-color="{P["red"]}" stop-opacity="0.02"/>
    </linearGradient></defs>''')
    svg_parts.append(f'<path d="{path_area}" fill="url(#tGrad{lang})"/>')
    svg_parts.append(f'<path d="{path_line}" fill="none" stroke="{P["red"]}" stroke-width="3" stroke-linejoin="round" stroke-linecap="round"/>')
    for i,(x,yy) in enumerate(coords):
        svg_parts.append(f'<circle cx="{x:.1f}" cy="{yy:.1f}" r="5" fill="#fff" stroke="{P["red"]}" stroke-width="2.5"/>')
        svg_parts.append(f'<text x="{x:.1f}" y="{yy-14:.1f}" font-family="DejaVu Sans Mono" font-size="12" font-weight="bold" fill="{P["text"]}" text-anchor="middle">{us_view[i]["viewers"]/1000:.0f}K</text>')
        svg_parts.append(f'<text x="{x:.1f}" y="{chart_y+chart_h+24:.1f}" font-family="DejaVu Sans Mono" font-size="11.5" fill="{P["text3"]}" text-anchor="middle">{us_view[i]["year"]}</text>')
    # marcador de luces de largada en el punto 2019 (indice 1)
    mark_x = coords[1][0]
    svg_parts.append(f'<line x1="{mark_x:.1f}" y1="{chart_y-10}" x2="{mark_x:.1f}" y2="{chart_y+chart_h+10}" stroke="{P["track"]}" stroke-width="1" stroke-dasharray="3 4" opacity="0.4"/>')
    svg_parts.append(start_lights(mark_x-52, chart_y-28, r=5, gap=13))
    svg_parts.append(f'<text x="{mark_x:.1f}" y="{chart_y-40}" font-family="DejaVu Sans" font-size="10.5" font-weight="bold" fill="{P["text2"]}" text-anchor="middle">{esc(s1_marker)}</text>')
    y += s1_h + 44

    # ============ SECCION 2: MEDIDORES (nuevo) ============
    svg_parts.append(f'<text x="70" y="{y}" font-family="DejaVu Sans" font-size="24" font-weight="bold" fill="{P["text"]}">{esc(s2_title)}</text>')
    y += 26
    svg_parts.append(f'<text x="70" y="{y}" font-family="DejaVu Sans" font-size="13.5" fill="{P["text2"]}">{esc(s2_sub)}</text>')
    y += 30
    s2_h = 260
    svg_parts.append(f'<rect x="70" y="{y}" width="{W-140}" height="{s2_h}" rx="20" fill="{P["surface"]}"/>')
    gauge_r = 92
    gauge_cy = y + 175
    gxs = [70+(W-140)/6, 70+(W-140)/2, 70+5*(W-140)/6]
    svg_parts.append(speed_gauge(gxs[0], gauge_cy, gauge_r, 104, 180, g1_lbl, g1_big))
    svg_parts.append(speed_gauge(gxs[1], gauge_cy, gauge_r, 60, 180, g2_lbl, g2_big))
    svg_parts.append(speed_gauge(gxs[2], gauge_cy, gauge_r, 177, 180, g3_lbl, g3_big))
    y += s2_h + 44

    # ============ SECCION 3: MESETA (hallazgo nuevo) ============
    svg_parts.append(f'<text x="70" y="{y}" font-family="DejaVu Sans Mono" font-size="12.5" font-weight="bold" letter-spacing="1" fill="{P["red"]}">{esc(s3_eyebrow)}</text>')
    y += 28
    title_lines, ntitle = wrap_tspans(s3_title, 70, 52, 22)
    svg_parts.append(f'<text x="70" y="{y}" font-family="DejaVu Sans" font-size="22" font-weight="bold" fill="{P["text"]}">{title_lines}</text>')
    y += ntitle*22*1.3 + 18
    s3_h = 130
    svg_parts.append(f'<rect x="70" y="{y}" width="{W-140}" height="{s3_h}" rx="16" fill="{P["surface"]}" stroke="{P["red"]}" stroke-width="1.5"/>')
    text_lines, ntext = wrap_tspans(s3_text, 98, 100, 14.5)
    ty = y + s3_h/2 - (ntext-1)*14.5*1.3/2 + 5
    svg_parts.append(f'<text x="98" y="{ty}" font-family="DejaVu Sans" font-size="14.5" fill="{P["text"]}">{text_lines}</text>')
    y += s3_h + 44

    # ============ SECCION 4: SCATTER (nuevo) ============
    svg_parts.append(f'<text x="70" y="{y}" font-family="DejaVu Sans Mono" font-size="12.5" font-weight="bold" letter-spacing="1" fill="{P["red"]}">{esc(s4_eyebrow)}</text>')
    y += 28
    svg_parts.append(f'<text x="70" y="{y}" font-family="DejaVu Sans" font-size="22" font-weight="bold" fill="{P["text"]}">{esc(s4_title)}</text>')
    y += 30
    s4_h = 330
    svg_parts.append(f'<rect x="70" y="{y}" width="{W-140}" height="{s4_h}" rx="20" fill="{P["surface"]}"/>')
    plot_x, plot_y, plot_w, plot_h = 130, y+34, 520, 190
    # ejes
    svg_parts.append(f'<line x1="{plot_x}" y1="{plot_y}" x2="{plot_x}" y2="{plot_y+plot_h}" stroke="{P["border"]}" stroke-width="1.5"/>')
    svg_parts.append(f'<line x1="{plot_x}" y1="{plot_y+plot_h}" x2="{plot_x+plot_w}" y2="{plot_y+plot_h}" stroke="{P["border"]}" stroke-width="1.5"/>')
    svg_parts.append(f'<text x="{plot_x+plot_w/2}" y="{plot_y+plot_h+34}" font-family="DejaVu Sans" font-size="11.5" fill="{P["text2"]}" text-anchor="middle">{esc(s4_xlabel)}</text>')
    svg_parts.append(f'<text x="{plot_x-46}" y="{plot_y+plot_h/2}" font-family="DejaVu Sans" font-size="11.5" fill="{P["text2"]}" text-anchor="middle" transform="rotate(-90 {plot_x-46} {plot_y+plot_h/2})">{esc(s4_ylabel)}</text>')
    xs = [r["tomatometer"] for r in dts_effect_df.to_dict(orient="records")]
    ys_raw = dts_effect_df["crecimiento_audiencia_año_siguiente_pct"].tolist()
    temporadas = dts_effect_df["temporada"].tolist()
    x_min, x_max = 0, 100
    y_min, y_max = min(ys_raw)-8, max(ys_raw)+8
    for xi, yi, temp in zip(xs, ys_raw, temporadas):
        px = plot_x + (xi-x_min)/(x_max-x_min)*plot_w
        py = plot_y + plot_h - (yi-y_min)/(y_max-y_min)*plot_h
        svg_parts.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="9" fill="{P["red"]}" opacity="0.85"/>')
        svg_parts.append(f'<text x="{px:.1f}" y="{py-16:.1f}" font-family="DejaVu Sans Mono" font-size="11.5" font-weight="bold" fill="{P["text"]}" text-anchor="middle">S{temp}</text>')
    # ticks del eje x
    for xt in [0,25,50,75,100]:
        px = plot_x + (xt-x_min)/(x_max-x_min)*plot_w
        svg_parts.append(f'<text x="{px:.1f}" y="{plot_y+plot_h+16}" font-family="DejaVu Sans Mono" font-size="10" fill="{P["text3"]}" text-anchor="middle">{xt}</text>')
    # texto explicativo a la derecha
    text_x = plot_x + plot_w + 50
    text_lines2, ntext2 = wrap_tspans(s4_text, text_x, 34, 14)
    svg_parts.append(f'<text x="{text_x}" y="{plot_y+30}" font-family="DejaVu Sans" font-size="14" fill="{P["text"]}">{text_lines2}</text>')
    y += s4_h + 44

    # ============ SECCION 5: FORECAST MINI ============
    svg_parts.append(f'<text x="70" y="{y}" font-family="DejaVu Sans Mono" font-size="12.5" font-weight="bold" letter-spacing="1" fill="{P["text2"]}">{esc(s5_label)}</text>')
    y += 26
    s5_h = 190
    svg_parts.append(f'<rect x="70" y="{y}" width="{W-140}" height="{s5_h}" rx="20" fill="{P["surface"]}"/>')
    fc = ai["us_viewership_forecast"]
    hist_pts = [(d["year"], d["viewers"]) for d in us_view]
    fc_pts = [(d["year"], d["pred"]) for d in fc]
    fc_upper = [(d["year"], d["upper"]) for d in fc]
    fc_lower = [(d["year"], d["lower"]) for d in fc]
    all_pts = hist_pts + fc_pts
    max_v2 = max(d["upper"] for d in fc) 
    max_v2 = max(max_v2, max(v for _,v in hist_pts))
    cx0, cy0, cw, ch = 100, y+28, W-140-60, 120
    n2 = len(all_pts)
    stepf = cw/(n2-1)
    def yscale(v): return cy0+ch-(v/max_v2)*ch
    coords_h = [(cx0+i*stepf, yscale(v)) for i,(yr,v) in enumerate(hist_pts)]
    coords_f = [(cx0+(len(hist_pts)+i)*stepf, yscale(v)) for i,(yr,v) in enumerate(fc_pts)]
    coords_fu = [(cx0+(len(hist_pts)+i)*stepf, yscale(v)) for i,(yr,v) in enumerate(fc_upper)]
    coords_fl = [(cx0+(len(hist_pts)+i)*stepf, yscale(v)) for i,(yr,v) in enumerate(fc_lower)]
    band = "M" + f"{coords_h[-1][0]:.1f},{coords_h[-1][1]:.1f} L" + " L".join(f"{x:.1f},{yy:.1f}" for x,yy in coords_fu) + " L" + " L".join(f"{x:.1f},{yy:.1f}" for x,yy in reversed(coords_fl)) + " Z"
    svg_parts.append(f'<path d="{band}" fill="{P["red"]}" opacity="0.10"/>')
    hist_path = "M" + " L".join(f"{x:.1f},{yy:.1f}" for x,yy in coords_h)
    fc_path = "M" + f"{coords_h[-1][0]:.1f},{coords_h[-1][1]:.1f} L" + " L".join(f"{x:.1f},{yy:.1f}" for x,yy in coords_f)
    svg_parts.append(f'<path d="{hist_path}" fill="none" stroke="{P["track"]}" stroke-width="2.5"/>')
    svg_parts.append(f'<path d="{fc_path}" fill="none" stroke="{P["red"]}" stroke-width="2.5" stroke-dasharray="6 4"/>')
    for i,(yr,v) in enumerate(all_pts):
        x = cx0+i*stepf
        yy = yscale(v)
        col = P["track"] if i < len(hist_pts) else P["red"]
        if i % 1 == 0:
            svg_parts.append(f'<circle cx="{x:.1f}" cy="{yy:.1f}" r="3.5" fill="{col}"/>')
        if i % 2 == 0 or i == n2-1:
            svg_parts.append(f'<text x="{x:.1f}" y="{cy0+ch+20}" font-family="DejaVu Sans Mono" font-size="10.5" fill="{P["text3"]}" text-anchor="middle">{yr}</text>')
    y += s5_h + 40

    # ---------- CTA ----------
    svg_parts.append(f'<line x1="70" y1="{y}" x2="{W-70}" y2="{y}" stroke="{P["border"]}" stroke-width="1"/>')
    y += 44
    svg_parts.append(f'<rect x="70" y="{y}" width="{W-140}" height="64" rx="32" fill="{P["track"]}"/>')
    svg_parts.append(f'<text x="{W/2}" y="{y+40}" font-family="DejaVu Sans" font-size="17" font-weight="bold" fill="#fff" text-anchor="middle">{esc(cta)}</text>')
    y += 64 + 26
    svg_parts.append(f'<text x="{W/2}" y="{y}" font-family="DejaVu Sans Mono" font-size="12" fill="{P["text2"]}" text-anchor="middle">{esc(cta2)}</text>')
    y += 22
    svg_parts.append(f'<text x="{W/2}" y="{y+20}" font-family="DejaVu Sans Mono" font-size="10.5" fill="{P["text3"]}" text-anchor="middle">{esc(footer)}</text>')
    y += 50

    H = int(y)
    svg = f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">' + "".join(svg_parts).replace("__H__", str(H)) + '</svg>'
    return svg, W, H

for lang in ["es", "en"]:
    svg_code, W, H = build_svg(lang)
    print(f"{lang}: {W}x{H}")
    svg_path = f"{OUT}/linkedin_infographic_{lang}.svg"
    png_path = f"{OUT}/linkedin_infographic_{lang}.png"
    open(svg_path, "w", encoding="utf-8").write(svg_code)
    cairosvg.svg2png(url=svg_path, write_to=png_path, output_width=W, output_height=H)
    print(f"Generado: {png_path}")
