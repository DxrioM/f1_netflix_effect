"""
Infografia LinkedIn — El Efecto Netflix en F1 (v3)
========================================================
Correccion sobre v2 (que se sintio "plana"): en vez de fondo blanco
uniforme con tarjetas gris-claro (muy poco contraste, casi el mismo
tono), ahora:
  - Pagina base blanca (mantiene el aire "Apple") pero cada panel de
    grafico es un panel OSCURO tipo pantalla de telemetria/cockpit --
    contraste real, y mas fiel a como se ve la data en las
    transmisiones de F1.
  - El hallazgo central (la meseta) se invierte a bloque ROJO solido
    con texto blanco -- una tercera superficie, no solo "clara/oscura"
    repetido, para romper la monotonia.
  - Tipografia Archivo Black (peso extremo) para todos los titulos y
    cifras grandes -- mucho mas impactante que un sans-serif bold
    generico.
"""
import cairosvg
import json
import os
import math
import textwrap
import pandas as pd
from xml.sax.saxutils import escape as xml_escape

PROC = "/home/claude/f1_portfolio/data/processed/"
OUT = "/home/claude/f1_portfolio/assets_linkedin"
os.makedirs(OUT, exist_ok=True)

P = {
    "bg": "#FFFFFF", "text": "#0A0A0A", "text2": "#6E6E73",
    "panel": "#101114", "panel_border": "rgba(255,255,255,0.08)",
    "panel_text": "#F5F5F7", "panel_text2": "#9BA1AE", "panel_track": "#26272C",
    "red": "#FF3B30", "red_deep": "#D8261B",
}
DISPLAY = "'Archivo Black'"
BODY = "DejaVu Sans"
MONO = "DejaVu Sans Mono"

eda = json.load(open(PROC + "eda_results.json", encoding="utf-8"))
ai = json.load(open(PROC + "ai_metrics.json", encoding="utf-8"))
us_view = eda["us_viewership_serie"]
dts_effect_df = pd.read_csv(PROC + "dts_effect.csv")

def esc(s):
    return xml_escape(str(s))

def wrap_tspans(text, x, width, font_size, dy_mult=1.3, anchor=None, family=BODY):
    wrapped = textwrap.wrap(esc(text), width=width)
    attrs = f' text-anchor="{anchor}"' if anchor else ''
    lines = "".join(f'<tspan x="{x}" dy="{0 if i==0 else font_size*dy_mult}"{attrs}>{ln}</tspan>' for i, ln in enumerate(wrapped))
    return lines, len(wrapped)

def start_lights(x, y, r=5, gap=13, lit=5):
    svg = ""
    for i in range(5):
        color = P["red"] if i < lit else P["panel_track"]
        svg += f'<circle cx="{x+i*gap}" cy="{y}" r="{r}" fill="{color}"/>'
    return svg

def race_car_silhouette(x, y, scale, color, opacity=1.0):
    """Silueta generica de un monoplaza de ruedas abiertas (perfil lateral,
    mirando a la derecha) -- forma generica del tipo de vehiculo, sin
    reproducir el diseño, patrocinios o librea de ninguna escuderia.
    Ruedas primero (quedan parcialmente detras de la carroceria, como en
    un perfil real), carroceria despues."""
    s = scale
    svg = f'<g opacity="{opacity}">'
    svg += f'<circle cx="{x+35*s}" cy="{y+62*s}" r="{17*s}" fill="{color}"/>'
    svg += f'<circle cx="{x+155*s}" cy="{y+64*s}" r="{19*s}" fill="{color}"/>'
    body = (f"M {x} {y+60*s} "
            f"L {x+18*s} {y+58*s} "
            f"L {x+22*s} {y+48*s} "
            f"L {x+55*s} {y+42*s} "
            f"L {x+65*s} {y+26*s} "
            f"L {x+95*s} {y+24*s} "
            f"L {x+110*s} {y+34*s} "
            f"L {x+135*s} {y+38*s} "
            f"L {x+138*s} {y+16*s} "
            f"L {x+178*s} {y+12*s} "
            f"L {x+178*s} {y+20*s} "
            f"L {x+140*s} {y+24*s} "
            f"L {x+152*s} {y+40*s} "
            f"L {x+158*s} {y+50*s} "
            f"L {x+35*s} {y+50*s} Z")
    svg += f'<path d="{body}" fill="{color}"/>'
    svg += '</g>'
    return svg

