# -*- coding: utf-8 -*-
"""Adiciona o 2º lote de casas ao mapeamento nacional (busca no Google + listas
públicas Wix/Padilla). Tudo EM VERIFICAÇÃO. Insere no fim da grade nacional."""
import pathlib, urllib.parse

ALVO = pathlib.Path(__file__).resolve().parent.parent / "site" / "instituicoes.html"
ICN_PINO = "<svg class='icn' aria-hidden='true'><use href='img/icones.svg#pino'/></svg>"

# (nome, cidade, uf, endereço, contato_html_ou_None, consulta_maps)
NOVAS = [
    # --- MG (estava vazio) ---
    ("Centro Espírita Mateus e Tomaz — Casa de Apometria", "Belo Horizonte", "MG",
     "Rua Jacuípe, 160 – Concórdia", "☏ (31) 3442-5919",
     "Centro Espirita Mateus e Tomaz Casa de Apometria Rua Jacuipe 160 Belo Horizonte"),
    ("Centro Espírita São Sebastião", "Belo Horizonte", "MG",
     "Rua Geraldo Menezes Soares, 500 – Sagrada Família", "☏ (31) 98840-0064",
     "Centro Espirita Sao Sebastiao Rua Geraldo Menezes Soares 500 Belo Horizonte"),
    ("Grupo Espírita Apométrico Despertar de Luz", "Uberlândia", "MG",
     "Uberlândia/MG — confirmar endereço", None,
     "Grupo Espirita Apometrico Despertar de Luz Uberlandia"),
    # --- PB (estado novo) ---
    ("Grupo Assistencial Maria de Magdala (GAMM)", "João Pessoa", "PB",
     "João Pessoa/PB — confirmar endereço", None,
     "Grupo Assistencial Maria de Magdala João Pessoa"),
    # --- RN (estado novo) ---
    ("GOIM — Grupo de Oração Irmã Meimei", "Natal", "RN",
     "Natal/RN — confirmar endereço", None,
     "GOIM Grupo de Oracao Irma Meimei Natal RN"),
    # --- PA (reforço) ---
    ("Associação Espírita Osvaldo Santos", "Belém", "PA",
     "Belém/PA — confirmar endereço", None,
     "Associacao Espirita Osvaldo Santos Belem PA"),
    # --- SP (reforço) ---
    ("GATE — Grupo Apométrico de Tratamento Espiritual", "Jundiaí", "SP",
     "Rua Dr. Cândido Mojola, 299 – Vila Hortolândia", "☏ (11) 99419-6559 · tratamento gratuito",
     "Rua Doutor Candido Mojola 299 Jundiai SP"),
    ("FEAL — Fraternidade Espiritual André Luiz", "São Paulo", "SP",
     "Rua César Augusto, 81 – Lapa", "<a class=\"ver\" href=\"https://fealapometria.com\" target=\"_blank\" rel=\"noopener\">fealapometria.com</a>",
     "Rua Cesar Augusto 81 Lapa Sao Paulo"),
    ("AFA — Apometria Francisco de Assis", "São Paulo", "SP",
     "Rua Sacadura Cabral, 68 – Lapa", "<a class=\"ver\" href=\"https://afa.org.br\" target=\"_blank\" rel=\"noopener\">afa.org.br</a>",
     "Rua Sacadura Cabral 68 Lapa Sao Paulo"),
    # --- PE (reforço) ---
    ("Grupo Espírita Amor ao Próximo (GEAP)", "Jaboatão dos Guararapes", "PE",
     "Jaboatão dos Guararapes/PE — confirmar endereço", None,
     "Grupo Espirita Amor ao Proximo Jaboatao dos Guararapes"),
    ("NEFA — Núcleo Espírita Francisco de Assis", "Paulista", "PE",
     "Paulista/PE — confirmar endereço", None,
     "Nucleo Espirita Francisco de Assis Paulista PE"),
    # --- GO (reforço) ---
    ("Centro Espírita Meimei", "Goiânia", "GO",
     "Goiânia/GO — confirmar endereço", None,
     "Centro Espirita Meimei Goiania"),
    # --- SC (reforço) ---
    ("Sociedade Espírita Samaritanos de Maria", "Joinville", "SC",
     "Joinville/SC — confirmar endereço", None,
     "Sociedade Espirita Samaritanos de Maria Joinville"),
]

def card(nome, cidade, uf, endereco, contato, consulta):
    maps = "https://www.google.com/maps/search/?api=1&query=" + urllib.parse.quote_plus(consulta)
    linhas = [f'            <div class="meta">{endereco} · {cidade}/{uf}</div>']
    if contato:
        linhas.append(f'            <div class="meta">{contato}</div>')
    linhas.append(
        f'            <div class="meta">{ICN_PINO} <a class="ver" href="{maps}" target="_blank" rel="noopener" data-es="Ver en Google Maps">Ver no Google Maps</a></div>'
    )
    corpo = "\n".join(linhas)
    return f'''      <div class="cartao inst-cartao" data-pais="Brasil" data-estado="{uf}" data-cidade="{cidade}">
        <div class="inst">
          <img src="img/selo.png?v=1" alt="Selo de certificação" style="opacity:0.45;">
          <div>
            <span class="badge verif" data-es="EN VERIFICACIÓN">EM VERIFICAÇÃO</span>
            <h3 style="margin-top:8px;">{nome}</h3>
{corpo}
          </div>
        </div>
      </div>'''

html = ALVO.read_text(encoding="utf-8")
assert "GATE — Grupo Apométrico" not in html, "lote 2 já inserido"

# insere logo antes do fechamento da grade nacional (última grade c2 antes do CERTIFICAR)
idx_cert = html.index("<!-- ==================== CERTIFICAR")
fecha_grade = html.rindex("    </div>\n\n  </div>\n</section>", 0, idx_cert)
novos = "\n\n" + "\n\n".join(card(*c) for c in NOVAS) + "\n"
html = html[:fecha_grade] + novos + html[fecha_grade:]
ALVO.write_text(html, encoding="utf-8")
print(f"OK: +{len(NOVAS)} cards inseridos")
