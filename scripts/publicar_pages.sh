#!/bin/sh
# Publica a versão atual de site/ no GitHub Pages (branch gh-pages).
# Uso: sh scripts/publicar_pages.sh
set -e
cd "$(dirname "$0")/.."

echo "→ Enviando main..."
git push origin main

echo "→ Regenerando gh-pages a partir de site/..."
git branch -D gh-pages 2>/dev/null || true
git subtree split --prefix=site -b gh-pages

echo "→ Publicando..."
git push -f origin gh-pages

echo "✓ Publicado. O site atualiza em ~1 minuto:"
echo "  https://guipenalva-tech.github.io/apometria-livre/"
