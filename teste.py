from reportlab.pdfgen import canvas
from reportlab.graphics.barcode import code128
from reportlab.lib.pagesizes import landscape, mm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Spacer
from reportlab.lib.units import mm
from reportlab.lib.units import cm
import textwrap
from reportlab.lib import colors


import xml.etree.ElementTree as ET
from io import BytesIO



def parse_nfe_xml(xml_path):
    ns = {'nfe': 'http://www.portalfiscal.inf.br/nfe'}
    tree = ET.parse(xml_path)
    root = tree.getroot()

    # Chave de acesso - está dentro da tag infNFe id="NFe123456789..."
    infNFe = root.find('.//nfe:infNFe', ns)
    chave = infNFe.attrib['Id'][3:]  # remove 'NFe' do começo

    emit = root.find('.//nfe:emit', ns)
    emit_nome = emit.find('nfe:xNome', ns).text

    dest = root.find('.//nfe:dest', ns)
    dest_nome = dest.find('nfe:xNome', ns).text if dest is not None else 'Consumidor Final'

    ide = root.find('.//nfe:ide', ns)
    nNF = ide.find('nfe:nNF', ns).text
    dhEmi = ide.find('nfe:dhEmi', ns)
    data_emissao = dhEmi.text if dhEmi is not None else ide.find('nfe:dhEmi', ns).text

    total = root.find('.//nfe:total/nfe:ICMSTot', ns)
    vNF = total.find('nfe:vNF', ns).text

    # Lista de produtos
    produtos = []
    for det in root.findall('.//nfe:det', ns):
        prod = det.find('nfe:prod', ns)
        if prod is not None:
            codigo = prod.find('nfe:cProd', ns).text
            descricao = prod.find('nfe:xProd', ns).text
            quantidade = prod.find('nfe:qCom', ns).text
            produtos.append({
                'codigo': codigo,
                'descricao': descricao,
                'quantidade': quantidade
            })

    return {
        'chave': chave,
        'emit_nome': emit_nome,
        'dest_nome': dest_nome,
        'nNF': nNF,
        'data_emissao': data_emissao,
        'vNF': vNF,
        'produtos': produtos
    }



######################################################

def gerar_danfe_simples(data, output_pdf):
    largura = 60 * mm
    altura = 100 * mm
    c = canvas.Canvas(output_pdf, pagesize=(largura, altura))

    # Cabeçalho
    c.setFont("Helvetica-Bold", 8)
    c.drawString(5*mm, altura - 10*mm, "DANFE SIMPLIFICADA - ETIQUETA")

    # Loja e Cliente
    c.setFont("Helvetica", 6)
    c.drawString(10*mm, altura - 16*mm, "Loja: Liora Jeans")
    #c.drawString(10*mm, altura - 22*mm, "Cliente: Alan Rodrigo Quispe")
    c.drawString(10*mm, altura - 22*mm, f"Cliente: {data['dest_nome'][:40]}")
    c.drawString(10*mm, altura - 27*mm, "Pagamento: 03-07-2025 13:55:02")
    c.drawString(10*mm, altura - 32*mm, "Vencimento: 03-07-2025 23:59:59")

    # Número e série
    #c.drawString(10*mm, altura - 37*mm, "Número: 0001051381   Série: 003")
    c.drawString(10*mm, altura - 37*mm, f"Numero: {data['nNF']}   Emissão:{data['data_emissao'][:10]}")

    # Código de barras
    #chave = "3525073515220000144550030005138111321940"
    #barcode = code128.Code128(chave, barHeight=20*mm, barWidth=0.4)
    #barcode.drawOn(c, 10*mm, altura - 60*mm)

    # Código de barras da chave de acesso (usando code128)
    barcode = code128.Code128(data['chave'], barHeight=20*mm, barWidth=0.4)
    barcode.drawOn(c, 5*mm, altura - 60*mm)




    # Chave formatada
    #chave_formatada = ' '.join([chave[i:i+4] for i in range(0, len(chave), 4)])
    #c.setFont("Helvetica", 6)
    #c.drawString(10*mm, altura - 65*mm, chave_formatada)

    # Chave de acesso (quebrada em blocos de 4 caracteres para leitura)
    chave_formatada = ' '.join([data['chave'][i:i+4] for i in range(0, len(data['chave']), 4)])
    c.setFont("Helvetica", 5)
    c.drawString(5*mm, altura - 65*mm, chave_formatada)








    # Cabeçalho da tabela
    tabela_dados = [
        ['Nº', 'CODIGO', 'CONTEÚDO', 'QTD.'],
    ]

    # Adiciona cada produto na tabela, quebrando descrição para não estourar a largura
    for i, produto in enumerate(data['produtos'], start=1):
        codigo = produto['codigo']
        descricao = produto['descricao']
        quantidade = produto['quantidade']

        # Quebrar descrição em linhas de até 50 caracteres para caber na célula
        descricao_wrapped = '\n'.join(textwrap.wrap(descricao, width=50))

        tabela_dados.append([str(i), codigo, descricao_wrapped, quantidade])

    # Agora você pode criar a tabela com o data preenchido:
    #table = Table(tabela_dados, colWidths=[1.5*cm, 4*cm, 10*cm, 1.5*cm])
    table = Table(tabela_dados, colWidths=[0.8*cm, 2.2*cm, 4.5*cm, 1*cm]  # Total ~8.5cm (85mm), ideal para 60mm de largura útil
)


    # (Estilo permanece igual ao que você já escreveu)
    style = TableStyle([
    ('GRID', (0,0), (-1,-1), 0.5, colors.black),
    ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
    ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ('ALIGN', (0,0), (-1,0), 'CENTER'),
    ('ALIGN', (0,1), (0,-1), 'CENTER'),
    ('ALIGN', (-1,1), (-1,-1), 'CENTER'),
    ('FONTSIZE', (0,0), (-1,-1), 6),  # fonte menor
    ('LEFTPADDING', (0,0), (-1,-1), 2),
    ('RIGHTPADDING', (0,0), (-1,-1), 2),
    ('TOPPADDING', (0,0), (-1,-1), 2),
    ('BOTTOMPADDING', (0,0), (-1,-1), 2),
    ])


    table.setStyle(style)

    # Define a posição da tabela no canvas (ajuste conforme necessário)
    x = 5 * mm
    y = altura - 85 * mm  # ajustar conforme layout

    # Prepara a tabela e a desenha no canvas
    table.wrapOn(c, largura, altura)
    table.drawOn(c, x, y)





    c.showPage()
    c.save()

if __name__ == "__main__":
    xml_file = "xmlTeste.xml"  # substitua pelo seu arquivo XML da NF-e
    dados = parse_nfe_xml(xml_file)
    gerar_danfe_simples(dados, "danfe_etiqueta.pdf")