def checkered_ribbon(x, y, w, h, cols=None):
    """Cinta de bandera a cuadros -- simbolo generico y universal del
    automovilismo, no asociado a ninguna marca puntual."""
    if cols is None:
        cols = max(2, int(w // h))
    cw = w / cols
    svg = f'<g>'
    for i in range(cols):
        for j in range(2):
            color = "#0A0A0A" if (i+j) % 2 == 0 else "#FFFFFF"
            svg += f'<rect x="{x+i*cw:.1f}" y="{y+j*h/2:.1f}" width="{cw:.1f}" height="{h/2:.1f}" fill="{color}"/>'
    svg += '</g>'
    return svg

def speed_gauge(cx, cy, r, value_pct, max_val, label_lines, big_label):
    start_theta = 180
    sweep = min(180, (value_pct/max_val)*180)
    end_theta = start_theta - sweep
    def pt(theta, radius=None):
        radius = radius if radius is not None else r
        rad = math.radians(theta)
        return (cx + radius*math.cos(rad), cy - radius*math.sin(rad))
    x0,y0 = pt(start_theta)
    x1,y1 = pt(end_theta)
    # pista de fondo
    svg = f'<path d="M {x0:.1f} {y0:.1f} A {r} {r} 0 0 1 {cx+r:.1f} {cy:.1f}" fill="none" stroke="{P["panel_track"]}" stroke-width="14" stroke-linecap="round"/>'
    # zona de corte (redline) -- ultimo 15% del arco, como en un tacometro real
    redline_theta = start_theta - 180*0.85
    xr,yr = pt(redline_theta)
    xr2,yr2 = pt(0)
    svg += f'<path d="M {xr:.1f} {yr:.1f} A {r} {r} 0 0 1 {xr2:.1f} {yr2:.1f}" fill="none" stroke="{P["red_deep"]}" stroke-width="14" stroke-linecap="butt" opacity="0.55"/>'
    # marcas de graduacion tipo tacometro (11 marcas, como 0-10 x1000 RPM)
    for k in range(11):
        theta_k = start_theta - k*18
        tick_out = pt(theta_k, r+11)
        tick_in = pt(theta_k, r+2)
        svg += f'<line x1="{tick_in[0]:.1f}" y1="{tick_in[1]:.1f}" x2="{tick_out[0]:.1f}" y2="{tick_out[1]:.1f}" stroke="{P["panel_text2"]}" stroke-width="2"/>'
    large_arc = 1 if sweep > 180 else 0
    svg += f'<path d="M {x0:.1f} {y0:.1f} A {r} {r} 0 {large_arc} 1 {x1:.1f} {y1:.1f}" fill="none" stroke="{P["red"]}" stroke-width="14" stroke-linecap="round"/>'
    needle_len = r*0.82
    nx,ny = cx+needle_len*math.cos(math.radians(end_theta)), cy-needle_len*math.sin(math.radians(end_theta))
    svg += f'<line x1="{cx}" y1="{cy}" x2="{nx:.1f}" y2="{ny:.1f}" stroke="{P["panel_text"]}" stroke-width="2.5"/>'
    svg += f'<circle cx="{cx}" cy="{cy}" r="5" fill="{P["panel_text"]}"/>'
    svg += f'<text x="{cx}" y="{cy-r-24:.0f}" font-family="{DISPLAY}" font-size="27" fill="{P["panel_text"]}" text-anchor="middle">{big_label}</text>'
    ll, _ = wrap_tspans(label_lines, cx, 22, 11, anchor="middle")
    svg += f'<text x="{cx}" y="{cy+28}" font-family="{BODY}" font-size="11" font-weight="bold" fill="{P["panel_text2"]}" text-anchor="middle">{ll}</text>'
    return svg

def build_svg(lang):
    if lang == "es":
        eyebrow = "PORTAFOLIO DE DATA SCIENCE · MARKETING + IA"
        title1, title2 = "EL MOTOR REAL", "FUE NETFLIX"
        subtitle = "Cómo Drive to Survive transformó a la Fórmula 1 en un fenómeno de marketing global"
        s1_label = "AUDIENCIA PROMEDIO POR CARRERA EN EE.UU. (ESPN)"
        s1_marker = "Drive to Survive se estrena aquí"
        s2_title = "¿CUÁL MÉTRICA CRECIÓ MÁS RÁPIDO?"
        s2_sub = "Tasa de crecimiento total de cada métrica, 2018/2019/2020 → 2024/2025"
        g1_lbl, g1_big = "Audiencia\nEE.UU.", "+104%"
        g2_lbl, g2_big = "Asistencia\na carreras", "+60%"
        g3_lbl, g3_big = "Seguidores\nen redes", "+177%"
        s3_eyebrow = "UN MATIZ QUE CASI NADIE MENCIONA"
        s3_title = "DESPUÉS DEL PICO,\nLA AUDIENCIA SE ESTANCÓ"
        s3_text = "1.20M (2022) → 1.16M (2023) → 1.13M (2024) — una caída de 5.8% desde el récord. El crecimiento explosivo inicial ya se volvió una meseta madura, no una curva infinita."
        s4_eyebrow = "¿LA CALIDAD DE LA SERIE PREDICE EL CRECIMIENTO?"
        s4_title = "LAS 4 TEMPORADAS, UNA AL LADO DE LA OTRA"
        s4_xlabel, s4_ylabel = "Tomatometer de la temporada (%)", "Crecimiento el año siguiente (%)"
        s4_text = "Sin patrón claro — el punto con peor Tomatometer (Temporada 4, 22%) no tuvo el peor crecimiento posterior. La correlación real es débil y no significativa (r=0.50, n=4)."
        s5_label = "PROYECCIÓN CON IA (PROPHET) · 2025-2028"
        cta = "EXPLORA EL DASHBOARD INTERACTIVO →"
        cta2 = "link en el post · ES / EN"
        footer = "Datos reales: ESPN Press Room, Formula1.com, Liberty Media Corporation, Rotten Tomatoes"
    else:
        eyebrow = "DATA SCIENCE PORTFOLIO · MARKETING + AI"
        title1, title2 = "THE REAL ENGINE", "WAS NETFLIX"
        subtitle = "How Drive to Survive turned Formula 1 into a global marketing phenomenon"
        s1_label = "AVERAGE US AUDIENCE PER RACE (ESPN)"
        s1_marker = "Drive to Survive premieres here"
        s2_title = "WHICH METRIC GREW THE FASTEST?"
        s2_sub = "Total growth rate for each metric, 2018/2019/2020 → 2024/2025"
        g1_lbl, g1_big = "US\nAudience", "+104%"
        g2_lbl, g2_big = "Race\nAttendance", "+60%"
        g3_lbl, g3_big = "Social\nFollowers", "+177%"
        s3_eyebrow = "A NUANCE ALMOST NO ONE MENTIONS"
        s3_title = "AFTER THE PEAK,\nAUDIENCE PLATEAUED"
        s3_text = "1.20M (2022) → 1.16M (2023) → 1.13M (2024) — a 5.8% drop from the record. The initial explosive growth has already matured into a plateau, not an infinite curve."
        s4_eyebrow = "DOES THE SHOW'S QUALITY PREDICT GROWTH?"
        s4_title = "ALL 4 SEASONS, SIDE BY SIDE"
        s4_xlabel, s4_ylabel = "Season Tomatometer (%)", "Next year's growth (%)"
        s4_text = "No clear pattern — the worst-reviewed season (Season 4, 22%) didn't have the worst subsequent growth. The real correlation is weak and not significant (r=0.50, n=4)."
        s5_label = "AI FORECAST (PROPHET) · 2025-2028"
        cta = "EXPLORE THE INTERACTIVE DASHBOARD →"
        cta2 = "link in the post · ES / EN"
        footer = "Real data: ESPN Press Room, Formula1.com, Liberty Media Corporation, Rotten Tomatoes"

    W = 1200
    svg_parts = [f'<rect width="{W}" height="__H__" fill="{P["bg"]}"/>']

    # ---------- CINTA A CUADROS (acento superior, simbolo universal de carreras) ----------
    svg_parts.append(checkered_ribbon(0, 0, W, 10))

    # ---------- HEADER ----------
    y = 74
    svg_parts.append(f'<text x="70" y="{y}" font-family="{MONO}" font-size="13" font-weight="bold" letter-spacing="1.2" fill="{P["red"]}">{esc(eyebrow)}</text>')
    y += 64
    svg_parts.append(f'<text x="66" y="{y}" font-family="{DISPLAY}" font-size="52" fill="{P["text"]}">{esc(title1)}</text>')
    y += 58
    svg_parts.append(f'<text x="66" y="{y}" font-family="{DISPLAY}" font-size="52" fill="{P["red"]}">{esc(title2)}</text>')
    svg_parts.append(race_car_silhouette(W-330, y-152, 1.15, P["text"], opacity=0.14))
    y += 36
    sub_lines, nsub = wrap_tspans(subtitle, 70, 68, 18)
    svg_parts.append(f'<text x="70" y="{y}" font-family="{BODY}" font-size="18" fill="{P["text2"]}">{sub_lines}</text>')
    y += nsub*18*1.3 + 40

    # ============ SECCION 1: TELEMETRIA (panel oscuro, signature) ============
    svg_parts.append(f'<text x="70" y="{y}" font-family="{MONO}" font-size="12.5" font-weight="bold" letter-spacing="1" fill="{P["text2"]}">{esc(s1_label)}</text>')
    y += 24
    s1_h = 310
    svg_parts.append(f'<rect x="70" y="{y}" width="{W-140}" height="{s1_h}" rx="18" fill="{P["panel"]}"/>')
    chart_x, chart_y, chart_w, chart_h = 100, y+42, W-140-60, 180
    max_v = max(d["viewers"] for d in us_view)
    min_v = min(d["viewers"] for d in us_view)
    n = len(us_view)
    step = chart_w/(n-1)
    coords = [(chart_x+i*step, chart_y+chart_h-((d["viewers"]-min_v)/(max_v-min_v+1)*chart_h*0.9)-chart_h*0.05) for i,d in enumerate(us_view)]
    path_line = "M" + " L".join(f"{x:.1f},{yy:.1f}" for x,yy in coords)
    path_area = path_line + f" L{coords[-1][0]:.1f},{chart_y+chart_h} L{coords[0][0]:.1f},{chart_y+chart_h} Z"
    svg_parts.append(f'''<defs><linearGradient id="tGrad{lang}" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="{P["red"]}" stop-opacity="0.35"/>
      <stop offset="100%" stop-color="{P["red"]}" stop-opacity="0"/>
    </linearGradient></defs>''')
    svg_parts.append(f'<path d="{path_area}" fill="url(#tGrad{lang})"/>')
    svg_parts.append(f'<path d="{path_line}" fill="none" stroke="{P["red"]}" stroke-width="3.5" stroke-linejoin="round" stroke-linecap="round"/>')
    for i,(x,yy) in enumerate(coords):
        svg_parts.append(f'<circle cx="{x:.1f}" cy="{yy:.1f}" r="5" fill="{P["panel"]}" stroke="{P["red"]}" stroke-width="2.5"/>')
        svg_parts.append(f'<text x="{x:.1f}" y="{yy-16:.1f}" font-family="{MONO}" font-size="12.5" font-weight="bold" fill="{P["panel_text"]}" text-anchor="middle">{us_view[i]["viewers"]/1000:.0f}K</text>')
        svg_parts.append(f'<text x="{x:.1f}" y="{chart_y+chart_h+26:.1f}" font-family="{MONO}" font-size="11.5" fill="{P["panel_text2"]}" text-anchor="middle">{us_view[i]["year"]}</text>')
    mark_x = coords[1][0]
    svg_parts.append(f'<line x1="{mark_x:.1f}" y1="{chart_y-10}" x2="{mark_x:.1f}" y2="{chart_y+chart_h+12}" stroke="{P["panel_track"]}" stroke-width="1" stroke-dasharray="3 4"/>')
    svg_parts.append(start_lights(mark_x-52, chart_y-30, r=5, gap=13))
    svg_parts.append(f'<text x="{mark_x:.1f}" y="{chart_y-44}" font-family="{BODY}" font-size="11" font-weight="bold" fill="{P["panel_text2"]}" text-anchor="middle">{esc(s1_marker)}</text>')
    y += s1_h + 46

    # ============ SECCION 2: MEDIDORES (panel oscuro) ============
    title_l, nt2 = wrap_tspans(s2_title, 70, 42, 26, family=DISPLAY)
    svg_parts.append(f'<text x="70" y="{y}" font-family="{DISPLAY}" font-size="26" fill="{P["text"]}">{title_l}</text>')
    y += nt2*26*1.3 + 12
    svg_parts.append(f'<text x="70" y="{y}" font-family="{BODY}" font-size="14" fill="{P["text2"]}">{esc(s2_sub)}</text>')
    y += 32
    s2_h = 270
    svg_parts.append(f'<rect x="70" y="{y}" width="{W-140}" height="{s2_h}" rx="18" fill="{P["panel"]}"/>')
    gauge_r = 92
    gauge_cy = y + 178
    gxs = [70+(W-140)/6, 70+(W-140)/2, 70+5*(W-140)/6]
    svg_parts.append(speed_gauge(gxs[0], gauge_cy, gauge_r, 104, 180, g1_lbl, g1_big))
    svg_parts.append(speed_gauge(gxs[1], gauge_cy, gauge_r, 60, 180, g2_lbl, g2_big))
    svg_parts.append(speed_gauge(gxs[2], gauge_cy, gauge_r, 177, 180, g3_lbl, g3_big))
    y += s2_h + 46

    # ============ SECCION 3: MESETA — BLOQUE ROJO INVERTIDO (rompe la monotonia) ============
    s3_h = 300
    svg_parts.append(f'<rect x="70" y="{y}" width="{W-140}" height="{s3_h}" rx="18" fill="{P["red"]}"/>')
    svg_parts.append(f'<text x="98" y="{y+42}" font-family="{MONO}" font-size="12.5" font-weight="bold" letter-spacing="1" fill="#FFE8E6">{esc(s3_eyebrow)}</text>')
    title_lines3 = s3_title.split("\n")
    ty3 = y + 90
    for tl in title_lines3:
        svg_parts.append(f'<text x="98" y="{ty3}" font-family="{DISPLAY}" font-size="34" fill="#FFFFFF">{esc(tl)}</text>')
        ty3 += 42
    text_lines, ntext = wrap_tspans(s3_text, 98, 84, 15.5)
    svg_parts.append(f'<text x="98" y="{ty3+20}" font-family="{BODY}" font-size="15.5" fill="#FFE8E6">{text_lines}</text>')
    y += s3_h + 46

    # ============ SECCION 4: SCATTER (panel oscuro) ============
    title_l4, nt4 = wrap_tspans(s4_eyebrow, 70, 60, 12.5, family=MONO)
    svg_parts.append(f'<text x="70" y="{y}" font-family="{MONO}" font-size="12.5" font-weight="bold" letter-spacing="1" fill="{P["text2"]}">{title_l4}</text>')
    y += nt4*12.5*1.3 + 14
    title_l4b, nt4b = wrap_tspans(s4_title, 70, 38, 26, family=DISPLAY)
    svg_parts.append(f'<text x="70" y="{y}" font-family="{DISPLAY}" font-size="26" fill="{P["text"]}">{title_l4b}</text>')
    y += nt4b*26*1.3 + 30
    s4_h = 340
    svg_parts.append(f'<rect x="70" y="{y}" width="{W-140}" height="{s4_h}" rx="18" fill="{P["panel"]}"/>')
    plot_x, plot_y, plot_w, plot_h = 130, y+40, 520, 190
    svg_parts.append(f'<line x1="{plot_x}" y1="{plot_y}" x2="{plot_x}" y2="{plot_y+plot_h}" stroke="{P["panel_track"]}" stroke-width="1.5"/>')
    svg_parts.append(f'<line x1="{plot_x}" y1="{plot_y+plot_h}" x2="{plot_x+plot_w}" y2="{plot_y+plot_h}" stroke="{P["panel_track"]}" stroke-width="1.5"/>')
    svg_parts.append(f'<text x="{plot_x+plot_w/2}" y="{plot_y+plot_h+36}" font-family="{BODY}" font-size="11.5" fill="{P["panel_text2"]}" text-anchor="middle">{esc(s4_xlabel)}</text>')
    svg_parts.append(f'<text x="{plot_x-48}" y="{plot_y+plot_h/2}" font-family="{BODY}" font-size="11.5" fill="{P["panel_text2"]}" text-anchor="middle" transform="rotate(-90 {plot_x-48} {plot_y+plot_h/2})">{esc(s4_ylabel)}</text>')
    xs = dts_effect_df["tomatometer"].tolist()
    ys_raw = dts_effect_df["crecimiento_audiencia_año_siguiente_pct"].tolist()
    temporadas = dts_effect_df["temporada"].tolist()
    x_min, x_max = 0, 100
    y_min, y_max = min(ys_raw)-8, max(ys_raw)+8
    for xi, yi, temp in zip(xs, ys_raw, temporadas):
        px = plot_x + (xi-x_min)/(x_max-x_min)*plot_w
        py = plot_y + plot_h - (yi-y_min)/(y_max-y_min)*plot_h
        svg_parts.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="9" fill="{P["red"]}"/>')
        svg_parts.append(f'<text x="{px:.1f}" y="{py-16:.1f}" font-family="{MONO}" font-size="12" font-weight="bold" fill="{P["panel_text"]}" text-anchor="middle">S{temp}</text>')
    for xt in [0,25,50,75,100]:
        px = plot_x + (xt-x_min)/(x_max-x_min)*plot_w
        svg_parts.append(f'<text x="{px:.1f}" y="{plot_y+plot_h+16}" font-family="{MONO}" font-size="10" fill="{P["panel_text2"]}" text-anchor="middle">{xt}</text>')
    text_x = plot_x + plot_w + 50
    text_lines2, ntext2 = wrap_tspans(s4_text, text_x, 32, 14)
    svg_parts.append(f'<text x="{text_x}" y="{plot_y+30}" font-family="{BODY}" font-size="14" fill="{P["panel_text"]}">{text_lines2}</text>')
    y += s4_h + 46

    # ============ SECCION 5: FORECAST (panel claro, para variar el ritmo) ============
    svg_parts.append(f'<text x="70" y="{y}" font-family="{MONO}" font-size="12.5" font-weight="bold" letter-spacing="1" fill="{P["text2"]}">{esc(s5_label)}</text>')
    y += 26
    s5_h = 200
    svg_parts.append(f'<rect x="70" y="{y}" width="{W-140}" height="{s5_h}" rx="18" fill="#FAFAFA" stroke="{P["red"]}" stroke-width="1.5"/>')
    fc = ai["us_viewership_forecast"]
    hist_pts = [(d["year"], d["viewers"]) for d in us_view]
    fc_pts = [(d["year"], d["pred"]) for d in fc]
    fc_upper = [(d["year"], d["upper"]) for d in fc]
    fc_lower = [(d["year"], d["lower"]) for d in fc]
    all_pts = hist_pts + fc_pts
    max_v2 = max(max(d["upper"] for d in fc), max(v for _,v in hist_pts))
    cx0, cy0, cw, ch = 100, y+30, W-140-60, 125
    n2 = len(all_pts)
    stepf = cw/(n2-1)
    def yscale(v): return cy0+ch-(v/max_v2)*ch
    coords_h = [(cx0+i*stepf, yscale(v)) for i,(yr,v) in enumerate(hist_pts)]
    coords_f = [(cx0+(len(hist_pts)+i)*stepf, yscale(v)) for i,(yr,v) in enumerate(fc_pts)]
    coords_fu = [(cx0+(len(hist_pts)+i)*stepf, yscale(v)) for i,(yr,v) in enumerate(fc_upper)]
    coords_fl = [(cx0+(len(hist_pts)+i)*stepf, yscale(v)) for i,(yr,v) in enumerate(fc_lower)]
    band = "M" + f"{coords_h[-1][0]:.1f},{coords_h[-1][1]:.1f} L" + " L".join(f"{x:.1f},{yy:.1f}" for x,yy in coords_fu) + " L" + " L".join(f"{x:.1f},{yy:.1f}" for x,yy in reversed(coords_fl)) + " Z"
    svg_parts.append(f'<path d="{band}" fill="{P["red"]}" opacity="0.12"/>')
    hist_path = "M" + " L".join(f"{x:.1f},{yy:.1f}" for x,yy in coords_h)
    fc_path = "M" + f"{coords_h[-1][0]:.1f},{coords_h[-1][1]:.1f} L" + " L".join(f"{x:.1f},{yy:.1f}" for x,yy in coords_f)
    svg_parts.append(f'<path d="{hist_path}" fill="none" stroke="{P["text"]}" stroke-width="2.5"/>')
    svg_parts.append(f'<path d="{fc_path}" fill="none" stroke="{P["red"]}" stroke-width="2.5" stroke-dasharray="6 4"/>')
    for i,(yr,v) in enumerate(all_pts):
        x = cx0+i*stepf
        yy = yscale(v)
        col = P["text"] if i < len(hist_pts) else P["red"]
        svg_parts.append(f'<circle cx="{x:.1f}" cy="{yy:.1f}" r="3.5" fill="{col}"/>')
        if i % 2 == 0 or i == n2-1:
            svg_parts.append(f'<text x="{x:.1f}" y="{cy0+ch+22}" font-family="{MONO}" font-size="10.5" fill="{P["text2"]}" text-anchor="middle">{yr}</text>')
    y += s5_h + 40

    # ---------- CTA ----------
    svg_parts.append(f'<rect x="70" y="{y}" width="{W-140}" height="70" rx="35" fill="{P["text"]}"/>')
    svg_parts.append(f'<text x="{W/2}" y="{y+44}" font-family="{DISPLAY}" font-size="17" fill="#fff" text-anchor="middle">{esc(cta)}</text>')
    y += 70 + 28
    svg_parts.append(f'<text x="{W/2}" y="{y}" font-family="{MONO}" font-size="12" fill="{P["text2"]}" text-anchor="middle">{esc(cta2)}</text>')
    y += 24
    svg_parts.append(f'<text x="{W/2}" y="{y+18}" font-family="{MONO}" font-size="10.5" fill="#98989D" text-anchor="middle">{esc(footer)}</text>')
    y += 40
    svg_parts.append(checkered_ribbon(0, y, W, 10))
    y += 10

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
