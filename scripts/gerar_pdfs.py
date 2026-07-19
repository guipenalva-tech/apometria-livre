# -*- coding: utf-8 -*-
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, HRFlowable, Table, TableStyle, PageBreak
)
from reportlab.lib import colors
from reportlab.pdfgen import canvas as canvas_mod

NAVY = colors.HexColor("#1b2a52")
GOLD = colors.HexColor("#c9992e")
CREAM = colors.HexColor("#faf7f0")
TEXT = colors.HexColor("#2a2f3a")
SUAVE = colors.HexColor("#5a6172")

def estilos():
    s = {}
    s['titulo'] = ParagraphStyle('titulo', fontName='Times-Bold', fontSize=25, leading=30,
                                  textColor=NAVY, alignment=TA_CENTER, spaceAfter=4)
    s['subtitulo'] = ParagraphStyle('subtitulo', fontName='Helvetica-Oblique', fontSize=12.5, leading=16,
                                     textColor=SUAVE, alignment=TA_CENTER, spaceAfter=14)
    s['h2'] = ParagraphStyle('h2', fontName='Times-Bold', fontSize=15, leading=19,
                              textColor=NAVY, spaceBefore=16, spaceAfter=6)
    s['corpo'] = ParagraphStyle('corpo', fontName='Helvetica', fontSize=10.3, leading=15.5,
                                 textColor=TEXT, alignment=TA_JUSTIFY, spaceAfter=8)
    s['citacao'] = ParagraphStyle('citacao', fontName='Times-Italic', fontSize=13, leading=18,
                                   textColor=NAVY, alignment=TA_CENTER, spaceBefore=10, spaceAfter=4)
    s['citacao_autor'] = ParagraphStyle('citacao_autor', fontName='Helvetica-Bold', fontSize=9.5,
                                         textColor=GOLD, alignment=TA_CENTER, spaceAfter=10)
    s['lista'] = ParagraphStyle('lista', fontName='Helvetica', fontSize=10.3, leading=15.5,
                                 textColor=TEXT, leftIndent=14, spaceAfter=5)
    s['termo'] = ParagraphStyle('termo', fontName='Times-Bold', fontSize=12, leading=15,
                                 textColor=NAVY, spaceBefore=10, spaceAfter=2)
    s['definicao'] = ParagraphStyle('definicao', fontName='Helvetica', fontSize=10.3, leading=15,
                                     textColor=TEXT, alignment=TA_JUSTIFY, spaceAfter=2)
    s['rodape_aviso'] = ParagraphStyle('rodape_aviso', fontName='Helvetica-Oblique', fontSize=8.3,
                                        textColor=SUAVE, alignment=TA_CENTER, leading=11)
    return s

def capa_rodape(nome_doc):
    def desenhar(c: canvas_mod.Canvas, doc):
        largura, altura = A4
        # barra superior
        c.setFillColor(NAVY)
        c.rect(0, altura - 1.6*cm, largura, 1.6*cm, fill=1, stroke=0)
        c.setFillColor(GOLD)
        c.rect(0, altura - 1.65*cm, largura, 0.05*cm, fill=1, stroke=0)
        c.setFillColor(colors.white)
        c.setFont('Times-Bold', 11)
        c.drawString(1.8*cm, altura - 1.12*cm, "APOMETRIA LIVRE")
        c.setFont('Helvetica', 8)
        c.drawRightString(largura - 1.8*cm, altura - 1.12*cm, "caridade é apometria")
        # rodapé
        c.setFillColor(SUAVE)
        c.setFont('Helvetica', 7.5)
        c.drawCentredString(largura/2, 1.1*cm,
            f"{nome_doc} · Movimento Apometria Livre · apometrialivre.org.br (modelo) · página {doc.page}")
        c.setStrokeColor(GOLD)
        c.setLineWidth(0.6)
        c.line(1.8*cm, 1.4*cm, largura - 1.8*cm, 1.4*cm)
    return desenhar

MARGEM = 2.2*cm

def novo_doc(caminho):
    return SimpleDocTemplate(caminho, pagesize=A4,
                              topMargin=2.6*cm, bottomMargin=2.2*cm,
                              leftMargin=MARGEM, rightMargin=MARGEM)

