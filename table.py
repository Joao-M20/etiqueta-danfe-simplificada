from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Spacer
from reportlab.lib import colors
from reportlab.lib.units import cm
import textwrap

# Criar o PDF
pdf_path = "etiqueta_entrega.pdf"
doc = SimpleDocTemplate(pdf_path, pagesize=A4)

# Conteúdo da tabela
data = [
    ['Nº', 'SKU(LOCAL)', 'CONTEÚDO', 'QTD.'],
]

# Criar a tabela
table = Table(data, colWidths=[1.5*cm, 4*cm, 10*cm, 1.5*cm])

# Estilo da tabela
style = TableStyle([
    ('GRID', (0,0), (-1,-1), 1, colors.black),
    ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
    ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ('ALIGN', (0,0), (-1,0), 'CENTER'),
    ('ALIGN', (0,1), (0,-1), 'CENTER'),
    ('ALIGN', (-1,1), (-1,-1), 'CENTER'),
    ('FONTSIZE', (0,0), (-1,-1), 10),
    ('LEFTPADDING', (0,0), (-1,-1), 4),
    ('RIGHTPADDING', (0,0), (-1,-1), 4),
    ('TOPPADDING', (0,0), (-1,-1), 6),
    ('BOTTOMPADDING', (0,0), (-1,-1), 6),
])

table.setStyle(style)

# Montar o PDF
elements = [table]
doc.build(elements)

print(f"PDF gerado em: {pdf_path}")












# Conteúdo da tabela
dataTable = [
    ['Nº', 'SKU(LOCAL)', 'CONTEÚDO', 'QTD.'],
]

# Criar a tabela
table = Table(dataTable, colWidths=[1.5*cm, 4*cm, 10*cm, 1.5*cm])

# Estilo da tabela
style = TableStyle([
    ('GRID', (0,0), (-1,-1), 1, colors.black),
    ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
    ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ('ALIGN', (0,0), (-1,0), 'CENTER'),
    ('ALIGN', (0,1), (0,-1), 'CENTER'),
    ('ALIGN', (-1,1), (-1,-1), 'CENTER'),
    ('FONTSIZE', (0,0), (-1,-1), 10),
    ('LEFTPADDING', (0,0), (-1,-1), 4),
    ('RIGHTPADDING', (0,0), (-1,-1), 4),
    ('TOPPADDING', (0,0), (-1,-1), 6),
    ('BOTTOMPADDING', (0,0), (-1,-1), 6),
])

table.setStyle(style)



















    #Produto
    c.setFont("Helvetica-Bold", 8)
    c.drawString(10*mm, altura - 75*mm, "CONTEÚDO:")
    y = altura - 80*mm

    for produto in data['produtos']:
        c.setFont("Helvetica", 7)
        descricao = f"{produto['codigo']} - {produto['descricao']}"
        c.drawString(10*mm, y, descricao[:45])  # limita a largura
        y -= 5*mm
        c.drawString(10*mm, y, f"Qtd: {produto['quantidade']}")
        y -= 7*mm  # espaço entre produtos