from reportlab.pdfgen import canvas
from reportlab.graphics.barcode import code128
from reportlab.lib.pagesizes import landscape, mm
from reportlab.lib.units import mm

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

    return {
        'chave': chave,
        'emit_nome': emit_nome,
        'dest_nome': dest_nome,
        'nNF': nNF,
        'data_emissao': data_emissao,
        'vNF': vNF
    }

def gerar_danfe_simples(output_pdf):
    largura = 100 * mm
    altura = 150 * mm
    c = canvas.Canvas(output_pdf, pagesize=(largura, altura))

    # Cabeçalho
    c.setFont("Helvetica-Bold", 10)
    c.drawString(10*mm, altura - 10*mm, "DANFE SIMPLIFICADA - ETIQUETA")

    # Loja e Cliente
    c.setFont("Helvetica", 8)
    c.drawString(10*mm, altura - 17*mm, "Loja: Elephant Shop")
    c.drawString(10*mm, altura - 22*mm, "Cliente: Alan Rodrigo Quispe")
    c.drawString(10*mm, altura - 27*mm, "Pagamento: 03-07-2025 13:55:02")
    c.drawString(10*mm, altura - 32*mm, "Vencimento: 03-07-2025 23:59:59")

    # Número e série
    c.drawString(10*mm, altura - 37*mm, "Número: 0001051381   Série: 003")

    # Código de barras
    chave = "3525073515220000144550030005138111321940"
    barcode = code128.Code128(chave, barHeight=20*mm, barWidth=0.4)
    barcode.drawOn(c, 10*mm, altura - 60*mm)

    # Chave formatada
    chave_formatada = ' '.join([chave[i:i+4] for i in range(0, len(chave), 4)])
    c.setFont("Helvetica", 6)
    c.drawString(10*mm, altura - 65*mm, chave_formatada)

    # Produto
    c.setFont("Helvetica-Bold", 8)
    c.drawString(10*mm, altura - 75*mm, "CONTEÚDO:")
    c.setFont("Helvetica", 7)
    c.drawString(10*mm, altura - 80*mm, "MDK-2074A - Impressora Térmica Para Código De Barras")
    c.drawString(10*mm, altura - 85*mm, "E Etiquetas 203dpi 110v/220v Tomate")

    # Quantidade
    c.drawString(10*mm, altura - 90*mm, "Qtd: 1")

    c.showPage()
    c.save()

if __name__ == "__main__":
    xml_file = "xmlTeste.xml"  # substitua pelo seu arquivo XML da NF-e
    dados = parse_nfe_xml(xml_file)
    gerar_danfe_simples("danfe_etiqueta.pdf")


