# -*- coding: utf-8 -*-
"""Substitui emojis decorativos por ícones outline do sprite img/icones.svg.
Mantém: bandeiras do seletor de idioma (🇧🇷/🇪🇸), caracteres de texto (✓ ✕ ›)."""
import re
import pathlib

SITE = pathlib.Path(__file__).resolve().parent.parent / "site"
PAGINAS = ["index.html", "instituicoes.html", "materiais.html",
           "biblioteca.html", "agenda.html", "documentario.html", "404.html"]

# emoji (sem o seletor de variação) → id do símbolo no sprite
MAPA = {
    "🏠": "casa",
    "🏛": "predio",
    "📄": "arquivo",
    "📚": "livro",
    "📖": "livro",
    "📅": "calendario",
    "💛": "coracao",
    "❤": "coracao",
    "🤲": "presente",
    "🙏": "coracao",
    "🕊": "faisca",
    "✨": "faisca",
    "👥": "grupo",
    "🤝": "grupo",
    "⚕": "cruzmed",
    "🩺": "cruzmed",
    "✉": "email",
    "🎬": "filme",
    "🎞": "filme",
    "📺": "tv",
    "🗞": "jornal",
    "📥": "baixar",
    "🛒": "carrinho",
    "🔗": "link",
    "▶": "play",
    "🔒": "cadeado",
    "🌐": "globo",
    "📍": "pino",
    "☎": "fone",
    "💬": "balao",
    "💰": "moeda",
    "💚": "moeda",
    "🎤": "mic",
    "📜": "arquivo",
    "⏳": "ampulheta",
    "📢": "megafone",
    "⚠": "alerta",
    "ℹ": "info",
    "🏅": "medalha",
}

def svg(simbolo):
    # aspas simples: funciona tanto em texto quanto dentro de atributos data-es="..."
    return f"<svg class='icn' aria-hidden='true'><use href='img/icones.svg#{simbolo}'/></svg>"

VS16 = "️"  # seletor de variação que acompanha muitos emojis

total = {}
for nome in PAGINAS:
    p = SITE / nome
    html = p.read_text(encoding="utf-8")
    for emoji, simbolo in MAPA.items():
        padrao = re.compile(re.escape(emoji) + VS16 + "?")
        html, n = padrao.subn(svg(simbolo), html)
        if n:
            total[emoji] = total.get(emoji, 0) + n
    p.write_text(html, encoding="utf-8")
    print(f"OK: {nome}")

print("\nSubstituições por emoji:")
for e, n in sorted(total.items(), key=lambda x: -x[1]):
    print(f"  {e} -> {MAPA[e]}: {n}x")
print(f"\nTotal: {sum(total.values())}")