# ============================================================
# PDF 1 — Apostila introdutória
# ============================================================
def gerar_apostila():
    s = estilos()
    doc = novo_doc("apostila-o-que-e-a-apometria.pdf")
    story = []

    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph("O que é a Apometria?", s['titulo']))
    story.append(Paragraph("Um guia de acolhimento — Movimento Apometria Livre", s['subtitulo']))
    story.append(HRFlowable(width="30%", thickness=1.5, color=GOLD, spaceAfter=14, hAlign='CENTER'))

    story.append(Paragraph("1. Definição", s['h2']))
    story.append(Paragraph(
        "A Apometria é um conjunto de procedimentos de <b>assistência espiritual pelo comando mental</b>, "
        "sistematizado em 1965 pelo médico José Lacerda de Azevedo no Hospital Espírita de Porto Alegre (RS), "
        "a partir de uma técnica anterior chamada “hipnometria”, apresentada pelo farmacêutico "
        "porto-riquenho Luiz Rodrigues. O nome vem do grego <i>apo</i> (além de, separação) + <i>metron</i> "
        "(medida) — escolhido para diferenciar a técnica da hipnose.", s['corpo']))
    story.append(Paragraph(
        "Segundo seus praticantes, a técnica promove o desdobramento dos corpos espirituais para tratamento "
        "no plano espiritual, com auxílio de equipes espirituais — sempre em grupo, dentro de instituição "
        "idônea, com trabalhadores formados por estudo programado e prática supervisionada.", s['corpo']))

    story.append(Paragraph("2. Quem foi Dr. José Lacerda de Azevedo", s['h2']))
    story.append(Paragraph(
        "Nascido em 12/06/1919 e desencarnado em 29/11/1997, formou-se em Medicina pela UFRGS (turma de 1951). "
        "Foi cirurgião geral, ginecologista e, por último, clínico geral — <b>não era psiquiatra</b>, como "
        "muitos pensam. Exerceu a medicina até o fim da vida, dedicando-se a unir ciência e espiritualidade. "
        "Escreveu as obras <i>Espírito/Matéria: Novos Horizontes para a Medicina</i> (1988) e "
        "<i>Energia e Espírito</i>.", s['corpo']))

    story.append(Paragraph("3. Os fundamentos da prática correta", s['h2']))
    for item in [
        "<b>Amor</b> — a base essencial de todo o trabalho.",
        "<b>Caridade</b> — o acompanhamento necessário: atendimento sempre gratuito, sem exceção.",
        "<b>Humildade</b> — serviço anônimo, sem promoção pessoal.",
        "<b>Estudo sério</b> — formação programada dentro da instituição, com prática supervisionada.",
        "<b>Instituição idônea</b> — trabalho em grupo, nunca em consultório individual pago.",
        "<b>Respeito à medicina</b> — o assistido é sempre orientado a manter seus tratamentos de saúde.",
    ]:
        story.append(Paragraph("•  " + item, s['lista']))

    story.append(Paragraph("4. O que a Apometria NÃO é", s['h2']))
    for item in [
        "<b>Não é medicina</b> — é prática espiritual complementar, sem reconhecimento científico. Jamais substitui médico, psicólogo ou medicação.",
        "<b>Não é serviço pago</b> — “Apometria paga não é caridade, portanto, não é Apometria” (Casa do Jardim).",
        "<b>Não é curso rápido</b> — certificados vendidos online, de poucas horas, não formam trabalhadores.",
        "<b>Não é magia nem milagre</b> — é trabalho gradual de assistência, ligado à transformação íntima do assistido.",
        "<b>Não é hipnose</b> — o próprio nome foi criado para diferenciar a técnica da hipnose.",
        "<b>Não é religião nova</b> — é técnica usada por casas espíritas, umbandistas e espiritualistas.",
    ]:
        story.append(Paragraph("✕  " + item, s['lista']))

    story.append(Spacer(1, 6))
    story.append(HRFlowable(width="100%", thickness=0.6, color=GOLD, spaceAfter=10))
    story.append(Paragraph("“Apometria sem amor é magia.”", s['citacao']))
    story.append(Paragraph("— Dr. José Lacerda de Azevedo", s['citacao_autor']))

    story.append(Spacer(1, 10))
    story.append(Paragraph(
        "<b>AVISO —</b> A Apometria é uma prática espiritual complementar e não substitui nenhum tratamento "
        "médico ou psicológico. Confie apenas em casas certificadas — verifique o selo e o diretório em "
        "apometrialivre.org.br (modelo).", s['rodape_aviso']))

    doc.build(story, onFirstPage=capa_rodape("Apostila introdutória"),
               onLaterPages=capa_rodape("Apostila introdutória"))
    print("OK:", doc.filename)

