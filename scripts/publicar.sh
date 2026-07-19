#!/bin/sh
# Publica a versão atual de site/ na branch de deploy (gh-pages).
#
# Essa branch contém SÓ o conteúdo do site na raiz (index.html, css/, img/,
# .htaccess...), que é o formato que tanto a Hostinger quanto o GitHub Pages
# esperam. Com o deploy automático da Hostinger ligado (hPanel → Avançado →
# Git, branch "gh-pages" → public_html), este comando publica o site.
#
# Uso: sh scripts/publicar.sh
set -e
cd "$(dirname "$0")/.."

echo "→ Enviando main (código + docs)..."
git push origin main

echo "→ Regenerando a branch de deploy a partir de site/..."
git branch -D gh-pages 2>/dev/null || true
git subtree split --prefix=site -b gh-pages

echo "→ Publicando..."
git push -f origin gh-pages

echo ""
echo "✓ Branch de deploy publicada."
echo "  Hostinger: deploy automático em ~1 min (se o Git estiver conectado)."
echo "  GitHub Pages: só funciona com o repositório público."
