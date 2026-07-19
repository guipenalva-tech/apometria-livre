# -*- coding: utf-8 -*-
"""Converte o texto curvo do selo (textPath) em <path> reais (contornos vetoriais),
para que o SVG funcione em qualquer programa, sem depender de fonte nem de textPath."""
import math
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen

CX, CY, R = 120, 120, 92

def carregar_fonte(caminho):
    font = TTFont(caminho)
    cmap = font.getBestCmap()
    upm = font['head'].unitsPerEm
    glyph_set = font.getGlyphSet()
    hmtx = font['hmtx']
    return font, cmap, upm, glyph_set, hmtx

def glifo(char, cmap, glyph_set, hmtx):
    nome = cmap.get(ord(char))
    if nome is None:
        return '', 0
    pen = SVGPathPen(glyph_set)
    glyph_set[nome].draw(pen)
    d = pen.getCommands()
    largura = hmtx[nome][0]
    return d, largura

def gerar_texto_arco(texto, caminho_fonte, font_size, letter_spacing, arco='topo'):
    font, cmap, upm, glyph_set, hmtx = carregar_fonte(caminho_fonte)
    escala = font_size / upm

    # largura de cada caractere (em unidades de usuário, já na escala do font-size)
    larguras = []
    ds = []
    for ch in texto:
        d, adv = glifo(ch, cmap, glyph_set, hmtx)
        ds.append(d)
        larguras.append(adv * escala)

    largura_total = sum(larguras) + letter_spacing * (len(texto) - 1)
    meio = largura_total / 2

    paths = []
    cum = 0.0
    for i, ch in enumerate(texto):
        avanco = larguras[i]
        offset = cum - meio  # posição (arco) do início do glifo, relativa ao centro
        cum += avanco + letter_spacing

        if ch == ' ' or not ds[i]:
            continue

        angulo_deg = math.degrees(offset / R)
        if arco == 'topo':
            theta = math.radians(270 + angulo_deg)
            rotacao = angulo_deg
        else:  # baixo
            theta = math.radians(90 - angulo_deg)
            rotacao = -angulo_deg

        x = CX + R * math.cos(theta)
        y = CY + R * math.sin(theta)

        transform = f"translate({x:.3f},{y:.3f}) rotate({rotacao:.3f}) scale({escala:.6f},{-escala:.6f})"
        paths.append(f'<path transform="{transform}" d="{ds[i]}"/>')

    return '\n    '.join(paths)

if __name__ == "__main__":
    GEORGIA_BOLD = "/System/Library/Fonts/Supplemental/Georgia Bold.ttf"
    GEORGIA_REG = "/System/Library/Fonts/Supplemental/Georgia.ttf"

    topo = gerar_texto_arco("APOMETRIA LIVRE", GEORGIA_BOLD, font_size=15.5, letter_spacing=2.5, arco='topo')
    baixo = gerar_texto_arco("LEGADO DR. LACERDA", GEORGIA_REG, font_size=12, letter_spacing=1, arco='baixo')

    print("=== TOPO ===")
    print(f'<g fill="#f4dfae">\n    {topo}\n  </g>')
    print("\n=== BAIXO ===")
    print(f'<g fill="#f4dfae">\n    {baixo}\n  </g>')