# ============================================================
# PDF 2 — Glossário
# ============================================================
TERMOS = [
    ("Apometria", "Do grego <i>apo</i> (além de, separação) + <i>metron</i> (medida). Conjunto de "
     "procedimentos de assistência espiritual pelo comando mental, sistematizado por Dr. José Lacerda de "
     "Azevedo em 1965, em Porto Alegre (RS)."),
    ("Casa apométrica / instituição idônea", "Instituição espírita, umbandista ou espiritualista que "
     "pratica a Apometria em grupo, de forma gratuita, com trabalhadores formados por estudo programado."),
    ("Comando mental", "Orientação verbal, feita pelo dirigente do trabalho, que conduz e organiza a "
     "atuação da equipe espiritual e dos trabalhadores durante a reunião apométrica."),
    ("Corpos espirituais / perispírito", "Conceito espírita clássico (Allan Kardec) que designa o envoltório "
     "semimaterial que liga o espírito ao corpo físico — base conceitual sobre a qual a Apometria trabalha."),
    ("Desdobramento", "Separação temporária, no plano espiritual, entre os corpos espirituais e o corpo "
     "físico do assistido ou do médium, com finalidade de assistência — não deve ser confundido com técnicas "
     "de indução hipnótica."),
    ("Equipe espiritual", "Conjunto de espíritos que, segundo a doutrina espírita e espiritualista, atuam "
     "voluntariamente no auxílio aos trabalhos de caridade, incluindo a Apometria."),
    ("Gratuidade", "Princípio fundador da Apometria: o atendimento espiritual nunca é cobrado. “De graça "
     "recebemos, de graça devemos dar.” A venda de livros ou bazares para manutenção da casa é distinta "
     "e tradicionalmente aceita."),
    ("Hospital espiritual", "Conceito da literatura espírita (ex.: obras psicografadas por Chico Xavier) que "
     "descreve locais no plano espiritual dedicados ao tratamento e recuperação de espíritos — referência "
     "cultural para compreender o trabalho apométrico, não um local físico."),
    ("Legado Dr. Lacerda", "O conjunto de princípios, obras e método deixado pelo Dr. José Lacerda de "
     "Azevedo (1919–1997), preservado pela Casa do Jardim (Porto Alegre) e pelas demais casas certificadas."),
    ("Médium / trabalhador", "Pessoa que, após formação estruturada dentro de uma casa idônea, participa "
     "ativamente das reuniões de Apometria, sempre de forma voluntária e não remunerada."),
    ("Selo de certificação", "Ícone público concedido pela associação Apometria Livre às instituições "
     "verificadas — aponta para o diretório oficial, onde qualquer pessoa pode confirmar sua autenticidade."),
]

def gerar_glossario():
    s = estilos()
    doc = novo_doc("glossario-apometria.pdf")
    story = []

    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph("Glossário da Apometria", s['titulo']))
    story.append(Paragraph("Termos essenciais para quem está conhecendo a prática", s['subtitulo']))
    story.append(HRFlowable(width="30%", thickness=1.5, color=GOLD, spaceAfter=14, hAlign='CENTER'))

    story.append(Paragraph(
        "Este glossário explica conceitos gerais da Apometria em linguagem simples. Ele não ensina a "
        "técnica — a prática correta se aprende dentro de uma casa idônea, com estudo programado e "
        "supervisão. Os termos estão em ordem alfabética.", s['corpo']))
    story.append(Spacer(1, 6))

    termos_ordenados = sorted(TERMOS, key=lambda t: t[0])
    for termo, definicao in termos_ordenados:
        story.append(Paragraph(termo, s['termo']))
        story.append(Paragraph(definicao, s['definicao']))

    story.append(Spacer(1, 14))
    story.append(HRFlowable(width="100%", thickness=0.6, color=GOLD, spaceAfter=10))
    story.append(Paragraph(
        "<b>AVISO —</b> A Apometria é uma prática espiritual complementar e não substitui nenhum tratamento "
        "médico ou psicológico. Confie apenas em casas certificadas — verifique o selo e o diretório em "
        "apometrialivre.org.br (modelo).", s['rodape_aviso']))

    doc.build(story, onFirstPage=capa_rodape("Glossário"),
               onLaterPages=capa_rodape("Glossário"))
    print("OK:", doc.filename)

