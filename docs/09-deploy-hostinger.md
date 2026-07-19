# 09 — Deploy em Produção (Hostinger)

> Passo a passo para colocar o site **Apometria Livre** no ar na sua hospedagem Hostinger. O site é HTML/CSS/JS puro — **não precisa de build, Node, PHP nem banco de dados**. É literalmente arrastar arquivos.

## O que já foi preparado

- ✅ **Pacote pronto para upload:** `apometria-livre-site.zip` (na raiz do projeto, ao lado desta pasta docs) — contém os 25 arquivos do site, incluindo o `.htaccess` oculto
- ✅ Selo novo com o retrato do Dr. Lacerda aplicado em todo o site (`img/selo.png` 632px + `img/selo-favicon.png` 240px)
- ✅ Imagem de compartilhamento social regenerada com o selo novo (`img/og-image.jpg`, 1200×630) e tags `og:image`/`twitter:image` em todas as páginas — um link do site no WhatsApp mostra a marca, não uma caixa vazia
- ✅ `robots.txt` e `sitemap.xml` (indexação no Google)
- ✅ `.htaccess` (HTTPS forçado, página 404 customizada, compressão, cache do navegador)
- ✅ Todos os links internos verificados — nenhum link quebrado
- ✅ Versões de cache (`?v=N`) consistentes em CSS/JS/imagens em todas as 7 páginas

**Pendente de você, antes ou logo depois do deploy:** ajustar o domínio nos arquivos abaixo se `apometrialivre.org.br` não for o domínio final (ver Passo 5).

## Passo 1 — Confirme o domínio na Hostinger

No painel da Hostinger (hPanel): **Domínios** → confirme que o domínio que você vai usar (ex.: `apometrialivre.org.br` ou outro) está ativo e apontando para o plano de hospedagem certo. Se o domínio foi comprado em outro lugar, configure os **nameservers** da Hostinger nesse registrador (o hPanel mostra os nameservers exatos, algo como `ns1.dns-parking.com` / `ns2.dns-parking.com`).

> Propagação de DNS pode levar de alguns minutos até 24h.

## Passo 2 — Ative o SSL grátis (HTTPS)

No hPanel: **Sites** → seu domínio → **SSL** → ative o certificado Let's Encrypt gratuito (geralmente automático em minutos). O `.htaccess` que preparamos já força redirecionamento para HTTPS — **sem SSL ativo, o site trava em redirecionamento infinito**, então confirme que o SSL está funcionando antes de testar.

## Passo 3 — Envie os arquivos

Você só precisa do conteúdo da pasta **`site/`** — não envie `docs/`, `scripts/` nem `PLAN.md`, que são materiais internos do projeto, não do site público.

### Opção A — File Manager (mais simples, sem instalar nada)

1. No hPanel: **Arquivos** → **Gerenciador de Arquivos**.
2. Entre na pasta `public_html` (ou `public_html/apometrialivre.org.br` se for um domínio adicional).
3. Apague o `index.html` de exemplo que a Hostinger costuma deixar lá, se houver.
4. No Gerenciador de Arquivos, clique **Enviar** → suba o arquivo **`apometria-livre-site.zip`** (já pronto na raiz do projeto, em `/Users/guip.mpro/APOMETRIA/`) → clique com o botão direito nele → **Extrair**.
5. Confirme que `index.html` ficou direto dentro de `public_html`, não dentro de uma subpasta.
6. Apague o `.zip` depois de extrair.

### Opção B — FTP (melhor para atualizações futuras)

1. No hPanel: **Arquivos** → **Contas FTP** → anote host, usuário, senha e porta (geralmente 21).
2. Use um cliente FTP como **FileZilla** (grátis): Arquivo → Gerenciador de Sites → novo site com esses dados.
3. Conecte, navegue até `public_html` no lado remoto (direita) e `site/` no lado local (esquerda).
4. Selecione todo o conteúdo de `site/` e arraste para `public_html`.

