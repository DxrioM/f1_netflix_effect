"""
Infografia LinkedIn — El Efecto Netflix en F1
==================================================
Diseño 90% visual, continuando la identidad del dashboard (asfalto
oscuro, ambar=pre-Netflix/broadcast, cian=post-Netflix/streaming,
franja de bandera a cuadros). El hallazgo central (Tomatometer bajo
pero crecimiento record) se representa con tamaño de circulo, igual
que en proyectos anteriores.
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
    "bg": "#14161C", "card": "#1B1E27", "card2": "#20232E", "border": "#2A2E3A",
    "text": "#F2F3F5", "text2": "#9BA1AE", "text3": "#656B78",
    "broadcast": "#E8B84F", "streaming": "#3FC9E0", "good": "#4CAF6D", "bad": "#E0524A",
}

us_view = json.load(open(PROC.replace("data/processed/","data/processed/") + "eda_results.json", encoding="utf-8"))["us_viewership_serie"]
ai_metrics = json.load(open(PROC + "ai_metrics.json", encoding="utf-8"))

def esc(s):
    return xml_escape(str(s))

def wrap_tspans(text, x, width, font_size, dy_mult=1.3, anchor=None):
    wrapped = textwrap.wrap(esc(text), width=width)
    attrs = f' text-anchor="{anchor}"' if anchor else ''
    lines = "".join(f'<tspan x="{x}" dy="{0 if i==0 else font_size*dy_mult}"{attrs}>{ln}</tspan>' for i, ln in enumerate(wrapped))
    return lines, len(wrapped)

def circle_metric(cx, cy, max_r, value_pct, color, value_label, min_r=30):
    r = max(min_r, (value_pct/100) * max_r)
    svg = f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{color}" opacity="0.95"/>'
    svg += f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="#fff" stroke-width="2" opacity="0.25"/>'
    fsize = min(26, max(13, r*0.28))
    svg += f'<text x="{cx}" y="{cy+fsize*0.35}" font-family="DejaVu Sans Mono" font-size="{fsize:.0f}" font-weight="bold" fill="{P["bg"]}" text-anchor="middle">{value_label}</text>'
    return svg, r

def flagstrip(x, y, w, h):
    n = int(w // 16)
    svg = ""
    for i in range(n):
        color = "#fff" if i % 2 == 0 else P["bg"]
        svg += f'<rect x="{x+i*16}" y="{y}" width="16" height="{h}" fill="{color}"/>'
    return svg

def build_svg(lang):
    if lang == "es":
        title1, title2 = "Motor: ", "Netflix"
        subtitle = "Cómo Drive to Survive transformó a F1 en un fenómeno de marketing global"
        header_eyebrow = "Portafolio de Data Science · Marketing + IA"
        kpi_labels = ["Audiencia EE.UU. 2018→24", "Asistencia récord 2025", "Seguidores 2024", "Patrocinio récord 2024"]
        kpi_vals = ["+104%", "6.7M", "97M", "$2.04B"]
        s1_title = "El crecimiento de audiencia en EE.UU."
        s1_sub = "Espectadores promedio por carrera (ESPN)"
        s2_eyebrow = "El hallazgo que sorprende"
        s2_title = "La marca ya no depende de que la serie sea buena"
        s2_left_lbl, s2_right_lbl = "Tomatometer Temp. 4 (2022)", "Crecimiento de audiencia 2022"
        s2_left_sub, s2_right_sub = "Una de las peores reseñas de la serie", "Año récord para F1 de todas formas"
        s2_caption = "Comparé el Tomatometer real contra mi propio análisis de sentimiento con IA (VADER). Correlación débil y no significativa (r=0.50, n=4) — la audiencia ya creció más allá de la calidad de la serie."
        s3_eyebrow = "Proyección con IA (Prophet)"
        s3_title = "La tendencia sigue al alza hacia 2028"
        record_label = "RÉCORD"
        cta = "Explora el dashboard interactivo + código completo"
        cta2 = "link en el post · ES / EN"
        footer = "Datos reales: ESPN Press Room, Formula1.com, Liberty Media Corporation, Rotten Tomatoes"
    else:
        title1, title2 = "Engine: ", "Netflix"
        subtitle = "How Drive to Survive turned F1 into a global marketing phenomenon"
        header_eyebrow = "Data Science Portfolio · Marketing + AI"
        kpi_labels = ["US Audience 2018→24", "Record 2025 Attendance", "2024 Followers", "Record 2024 Sponsorship"]
        kpi_vals = ["+104%", "6.7M", "97M", "$2.04B"]
        s1_title = "US audience growth"
        s1_sub = "Average viewers per race (ESPN)"
        s2_eyebrow = "The surprising finding"
        s2_title = "The brand no longer depends on the show being good"
        s2_left_lbl, s2_right_lbl = "Season 4 Tomatometer (2022)", "2022 Audience Growth"
        s2_left_sub, s2_right_sub = "One of the show's worst reviews", "Record year for F1 anyway"
        s2_caption = "I compared the real Tomatometer against my own AI sentiment analysis (VADER). Weak, non-significant correlation (r=0.50, n=4) — the audience has already outgrown the show's quality."
        s3_eyebrow = "AI forecast (Prophet)"
        s3_title = "The trend keeps climbing through 2028"
        record_label = "RECORD"
        cta = "Explore the interactive dashboard + full code"
        cta2 = "link in the post · ES / EN"
        footer = "Real data: ESPN Press Room, Formula1.com, Liberty Media Corporation, Rotten Tomatoes"

    W = 1200
    svg_parts = [f'<rect width="{W}" height="__H__" fill="{P["bg"]}"/>']
    svg_parts.append(flagstrip(0, 0, W, 8))

    # ---------- HEADER ----------
    y = 56
    svg_parts.append(f'<text x="70" y="{y}" font-family="DejaVu Sans Mono" font-size="13.5" font-weight="bold" fill="{P["streaming"]}">{esc(header_eyebrow)}</text>')
    y += 54
    svg_parts.append(f'<text x="66" y="{y}" font-family="DejaVu Sans" font-size="48" font-weight="bold" fill="{P["text"]}">{esc(title1)}</text>')
    tw = len(title1)*29
    svg_parts.append(f'<text x="{66+tw}" y="{y}" font-family="DejaVu Sans" font-size="48" font-weight="bold" fill="{P["streaming"]}">{esc(title2)}</text>')
    y += 32
    svg_parts.append(f'<text x="70" y="{y}" font-family="DejaVu Sans" font-size="16" fill="{P["text2"]}">{esc(subtitle)}</text>')
    y += 36

    # ---------- KPI ROW ----------
    kpi_colors = [P["streaming"], P["broadcast"], P["broadcast"], P["good"]]
    kpi_w = (W-140-3*14)/4
    for i in range(4):
        x0 = 70 + i*(kpi_w+14)
        svg_parts.append(f'<rect x="{x0}" y="{y}" width="{kpi_w}" height="76" rx="12" fill="{P["card"]}" stroke="{P["border"]}"/>')
        svg_parts.append(f'<text x="{x0+16}" y="{y+38}" font-family="DejaVu Sans Mono" font-size="24" font-weight="bold" fill="{kpi_colors[i]}">{esc(kpi_vals[i])}</text>')
        lbl_lines, _ = wrap_tspans(kpi_labels[i], x0+16, 24, 10.5)
        svg_parts.append(f'<text x="{x0+16}" y="{y+58}" font-family="DejaVu Sans" font-size="10.5" font-weight="bold" fill="{P["text2"]}">{lbl_lines}</text>')
    y += 76 + 40

    # ============ SECCION 1: CURVA DE CRECIMIENTO (protagonica) ============
    svg_parts.append(f'<text x="70" y="{y}" font-family="DejaVu Sans" font-size="20" font-weight="bold" fill="{P["text"]}">{esc(s1_title)}</text>')
    y += 26
    s1_h = 300
    svg_parts.append(f'<rect x="70" y="{y}" width="{W-140}" height="{s1_h}" rx="16" fill="{P["card"]}" stroke="{P["border"]}"/>')
    svg_parts.append(f'<text x="98" y="{y+34}" font-family="DejaVu Sans" font-size="13" fill="{P["text2"]}">{esc(s1_sub)}</text>')
    chart_x, chart_y, chart_w, chart_h = 98, y+55, W-140-56, 190
    max_v = max(d["viewers"] for d in us_view)
    n = len(us_view)
    bar_w = chart_w / n * 0.6
    gap = chart_w / n
    for i, d in enumerate(us_view):
        bh = (d["viewers"]/max_v) * chart_h
        bx = chart_x + i*gap + (gap-bar_w)/2
        by = chart_y + (chart_h - bh)
        color = P["broadcast"] if d["year"] < 2019 else P["streaming"]
        svg_parts.append(f'<rect x="{bx:.1f}" y="{by:.1f}" width="{bar_w:.1f}" height="{bh:.1f}" rx="4" fill="{color}"/>')
        val_k = d["viewers"]/1000
        svg_parts.append(f'<text x="{bx+bar_w/2:.1f}" y="{by-8}" font-family="DejaVu Sans Mono" font-size="11.5" font-weight="bold" fill="{P["text"]}" text-anchor="middle">{val_k:.0f}K</text>')
        svg_parts.append(f'<text x="{bx+bar_w/2:.1f}" y="{chart_y+chart_h+20}" font-family="DejaVu Sans Mono" font-size="11" fill="{P["text3"]}" text-anchor="middle">{d["year"]}</text>')
    y += s1_h + 34

    # ============ SECCION 2: EL HALLAZGO (circulos de tamaño) ============
    svg_parts.append(f'<text x="70" y="{y}" font-family="DejaVu Sans Mono" font-size="13.5" font-weight="bold" fill="{P["streaming"]}">{esc(s2_eyebrow)}</text>')
    y += 28
    svg_parts.append(f'<text x="70" y="{y}" font-family="DejaVu Sans" font-size="22" font-weight="bold" fill="{P["text"]}">{esc(s2_title)}</text>')
    y += 30
    s2_h = 430
    svg_parts.append(f'<rect x="70" y="{y}" width="{W-140}" height="{s2_h}" rx="16" fill="{P["card"]}" stroke="{P["border"]}"/>')
    mid_x = W/2
    svg_parts.append(f'<line x1="{mid_x}" y1="{y+24}" x2="{mid_x}" y2="{y+s2_h-90}" stroke="{P["border"]}" stroke-width="1"/>')

    lx_cx = 70 + (W-140)/4
    rx_cx = mid_x + (W-140)/4
    l1, _ = wrap_tspans(s2_left_lbl, lx_cx, 26, 13, anchor="middle")
    svg_parts.append(f'<text x="{lx_cx}" y="{y+38}" font-family="DejaVu Sans" font-size="13" font-weight="bold" fill="{P["text2"]}" text-anchor="middle">{l1}</text>')
    l2, _ = wrap_tspans(s2_right_lbl, rx_cx, 26, 13, anchor="middle")
    svg_parts.append(f'<text x="{rx_cx}" y="{y+38}" font-family="DejaVu Sans" font-size="13" font-weight="bold" fill="{P["text2"]}" text-anchor="middle">{l2}</text>')

    circle_cy = y + 195
    circle_max_r = 95
    c1, _ = circle_metric(lx_cx, circle_cy, circle_max_r, 22, P["bad"], "22%", min_r=28)
    svg_parts.append(c1)
    c2, _ = circle_metric(rx_cx, circle_cy, circle_max_r, 100, P["good"], record_label)
    svg_parts.append(c2)
    # el circulo mas grande posible llega hasta circle_cy + circle_max_r; las
    # etiquetas de abajo empiezan despues de eso, con margen, sin importar
    # el tamaño real de cada circulo individual
    sub_y = circle_cy + circle_max_r + 34

    cap_l, _ = wrap_tspans(s2_left_sub, lx_cx, 30, 12.5, anchor="middle")
    svg_parts.append(f'<text x="{lx_cx}" y="{sub_y}" font-family="DejaVu Sans" font-size="12.5" fill="{P["bad"]}" text-anchor="middle">{cap_l}</text>')
    cap_r, _ = wrap_tspans(s2_right_sub, rx_cx, 30, 12.5, anchor="middle")
    svg_parts.append(f'<text x="{rx_cx}" y="{sub_y}" font-family="DejaVu Sans" font-size="12.5" fill="{P["good"]}" text-anchor="middle">{cap_r}</text>')

    cap3, ncap3 = wrap_tspans(s2_caption, mid_x, 96, 13, anchor="middle")
    svg_parts.append(f'<text x="{mid_x}" y="{sub_y+40}" font-family="DejaVu Sans" font-size="13" fill="{P["text2"]}" text-anchor="middle">{cap3}</text>')
    y += s2_h + 36

    # ============ SECCION 3: FORECAST MINI ============
    svg_parts.append(f'<text x="70" y="{y}" font-family="DejaVu Sans Mono" font-size="13.5" font-weight="bold" fill="{P["streaming"]}">{esc(s3_eyebrow)}</text>')
    y += 26
    svg_parts.append(f'<text x="70" y="{y}" font-family="DejaVu Sans" font-size="20" font-weight="bold" fill="{P["text"]}">{esc(s3_title)}</text>')
    y += 26
    s3_h = 200
    svg_parts.append(f'<rect x="70" y="{y}" width="{W-140}" height="{s3_h}" rx="16" fill="{P["card"]}" stroke="{P["streaming"]}" stroke-width="1.5"/>')
    fc = ai_metrics["us_viewership_forecast"]
    hist_pts = [(d["year"], d["viewers"]) for d in us_view]
    fc_pts = [(d["year"], d["pred"]) for d in fc]
    all_pts = hist_pts + fc_pts
    all_years = [p[0] for p in all_pts]
    all_vals = [p[1] for p in all_pts]
    max_v2 = max(all_vals)
    cx0, cy0, cw, ch = 98, y+30, W-140-56, 130
    n2 = len(all_pts)
    step = cw / (n2-1)
    coords = [(cx0+i*step, cy0+ch-(v/max_v2)*ch) for i,(yr,v) in enumerate(all_pts)]
    hist_n = len(hist_pts)
    hist_path = "M" + " L".join(f"{x:.1f},{yy:.1f}" for x,yy in coords[:hist_n])
    fc_path = "M" + " L".join(f"{x:.1f},{yy:.1f}" for x,yy in coords[hist_n-1:])
    svg_parts.append(f'<path d="{hist_path}" fill="none" stroke="{P["broadcast"]}" stroke-width="3"/>')
    svg_parts.append(f'<path d="{fc_path}" fill="none" stroke="{P["streaming"]}" stroke-width="3" stroke-dasharray="7 5"/>')
    for i,(x,yy) in enumerate(coords):
        col = P["broadcast"] if i < hist_n else P["streaming"]
        svg_parts.append(f'<circle cx="{x:.1f}" cy="{yy:.1f}" r="4.5" fill="{col}"/>')
        if i % 2 == 0 or i == n2-1:
            svg_parts.append(f'<text x="{x:.1f}" y="{cy0+ch+20}" font-family="DejaVu Sans Mono" font-size="10.5" fill="{P["text3"]}" text-anchor="middle">{all_years[i]}</text>')
    y += s3_h + 36

    # ---------- CTA ----------
    cta_h = 68
    svg_parts.append(f'<rect x="70" y="{y}" width="{W-140}" height="{cta_h}" rx="14" fill="{P["streaming"]}"/>')
    svg_parts.append(f'<text x="100" y="{y+cta_h/2+6}" font-family="DejaVu Sans" font-size="16" font-weight="bold" fill="{P["bg"]}">{esc(cta)}</text>')
    svg_parts.append(f'<text x="{W-100}" y="{y+cta_h/2+5}" font-family="DejaVu Sans Mono" font-size="12.5" fill="{P["bg"]}" text-anchor="end">{esc(cta2)}</text>')
    y += cta_h + 30

    svg_parts.append(f'<text x="{mid_x}" y="{y}" font-family="DejaVu Sans Mono" font-size="11" fill="{P["text3"]}" text-anchor="middle">{esc(footer)}</text>')
    y += 34
    svg_parts.append(flagstrip(0, y, W, 8))
    y += 8

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
