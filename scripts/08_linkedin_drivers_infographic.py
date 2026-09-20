"""
Infografia LinkedIn — Pilotos de F1 en Redes Sociales
==========================================================
Misma identidad visual del proyecto F1 Netflix Effect: fondo claro,
paneles oscuros tipo telemetria, Archivo Black, acento rojo de
carreras, bandera a cuadros, silueta de monoplaza.
"""
import cairosvg
import json
import os
import math
import textwrap
import pandas as pd
from xml.sax.saxutils import escape as xml_escape

PROC = "/home/claude/f1_portfolio/data/processed/"
OUT = "/home/claude/f1_portfolio/assets_linkedin_drivers"
os.makedirs(OUT, exist_ok=True)

P = {
    "bg": "#FFFFFF", "text": "#0A0A0A", "text2": "#6E6E73",
    "panel": "#101114", "panel_text": "#F5F5F7", "panel_text2": "#9BA1AE", "panel_track": "#26272C",
    "red": "#FF3B30", "red_deep": "#D8261B",
}
DISPLAY = "'Archivo Black'"
BODY = "DejaVu Sans"
MONO = "DejaVu Sans Mono"

driver_eng = pd.read_csv(PROC + "driver_engagement.csv")
f1_ig = pd.read_csv(PROC + "f1_account_instagram.csv")

def esc(s):
    return xml_escape(str(s))

def wrap_tspans(text, x, width, font_size, dy_mult=1.3, anchor=None):
    wrapped = textwrap.wrap(esc(text), width=width)
    attrs = f' text-anchor="{anchor}"' if anchor else ''
    lines = "".join(f'<tspan x="{x}" dy="{0 if i==0 else font_size*dy_mult}"{attrs}>{ln}</tspan>' for i, ln in enumerate(wrapped))
    return lines, len(wrapped)