```
Estrutura final esperada em public_html/:
public_html/
├── index.html
├── instituicoes.html
├── materiais.html
├── biblioteca.html
├── agenda.html
├── documentario.html
├── 404.html
├── robots.txt
├── sitemap.xml
├── .htaccess          ← arquivo oculto, confirme que foi enviado
├── css/style.css
├── js/main.js
├── img/ (selo.png, selo-favicon.png, og-image.jpg, logos SVG...)
└── downloads/ (os 3 PDFs)
```

## Passo 4 — Configure a página de erro 404 no painel (redundância)

O `.htaccess` já define isso, mas a Hostinger também tem uma configuração própria: hPanel → **Sites** → **Páginas de Erro** → defina `/404.html` como página de erro 404. Isso garante que funcione mesmo se o `.htaccess` for sobrescrito por alguma atualização do painel.

## Passo 5 — Ajuste o domínio real nos arquivos (se for diferente)

Os arquivos foram preparados usando `apometrialivre.org.br` como placeholder. Se o domínio final for outro, rode este comando (Mac/Linux) na pasta `site/` **antes** de enviar, trocando `SEUDOMINIO.com.br` pelo domínio real:

```bash
cd site
grep -rl "apometrialivre.org.br" . | xargs sed -i '' 's/apometrialivre\.org\.br/SEUDOMINIO.com.br/g'
```

Isso corrige: `robots.txt`, `sitemap.xml` e as tags `og:url`/`og:image` de todas as páginas.

## Passo 6 — Teste tudo no ar

- [ ] Site abre em `https://` (cadeado verde, sem aviso de "não seguro")
- [ ] `seudominio.com.br/pagina-que-nao-existe` mostra a página 404 personalizada, não um erro genérico do servidor
- [ ] Os 3 PDFs baixam (Materiais → apostila, carta-manifesto, glossário)
- [ ] O seletor PT⇄ES funciona e mantém a escolha ao navegar entre páginas
- [ ] O menu mobile (hambúrguer) abre e fecha corretamente no celular
- [ ] O modal "Quero participar do projeto" (página Documentário) abre e fecha
- [ ] Cole o link do site no WhatsApp para um contato de teste — confirme que aparece a imagem/título/descrição corretos (isso valida o `og:image`)
- [ ] Rode o site em [Google PageSpeed Insights](https://pagespeed.web.dev) — deve pontuar alto por ser puro HTML/CSS/JS sem frameworks

## Passo 7 — Envie ao Google Search Console

1. Acesse [search.google.com/search-console](https://search.google.com/search-console), adicione a propriedade com seu domínio.
2. Verifique a propriedade (a Hostinger permite adicionar um registro TXT em **DNS** → **Gerenciar registros DNS**, ou use o método de upload de arquivo HTML).
3. Em **Sitemaps**, envie: `https://seudominio.com.br/sitemap.xml`.

## Depois do ar — coisas ainda marcadas como "modelo" no site

Antes de divulgar amplamente, revise estes pontos (todos já sinalizados no próprio site como protótipo):

| Onde | O quê |
|---|---|
| Página **Documentário** | Meta e valor arrecadado são fictícios ("R$ 0 / R$ 60.000 (modelo)") — ajuste quando a campanha real for definida com a produtora |
| Página **Credenciadas** | Casas "Em verificação" precisam de confirmação por visita antes do credenciamento formal (ver [docs/01 §8](01-fundamentos-apometria.md)) |
| Formulários de "Certificação" e "Denunciar irregularidade" | Ainda são placeholders (`href="#"`) — precisam de um formulário real (Google Forms/Tally, ver [docs/06](06-roadmap-execucao.md)) conectado a um e-mail da associação |
| `og:url`/`og:image`/`robots.txt`/`sitemap.xml` | Confirme que o domínio usado é o definitivo (Passo 5) |

## Atualizações futuras

Sempre que editar `css/style.css` ou `js/main.js`, aumente o número de versão (`?v=N`) em **todas** as páginas HTML — os navegadores cacheiam esses arquivos por 1 ano (ver `.htaccess`), então sem isso as mudanças não aparecem para quem já visitou o site. Depois, reenvie os arquivos alterados por FTP ou Gerenciador de Arquivos.