# ============================================================
# PDF 3 — Carta-Manifesto (PT + ES)
# ============================================================
CARTA_PT_PARAGRAFOS = [
    ("Nós, instituições espíritas, umbandistas e espiritualistas que praticamos a Apometria conforme os "
     "princípios estabelecidos pelo Dr. José Lacerda de Azevedo, vimos a público reafirmar o que sempre "
     "foi — e o que jamais poderá deixar de ser — esta técnica de assistência espiritual."),
    ("A Apometria nasceu em 1965, no Hospital Espírita de Porto Alegre, das mãos de um médico que dedicou "
     "a vida a unir ciência e espiritualidade. Dr. Lacerda nos ensinou que o amor é a base essencial deste "
     "trabalho, que a caridade é seu acompanhamento necessário, e que a humildade e o serviço anônimo são "
     "o caminho de quem o pratica. Ele nos deixou um alerta que hoje ressoa mais forte do que nunca: "
     "<i>“Apometria sem amor é magia.”</i>"),
    ("Vemos com tristeza a multiplicação de consultórios, cursos rápidos e certificados vendidos que usam "
     "o nome da Apometria — e o nome do Dr. Lacerda — como mercadoria. A quem chega a essas portas, "
     "declaramos com clareza:"),
    ("<b>1.</b> Apometria paga não é caridade — portanto, não é Apometria. O atendimento espiritual é "
     "gratuito, sempre. “De graça recebemos, de graça devemos dar.”"),
    ("<b>2.</b> A Apometria não substitui a medicina. Ela é assistência espiritual complementar. Toda casa "
     "séria orienta seus assistidos a manterem seus tratamentos médicos e psicológicos."),
    ("<b>3.</b> A Apometria não se aprende em um fim de semana. A formação séria acontece dentro das "
     "casas, com estudo programado, prática supervisionada e compromisso moral — ao longo de meses e anos."),
    ("<b>4.</b> A Apometria é trabalho de grupo, dentro de instituição idônea — não prática individual de "
     "consultório."),
    ("Por isso nos unimos em associação, para <b>educar</b> o público sobre o que a Apometria é e o que "
     "ela não é; <b>certificar</b>, por meio de selo público e verificável, as casas que praticam a "
     "Apometria autêntica e gratuita; <b>amparar</b> as casas novas que desejem trilhar o caminho correto; "
     "e <b>preservar</b> o legado do Dr. José Lacerda de Azevedo para as gerações futuras."),
    ("Convidamos toda instituição que compartilhe destes princípios a somar-se a este movimento. E pedimos "
     "ao público: <b>confie apenas nas casas certificadas — e desconfie sempre de quem cobra pela "
     "caridade.</b>"),
]

