# Apometria Livre

> **Caridade é Apometria.** Pesquisa presencial e independente das casas que praticam a Apometria autêntica e gratuita, pelo legado do Dr. José Lacerda de Azevedo.

## O que é este projeto

Site bilíngue (PT-BR ⇄ ES) que educa o público sobre o que a Apometria **é** e o que ela **não é**, e recomenda casas verificadas — visitadas presencialmente ou indicadas por médiuns que praticam a técnica de forma gratuita e coletiva.

**Princípio central:** "Apometria paga não é caridade — portanto, não é Apometria."

## Estrutura

| Pasta | Conteúdo |
|---|---|
| [`site/`](site/) | O site em produção — HTML/CSS/JS puro, zero dependências |
| [`docs/`](docs/) | Documentos de planejamento: dossiê de pesquisa, carta-manifesto, selo, campanha do documentário, deploy |
| [`scripts/`](scripts/) | Scripts utilitários (geração de PDFs, manutenção do HTML) |

## Site

- **Publicar:** `sh scripts/publicar.sh` — regenera a branch **`gh-pages`** (só o conteúdo de `site/` na raiz) e envia. A Hostinger republica sozinha em ~1 min.
- **Hospedagem:** Hostinger com deploy automático via Git — configuração em [`docs/09-deploy-hostinger.md`](docs/09-deploy-hostinger.md) (Opção C)
- **Rodar localmente:** `cd site && python3 -m http.server 8765` → http://localhost:8765

> **Repositório privado + GitHub Pages não combinam** no plano gratuito do GitHub: Pages só funciona em repositório público. Como este é privado, o site público vive na Hostinger. Se um dia o repositório voltar a ser público, a branch `gh-pages` já está no formato certo para o Pages.
>
> `scripts/pages.yml.exemplo` contém um workflow de Actions equivalente — exige `gh auth refresh -s workflow` e mover para `.github/workflows/pages.yml`.

## Licença e uso

Conteúdo educativo do movimento Apometria Livre. As casas listadas atendem gratuitamente — desconfie de quem cobra pela caridade.
