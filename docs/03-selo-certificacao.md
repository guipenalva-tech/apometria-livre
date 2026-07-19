# 03 — Selo de Certificação "Apometria Legado Lacerda"

> O selo é um **ícone digital** (SVG/PNG) e físico (adesivo/placa) que as instituições certificadas exibem em seus sites, portas e materiais. A verificação é feita pelo **diretório público** no site da associação: cada selo aponta (link/QR) para a página da instituição no diretório.

## 1. Por que o modelo "diretório verificado"

- **Barato e imediato:** não exige infraestrutura criptográfica.
- **Difícil de falsificar na prática:** qualquer pessoa clica no selo (ou escaneia o QR) e cai na página oficial `associacao.org.br/instituicoes/nome-da-casa`. Se a casa não está no diretório, o selo é falso.
- **Revogável:** basta remover a página do diretório; o selo do infrator passa a apontar para uma página "certificação revogada/não encontrada".
- Fase 2 (futura): badge assinado digitalmente (JSON + QR verificável offline).

## 2. Critérios de certificação

Uma instituição recebe o selo se cumprir **todos** os critérios:

### Critérios eliminatórios (sem exceção)
1. **Gratuidade total do atendimento espiritual** — nenhuma cobrança, "contribuição sugerida", ou venda casada. Doações espontâneas e bazares/livrarias para manutenção da casa são aceitos (modelo tradicional espírita).
2. **Prática em grupo dentro de instituição** — não certifica pessoas físicas nem "consultórios" individuais.
3. **Aviso claro aos assistidos** de que a Apometria não substitui tratamento médico/psicológico.
4. **Personalidade jurídica** (associação/entidade religiosa com CNPJ) ou vínculo formal com casa que a tenha.

### Critérios de idoneidade
5. **Tempo mínimo de prática:** 5 anos de trabalho contínuo de Apometria (comprovável por histórico público, atas, testemunho de casas vizinhas). Casas mais novas podem entrar como **"membro aspirante"** (sem selo, com mentoria de uma casa certificada).
6. **Formação estruturada:** trabalhadores formados em curso interno seriado (meses/anos) com prática supervisionada — não apenas cursos EAD comprados.
7. **Linhagem/alinhamento:** estudo baseado nas obras do Dr. Lacerda e compromisso público com a carta-manifesto.
8. **Referências:** carta de recomendação de 2 casas já certificadas (após a fundação; as fundadoras se validam mutuamente + validação da casa-mãe).

## 3. Processo de certificação

```
Pedido (formulário no site)
   → Análise documental (Conselho de Certificação, 30 dias)
   → Visita/entrevista (presencial ou vídeo, com roteiro padrão)
   → Parecer do Conselho (aprovado / aspirante / negado, com justificativa)
   → Assinatura do Termo de Compromisso + Carta-Manifesto
   → Publicação no diretório + entrega do kit do selo
   → Renovação a cada 2 anos (declaração + verificação simplificada)
```

**Custo para a instituição: R$ 0.** (Opcional: anuidade simbólica voluntária para manutenção da associação — nunca condição para o selo.)

## 4. Regras de uso do selo

1. O selo digital deve **sempre linkar** para a página da instituição no diretório oficial.
2. Proibido usar o selo em material de venda de cursos/atendimentos pagos.
3. Proibido sublicenciar ou ceder o selo.
4. Revogação automática em caso de: cobrança de atendimento comprovada, uso comercial do nome do Dr. Lacerda, recusa de renovação.
5. Denúncias: formulário público no site; análise pelo Conselho de Ética com direito de defesa.

## 5. Identidade visual do selo

- Formato: círculo (medalha) com anel de texto **"APOMETRIA GRATUITA · LEGADO DR. LACERDA"**.
- Centro: mãos entregando luz / chama sobre livro aberto (gratuidade + estudo).
- Cores: azul-profundo (espiritualidade/confiança) + dourado (luz) — já implementado em `site/img/selo.svg`.
- Versões: colorida, monocromática, adesivo físico com QR code.
- Sempre acompanhado do ano de validade: ex. **"Certificada 2026–2028"**.

## 6. Página de verificação (no site)

Cada instituição certificada tem página com:
- Nome, cidade/UF, endereço, contatos, horários de atendimento.
- Data de certificação e validade.
- Nome do dirigente responsável.
- Status: **Certificada** / Aspirante / Revogada.
- Botão "Denunciar irregularidade".

## 7. Mensagem pública ao usuário final (texto para o site)

> **Confie apenas em casas certificadas.** Antes de buscar atendimento de Apometria, verifique se a instituição exibe o selo e se ela aparece no nosso diretório. Instituições sérias trabalham há décadas, formam seus trabalhadores com estudo sério e **jamais cobram pelo atendimento espiritual**. Se cobraram de você, não é Apometria — denuncie.
