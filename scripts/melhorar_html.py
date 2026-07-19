# -*- coding: utf-8 -*-
"""Passada de qualidade nas páginas do site: SEO social, acessibilidade e cache-busting."""
import re, pathlib

SITE = pathlib.Path(__file__).resolve().parent.parent / "site"
PAGINAS = ["index.html", "instituicoes.html", "materiais.html",
           "biblioteca.html", "agenda.html", "documentario.html"]

for nome in PAGINAS:
    p = SITE / nome
    html = p.read_text(encoding="utf-8")

    titulo = re.search(r"<title>([^<]+)</title>", html).group(1).replace('"', "&quot;")
    desc = re.search(r'<meta name="description" content="([^"]+)"', html).group(1)

    # 1. theme-color + Open Graph / Twitter (uma vez só)
    if "og:title" not in html:
        og = (
            '<meta name="theme-color" content="#1b2a52">\n'
            f'<meta property="og:title" content="{titulo}">\n'
            f'<meta property="og:description" content="{desc}">\n'
            '<meta property="og:type" content="website">\n'
            '<meta property="og:locale" content="pt_BR">\n'
            '<meta property="og:locale:alternate" content="es_ES">\n'
            '<meta name="twitter:card" content="summary">\n'
        )
        html = html.replace('<link rel="stylesheet"', og + '<link rel="stylesheet"', 1)

    # 2. Link "pular para o conteúdo" + âncora no hero
    if 'class="pular"' not in html:
        html = html.replace(
            "<body>\n",
            '<body>\n\n<a class="pular" href="#conteudo" data-es="Saltar al contenido">Pular para o conteúdo</a>\n',
            1,
        )
        html = re.sub(r'<section class="hero"', '<section id="conteudo" class="hero"', html, count=1)

    # 3. Cache-busting: v3 para css e js
    html = html.replace('href="css/style.css"', 'href="css/style.css?v=3"')
    html = html.replace('href="css/style.css?v=2"', 'href="css/style.css?v=3"')
    html = html.replace('src="js/main.js?v=2"', 'src="js/main.js?v=3"')

    # 4. Terminologia da marca: casas "credenciadas", não "certificadas"
    html = html.replace("casas certificadas", "casas credenciadas")
    html = html.replace("casa certificada", "casa credenciada")
    html = html.replace("casas certificadas", "casas credenciadas")  # ES usa "acreditadas", já correto

    p.write_text(html, encoding="utf-8")
    print(f"OK: {nome}")
