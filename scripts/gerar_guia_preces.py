# -*- coding: utf-8 -*-
"""Gera a seção 'Guia de Preces' (fragmento HTML) a partir do dataset verificado
do Cap. XXVIII de O Evangelho Segundo o Espiritismo (Kardec, trad. Guillon Ribeiro,
domínio público). Accordion nativo <details> — zero JavaScript.
Fonte: site/data/preces-kardec-cap28.json"""
import json, pathlib, html, re

BASE = pathlib.Path(__file__).resolve().parent.parent
DADOS = BASE / "site" / "data" / "preces-kardec-cap28.json"
SAIDA = BASE / "scripts" / "_guia_preces_fragmento.html"

preces = json.load(open(DADOS, encoding="utf-8"))

def para_html(texto):
    texto = html.escape(texto.strip())
    # quebras duplas → parágrafos; simples → <br>
    blocos = re.split(r"\n\s*\n", texto)
    return "".join("<p>" + b.replace("\n", "<br>") + "</p>" for b in blocos)

# agrupa preservando a ordem das seções
secoes = []
por_secao = {}
for p in preces:
    s = p["secao"]
    if s not in por_secao:
        por_secao[s] = []
        secoes.append(s)
    por_secao[s].append(p)

partes = []
for s in secoes:
    partes.append(f'    <h3 class="sub-secao" style="text-align:left;">{html.escape(s)}</h3>')
    for p in por_secao[s]:
        titulo = html.escape(p["titulo"])
        corpo = para_html(p["texto"])
        partes.append(
            '    <details class="prece">\n'
            f'      <summary>{titulo}</summary>\n'
            f'      <div class="prece-texto">{corpo}</div>\n'
            '    </details>'
        )

fragmento = "\n".join(partes)
SAIDA.write_text(fragmento, encoding="utf-8")
print(f"OK: {len(preces)} preces, {len(secoes)} seções → {SAIDA.name} ({len(fragmento)} chars)")
