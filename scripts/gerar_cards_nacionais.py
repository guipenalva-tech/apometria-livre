# -*- coding: utf-8 -*-
"""Gera os cards do mapeamento nacional e insere em site/instituicoes.html.
Fonte dos dados: docs/10-mapeamento-nacional.md (seleção curada, tudo EM VERIFICAÇÃO)."""
import pathlib, urllib.parse

SITE = pathlib.Path(__file__).resolve().parent.parent / "site"
ALVO = SITE / "instituicoes.html"

ICN_PINO = "<svg class='icn' aria-hidden='true'><use href='img/icones.svg#pino'/></svg>"
ICN_LINK = "<svg class='icn' aria-hidden='true'><use href='img/icones.svg#link'/></svg>"

# (nome, cidade, uf, endereço, contato_html_ou_None, consulta_maps)
CASAS = [
    ("Fraternidade Espiritualista Fonte de Luz", "Brasília", "DF", "SCRLN 714/715 Bloco B Loja 34 – Asa Norte",
     "<a class=\"ver\" href=\"http://www.fraternidadefontedeluz.org\" target=\"_blank\" rel=\"noopener\">fraternidadefontedeluz.org</a>",
     "Fraternidade Fonte de Luz SCRLN 714 Asa Norte Brasilia"),
    ("Oficina de Apometria da Casa de Eurípedes", "Goiânia", "GO", "Via Ana Luzia de Jesus, s/n – Setor Rio Formoso", None,
     "Casa de Euripedes Goiania"),
    ("Central de Estudos Dr. Lacerda", "Luziânia", "GO", "Pç. Evangelino Meireles, 37 (fundos) – Centro", "☏ (61) 3622-8767",
     "Praca Evangelino Meireles 37 Luziania GO"),
    ("Casa Apométrica", "Primavera do Leste", "MT", "Rua Jasmim, 68 – Cond. Pioneiro", None,
     "Rua Jasmim 68 Primavera do Leste MT"),
    ("Grupo Apométrico Rosas Azuis", "Campo Grande", "MS", "Av. das Bandeiras, 2196 Casa 2 – Marcos Roberto", None,
     "Avenida das Bandeiras 2196 Campo Grande MS"),
    ("Centro Unidos Para o Reino", "Castanhal", "PA", "Rua Cônego Luís Leitão, 2350 – Centro", None,
     "Rua Conego Luis Leitao 2350 Castanhal PA"),
    ("CEPEC — Centro de Pesquisas Espirituais Caminheiros", "Curitiba", "PR", "Atendimento e curso de Apometria gratuitos",
     "<a class=\"ver\" href=\"https://www.cepeccuritiba.org.br\" target=\"_blank\" rel=\"noopener\">cepeccuritiba.org.br</a>",
     "CEPEC Centro de Pesquisas Espirituais Caminheiros Curitiba"),
    ("Núcleo Espírita de Estudos Apométricos", "Londrina", "PR", "Rua Ponta Grossa, 399",
     "✎ apometrialondrina@gmail.com", "Rua Ponta Grossa 399 Londrina PR"),
    ("Centro de Apometria “Chico Xavier”", "Ponta Grossa", "PR", "Rua Coronel Cláudio, 248 – Calçadão, Centro",
     "☏ (42) 3025-3002", "Rua Coronel Claudio 248 Ponta Grossa PR"),
    ("Lar Escola Seara do Bem", "Foz do Iguaçu", "PR", "R. Cap. Kleber Becker, 262 – V. Iolanda",
     "<a class=\"ver\" href=\"http://www.apometrialarescola.com.br\" target=\"_blank\" rel=\"noopener\">apometrialarescola.com.br</a>",
     "Lar Escola Seara do Bem Foz do Iguacu"),
    ("Apometria Novos Horizontes", "Olinda", "PE", "Rua Tupiaras, 202 – Cidade Tabajara", "☏ (81) 3433-7000",
     "Rua Tupiaras 202 Olinda PE"),
    ("MAP — Movimento de Amor ao Próximo", "Rio de Janeiro", "RJ", "Estrada do Pau Ferro, 325 – Pechincha",
     "<a class=\"ver\" href=\"https://www.map.org.br\" target=\"_blank\" rel=\"noopener\">map.org.br</a>",
     "MAP Movimento de Amor ao Proximo Estrada do Pau Ferro 325 Rio de Janeiro"),
    ("FEAP — Fraternidade Espírita Amor e Paz", "Rio de Janeiro", "RJ", "Rua General Roca, 391 – Tijuca", "☏ (21) 2587-8687",
     "Rua General Roca 391 Tijuca Rio de Janeiro"),
    ("Centro Cultural Espírita Jardelino Ramos", "Caxias do Sul", "RS", "Av. Assis Brasil, 363 – Jardelino Ramos", None,
     "Avenida Assis Brasil 363 Caxias do Sul RS"),
    ("Núcleo Ramatís", "São Leopoldo", "RS", "Rua Bento Gonçalves, 441", None,
     "Rua Bento Goncalves 441 Sao Leopoldo RS"),
    ("GEPER — Grupo de Estudos e Práticas Espiritualista Ramatis", "Santa Maria", "RS", "Av. Liberdade, 191 Casa 2", None,
     "Avenida Liberdade 191 Santa Maria RS"),
    ("Núcleo Espírita Nosso Lar", "Florianópolis", "SC", "Rua dos Tambaquis, 97 – Canasvieiras", None,
     "Nucleo Espirita Nosso Lar Canasvieiras Florianopolis"),
    ("SERTE — S.E. Recuperação, Trabalho e Educação", "Florianópolis", "SC", "Rua Allan Kardec, s/n – Centro", None,
     "SERTE Sociedade Espirita Florianopolis"),
    ("Grupo Fraternal Ramatis", "Balneário Camboriú", "SC", "Rua Acre, 219 – Bairro dos Estados",
     "<a class=\"ver\" href=\"http://www.gruporamatis.com.br\" target=\"_blank\" rel=\"noopener\">gruporamatis.com.br</a>",
     "Rua Acre 219 Balneario Camboriu SC"),
    ("Neutra Apometria", "São Paulo", "SP", "Atendimento com apometria gratuito (capital)",
     "<a class=\"ver\" href=\"https://www.neutrapometria.org.br\" target=\"_blank\" rel=\"noopener\">neutrapometria.org.br</a>",
     "Neutra Apometria Sao Paulo"),
    ("Casa do Caminho Frei Luiz", "São Paulo", "SP", "Rua das Gardênias, 5 – Mirandópolis",
     "<a class=\"ver\" href=\"https://www.freiluiz.org.br\" target=\"_blank\" rel=\"noopener\">freiluiz.org.br</a>",
     "Rua das Gardenias 5 Mirandopolis Sao Paulo"),
    ("TUPI — Templo Universalista Paz Interior", "São Paulo", "SP", "Rua Bitencourt Sampaio, 41 – Vila Mariana",
     "<a class=\"ver\" href=\"http://www.templotupi.org\" target=\"_blank\" rel=\"noopener\">templotupi.org</a>",
     "Rua Bitencourt Sampaio 41 Vila Mariana Sao Paulo"),
    ("GAAC — Grupo Amor e Caridade", "Campinas", "SP", "Rua Soldado Percílio Neto, 77 – Pq. Taquaral",
     "<a class=\"ver\" href=\"http://www.gaac.com.br\" target=\"_blank\" rel=\"noopener\">gaac.com.br</a>",
     "Rua Soldado Percilio Neto 77 Campinas SP"),
    ("GELF — Grupo Espiritualista Luz e Fraternidade", "Campinas", "SP", "Rua Prof. Heitor Mayer, 63 – Guanabara",
     "<a class=\"ver\" href=\"https://gelf.org.br\" target=\"_blank\" rel=\"noopener\">gelf.org.br</a>",
     "Rua Professor Heitor Mayer 63 Campinas SP"),
]