CARTA_ES_PARAGRAFOS = [
    ("Nosotras, instituciones espíritas, umbandistas y espiritualistas que practicamos la Apometría según "
     "los principios establecidos por el Dr. José Lacerda de Azevedo, venimos públicamente a reafirmar lo "
     "que siempre fue — y lo que jamás podrá dejar de ser — esta técnica de asistencia espiritual."),
    ("La Apometría nació en 1965, en el Hospital Espírita de Porto Alegre (Brasil), de las manos de un "
     "médico que dedicó su vida a unir ciencia y espiritualidad. El Dr. Lacerda nos enseñó que el amor es "
     "la base esencial de este trabajo, que la caridad es su acompañamiento necesario, y que la humildad y "
     "el servicio anónimo son el camino de quien lo practica. Nos dejó una advertencia que hoy resuena más "
     "fuerte que nunca: <i>“Apometría sin amor es magia.”</i>"),
    ("Vemos con tristeza la multiplicación de consultorios, cursos rápidos y certificados vendidos que usan "
     "el nombre de la Apometría — y el nombre del Dr. Lacerda — como mercancía. A quien llega a esas "
     "puertas, declaramos con claridad:"),
    ("<b>1.</b> La Apometría pagada no es caridad — por lo tanto, no es Apometría. La asistencia espiritual "
     "es gratuita, siempre. “Gratis recibimos, gratis debemos dar.”"),
    ("<b>2.</b> La Apometría no sustituye a la medicina. Es asistencia espiritual complementaria. Toda casa "
     "seria orienta a sus asistidos a mantener sus tratamientos médicos y psicológicos."),
    ("<b>3.</b> La Apometría no se aprende en un fin de semana. La formación seria ocurre dentro de las "
     "casas, con estudio programado, práctica supervisada y compromiso moral — a lo largo de meses y años."),
    ("<b>4.</b> La Apometría es trabajo de grupo, dentro de una institución idónea — no práctica individual "
     "de consultorio."),
    ("Por eso nos unimos en asociación, para <b>educar</b> al público sobre lo que la Apometría es y lo que "
     "no es; <b>certificar</b>, mediante un sello público y verificable, a las casas que practican la "
     "Apometría auténtica y gratuita; <b>amparar</b> a las casas nuevas que deseen recorrer el camino "
     "correcto; y <b>preservar</b> el legado del Dr. José Lacerda de Azevedo para las generaciones futuras."),
    ("Invitamos a toda institución que comparta estos principios a sumarse a este movimiento. Y pedimos al "
     "público: <b>confíe solamente en las casas certificadas — y desconfíe siempre de quien cobra por la "
     "caridad.</b>"),
]

def gerar_carta_manifesto():
    s = estilos()
    doc = novo_doc("carta-manifesto.pdf")
    story = []

    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph("Carta-Manifesto do Movimento", s['titulo']))
    story.append(Paragraph("Carta às Casas de Apometria do Brasil — pelo Legado do Dr. Lacerda", s['subtitulo']))
    story.append(HRFlowable(width="30%", thickness=1.5, color=GOLD, spaceAfter=14, hAlign='CENTER'))
    for p in CARTA_PT_PARAGRAFOS:
        story.append(Paragraph(p, s['corpo']))

    story.append(Spacer(1, 10))
    story.append(Paragraph("Assinam as instituições fundadoras, <i>(local e data)</i>", s['corpo']))
    tabela = Table([["Instituição", "Cidade/UF", "Dirigente responsável", "Assinatura"],
                     ["", "", "", ""], ["", "", "", ""], ["", "", "", ""]],
                    colWidths=[4.3*cm, 2.6*cm, 4.3*cm, 4.3*cm], rowHeights=[0.8*cm, 0.9*cm, 0.9*cm, 0.9*cm])
    tabela.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), NAVY),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 8.5),
        ('GRID', (0, 0), (-1, -1), 0.6, GOLD),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(tabela)

    story.append(PageBreak())
    story.append(Paragraph("Carta-Manifiesto del Movimiento", s['titulo']))
    story.append(Paragraph("Carta a las Casas de Apometría — por el Legado del Dr. Lacerda", s['subtitulo']))
    story.append(HRFlowable(width="30%", thickness=1.5, color=GOLD, spaceAfter=14, hAlign='CENTER'))
    for p in CARTA_ES_PARAGRAFOS:
        story.append(Paragraph(p, s['corpo']))
    story.append(Spacer(1, 10))
    story.append(Paragraph("Firman las instituciones fundadoras, <i>(lugar y fecha)</i>", s['corpo']))

    doc.build(story, onFirstPage=capa_rodape("Carta-Manifesto"),
               onLaterPages=capa_rodape("Carta-Manifesto"))
    print("OK:", doc.filename)

if __name__ == "__main__":
    gerar_apostila()
    gerar_glossario()
    gerar_carta_manifesto()
