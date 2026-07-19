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

- **Web:** publicado via GitHub Pages a partir de `site/` (workflow em `.github/workflows/pages.yml`)
- **Hospedagem própria:** ver o passo a passo em [`docs/09-deploy-hostinger.md`](docs/09-deploy-hostinger.md)
- Rodar localmente: `cd site && python3 -m http.server 8765` → http://localhost:8765

## Licença e uso

Conteúdo educativo do movimento Apometria Livre. As casas listadas atendem gratuitamente — desconfie de quem cobra pela caridade.