def card(nome, cidade, uf, endereco, contato, consulta):
    maps = "https://www.google.com/maps/search/?api=1&query=" + urllib.parse.quote_plus(consulta)
    linhas = [
        f'            <div class="meta">{endereco} · {cidade}/{uf}</div>',
    ]
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

cards = "\n\n".join(card(*c) for c in CASAS)

bloco = f'''
    <h2 style="margin-top:56px;" data-es="Mapeo nacional — en verificación">Mapeamento nacional — em verificação</h2>
    <div class="linha-ouro"></div>
    <p class="intro" data-es="Casas de otros estados y ciudades levantadas en los directorios públicos de la comunidad apométrica. Los datos son antiguos y aún no verificados — confirma dirección y gratuidad antes de visitar. La verificación presencial y por entrevistas está en curso.">
      Casas de outros estados e cidades levantadas nos diretórios públicos da comunidade apométrica. Os dados são antigos e ainda não verificados — confirme endereço e gratuidade antes de visitar. A verificação presencial e por entrevistas está em andamento.
    </p>
    <div class="grade c2">
{cards}
    </div>
'''

html = ALVO.read_text(encoding="utf-8")
marcador = "Endereços e horários devem ser confirmados diretamente com cada casa.\n    </div>"
assert marcador in html, "marcador de inserção não encontrado"
assert "Mapeamento nacional" not in html, "bloco já inserido"
html = html.replace(marcador, marcador + "\n" + bloco, 1)
ALVO.write_text(html, encoding="utf-8")
print(f"OK: {len(CASAS)} cards nacionais inseridos em instituicoes.html")