def checkered_ribbon(x, y, w, h):
    cols = max(2, int(w // h))
    cw = w / cols
    svg = '<g>'
    for i in range(cols):
        for j in range(2):
            color = "#0A0A0A" if (i+j) % 2 == 0 else "#FFFFFF"
            svg += f'<rect x="{x+i*cw:.1f}" y="{y+j*h/2:.1f}" width="{cw:.1f}" height="{h/2:.1f}" fill="{color}"/>'
    svg += '</g>'
    return svg

def race_car_silhouette(x, y, scale, color, opacity=1.0):
    s = scale
    svg = f'<g opacity="{opacity}">'
    svg += f'<circle cx="{x+35*s}" cy="{y+62*s}" r="{17*s}" fill="{color}"/>'
    svg += f'<circle cx="{x+155*s}" cy="{y+64*s}" r="{19*s}" fill="{color}"/>'
    body = (f"M {x} {y+60*s} L {x+18*s} {y+58*s} L {x+22*s} {y+48*s} L {x+55*s} {y+42*s} "
            f"L {x+65*s} {y+26*s} L {x+95*s} {y+24*s} L {x+110*s} {y+34*s} L {x+135*s} {y+38*s} "
            f"L {x+138*s} {y+16*s} L {x+178*s} {y+12*s} L {x+178*s} {y+20*s} L {x+140*s} {y+24*s} "
            f"L {x+152*s} {y+40*s} L {x+158*s} {y+50*s} L {x+35*s} {y+50*s} Z")
    svg += f'<path d="{body}" fill="{color}"/>'
    svg += '</g>'
    return svg

def bar_gauge_pair(cx, y_top, w, driver, followers, engagement, max_followers, max_engagement, color):
    """Dos barras horizontales: seguidores y engagement, para un piloto."""
    svg = f'<text x="{cx-w/2}" y="{y_top}" font-family="{DISPLAY}" font-size="17" fill="{P["panel_text"]}">{esc(driver)}</text>'
    bar_h = 16
    # barra de seguidores
    y1 = y_top + 16
    fw = (followers/max_followers) * w
    svg += f'<rect x="{cx-w/2}" y="{y1}" width="{w}" height="{bar_h}" rx="4" fill="{P["panel_track"]}"/>'
    svg += f'<rect x="{cx-w/2}" y="{y1}" width="{fw}" height="{bar_h}" rx="4" fill="{P["panel_text2"]}"/>'
    svg += f'<text x="{cx-w/2+w+10}" y="{y1+bar_h-3}" font-family="{MONO}" font-size="12.5" fill="{P["panel_text"]}">{followers}M</text>'
    # barra de engagement
    y2 = y1 + bar_h + 8
    ew = min(1.0, engagement/max_engagement) * w
    svg += f'<rect x="{cx-w/2}" y="{y2}" width="{w}" height="{bar_h}" rx="4" fill="{P["panel_track"]}"/>'
    svg += f'<rect x="{cx-w/2}" y="{y2}" width="{ew}" height="{bar_h}" rx="4" fill="{color}"/>'
    svg += f'<text x="{cx-w/2+w+10}" y="{y2+bar_h-3}" font-family="{MONO}" font-size="12.5" font-weight="bold" fill="{color}">{engagement}%</text>'
    return svg, y2+bar_h

def build_svg(lang):
    if lang == "es":
        eyebrow = "PORTAFOLIO DE DATA SCIENCE · REDES SOCIALES"
        title1, title2 = "MÁS FAMA,", "MENOS ENGAGEMENT"
        subtitle = "Lo que el efecto Netflix hizo con la marca personal de los pilotos de F1"
        s1_label = "SEGUIDORES VS. ENGAGEMENT EN INSTAGRAM · MISMO ESTUDIO, MAYO 2024"
        legend1, legend2 = "Seguidores (millones)", "Engagement (%)"
        s2_eyebrow = "EL HALLAZGO"
        s2_title = "MÁS SEGUIDORES ≠ MÁS AUDIENCIA COMPROMETIDA"
        s2_text = "Norris tiene menos de la cuarta parte de los seguidores de Hamilton — pero más del doble de su engagement. Correlación débil y no significativa (r=-0.35, p=0.65, n=4)."
        s3_label = "LA MARCA DEL PILOTO VS. LA MARCA DE F1 (INSTAGRAM)"
        s3_text = "Para 2023, Hamilton ya tenía 44% más seguidores que la cuenta oficial de F1. Para 2024, su cuenta llegó a 37M — superando ampliamente a la del deporte que lo hizo famoso."
        cta = "EXPLORA EL DASHBOARD COMPLETO →"
        cta2 = "link en el post · ES / EN"
        footer = "Datos reales: tonybet/Social Blade vía GrandPrix247 (mayo 2024), Blinkfire Analytics"
    else:
        eyebrow = "DATA SCIENCE PORTFOLIO · SOCIAL MEDIA"
        title1, title2 = "MORE FAME,", "LESS ENGAGEMENT"
        subtitle = "What the Netflix effect did to F1 drivers' personal brands"
        s1_label = "FOLLOWERS VS. ENGAGEMENT ON INSTAGRAM · SAME STUDY, MAY 2024"
        legend1, legend2 = "Followers (millions)", "Engagement (%)"
        s2_eyebrow = "THE FINDING"
        s2_title = "MORE FOLLOWERS ≠ MORE ENGAGED AUDIENCE"
        s2_text = "Norris has less than a quarter of Hamilton's followers — but more than double his engagement. Weak, non-significant correlation (r=-0.35, p=0.65, n=4)."
        s3_label = "A DRIVER'S BRAND VS. F1'S OWN BRAND (INSTAGRAM)"
        s3_text = "By 2023, Hamilton already had 44% more followers than F1's official account. By 2024, his account reached 37M — far surpassing the sport that made him famous."
        cta = "EXPLORE THE FULL DASHBOARD →"
        cta2 = "link in the post · ES / EN"
        footer = "Real data: tonybet/Social Blade via GrandPrix247 (May 2024), Blinkfire Analytics"

    W = 1200
    svg_parts = [f'<rect width="{W}" height="__H__" fill="{P["bg"]}"/>']
    svg_parts.append(checkered_ribbon(0, 0, W, 10))

    y = 74
    svg_parts.append(f'<text x="70" y="{y}" font-family="{MONO}" font-size="13" font-weight="bold" letter-spacing="1.2" fill="{P["red"]}">{esc(eyebrow)}</text>')
    y += 64
    svg_parts.append(f'<text x="66" y="{y}" font-family="{DISPLAY}" font-size="50" fill="{P["text"]}">{esc(title1)}</text>')
    y += 58
    svg_parts.append(f'<text x="66" y="{y}" font-family="{DISPLAY}" font-size="50" fill="{P["red"]}">{esc(title2)}</text>')
    svg_parts.append(race_car_silhouette(W-320, y-150, 1.1, P["text"], opacity=0.14))
    y += 34
    sub_lines, nsub = wrap_tspans(subtitle, 70, 66, 17)
    svg_parts.append(f'<text x="70" y="{y}" font-family="{BODY}" font-size="17" fill="{P["text2"]}">{sub_lines}</text>')
    y += nsub*17*1.3 + 40

    # ============ SECCION 1: SEGUIDORES VS ENGAGEMENT (panel oscuro) ============
    svg_parts.append(f'<text x="70" y="{y}" font-family="{MONO}" font-size="12.5" font-weight="bold" letter-spacing="1" fill="{P["text2"]}">{esc(s1_label)}</text>')
    y += 26
    s1_h = 420
    svg_parts.append(f'<rect x="70" y="{y}" width="{W-140}" height="{s1_h}" rx="18" fill="{P["panel"]}"/>')
    bar_w = 560
    cx_bars = 70 + 60 + bar_w/2
    max_f = 40
    max_e = 12
    colors = [P["red"], P["red"], P["red"], P["red_deep"]]
    yy = y + 46
    rows = driver_eng.to_dict(orient="records")
    for i, row in enumerate(rows):
        bar_svg, yy = bar_gauge_pair(cx_bars, yy, bar_w, row["piloto"], row["seguidores_millones"], row["engagement_pct"], max_f, max_e, colors[i % len(colors)])
        svg_parts.append(bar_svg)
        yy += 34
    legend_y = y + s1_h - 26
    svg_parts.append(f'<rect x="{cx_bars-bar_w/2}" y="{legend_y-11}" width="14" height="14" rx="3" fill="{P["panel_text2"]}"/>')
    svg_parts.append(f'<text x="{cx_bars-bar_w/2+20}" y="{legend_y}" font-family="{BODY}" font-size="12" fill="{P["panel_text2"]}">{esc(legend1)}</text>')
    svg_parts.append(f'<rect x="{cx_bars-bar_w/2+230}" y="{legend_y-11}" width="14" height="14" rx="3" fill="{P["red"]}"/>')
    svg_parts.append(f'<text x="{cx_bars-bar_w/2+250}" y="{legend_y}" font-family="{BODY}" font-size="12" fill="{P["panel_text2"]}">{esc(legend2)}</text>')
    y += s1_h + 44

    # ============ SECCION 2: HALLAZGO (bloque rojo invertido) ============
    s2_h = 220
    svg_parts.append(f'<rect x="70" y="{y}" width="{W-140}" height="{s2_h}" rx="18" fill="{P["red"]}"/>')
    svg_parts.append(f'<text x="98" y="{y+42}" font-family="{MONO}" font-size="12.5" font-weight="bold" letter-spacing="1" fill="#FFE8E6">{esc(s2_eyebrow)}</text>')
    title_lines, nt = wrap_tspans(s2_title, 98, 34, 27)
    svg_parts.append(f'<text x="98" y="{y+88}" font-family="{DISPLAY}" font-size="27" fill="#FFFFFF">{title_lines}</text>')
    text_lines, ntext = wrap_tspans(s2_text, 98, 90, 15)
    svg_parts.append(f'<text x="98" y="{y+88+nt*27*1.3+30}" font-family="{BODY}" font-size="15" fill="#FFE8E6">{text_lines}</text>')
    y += s2_h + 44

    # ============ SECCION 3: HAMILTON VS F1 (panel oscuro) ============
    svg_parts.append(f'<text x="70" y="{y}" font-family="{MONO}" font-size="12.5" font-weight="bold" letter-spacing="1" fill="{P["text2"]}">{esc(s3_label)}</text>')
    y += 26
    s3_h = 300
    svg_parts.append(f'<rect x="70" y="{y}" width="{W-140}" height="{s3_h}" rx="18" fill="{P["panel"]}"/>')
    bars = [("F1 (2018)", 5.6, P["panel_track"]), ("F1 (2022)", 21.6, P["panel_text2"]), ("Hamilton (2024)", 37.0, P["red"])]
    bar_area_x, bar_area_w = 120, W-140-160
    bar_max_h = 170
    n_bars = len(bars)
    slot = bar_area_w / n_bars
    bw = slot * 0.5
    base_y = y + 30 + bar_max_h
    max_val = 40
    for i, (label, val, color) in enumerate(bars):
        bx = bar_area_x + i*slot + (slot-bw)/2
        bh = (val/max_val) * bar_max_h
        svg_parts.append(f'<rect x="{bx:.1f}" y="{base_y-bh:.1f}" width="{bw:.1f}" height="{bh:.1f}" rx="6" fill="{color}"/>')
        svg_parts.append(f'<text x="{bx+bw/2:.1f}" y="{base_y-bh-14:.1f}" font-family="{DISPLAY}" font-size="20" fill="{P["panel_text"]}" text-anchor="middle">{val}M</text>')
        svg_parts.append(f'<text x="{bx+bw/2:.1f}" y="{base_y+26:.1f}" font-family="{BODY}" font-size="13" font-weight="bold" fill="{P["panel_text2"]}" text-anchor="middle">{esc(label)}</text>')
    text_lines3, ntext3 = wrap_tspans(s3_text, W/2, 100, 14, anchor="middle")
    svg_parts.append(f'<text x="{W/2}" y="{y+s3_h-24}" font-family="{BODY}" font-size="14" fill="{P["panel_text2"]}" text-anchor="middle">{text_lines3}</text>')
    y += s3_h + 44

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
    svg_path = f"{OUT}/linkedin_drivers_{lang}.svg"
    png_path = f"{OUT}/linkedin_drivers_{lang}.png"
    open(svg_path, "w", encoding="utf-8").write(svg_code)
    cairosvg.svg2png(url=svg_path, write_to=png_path, output_width=W, output_height=H)
    print(f"Generado: {png_path}")
