import xml.etree.ElementTree as ET
from reportlab.pdfgen import canvas
from reportlab.graphics.barcode import code128
from reportlab.lib.pagesizes import landscape, mm
from reportlab.lib.units import mm
import qrcode
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


#######################################################

def generate_danfe_etiqueta(data, output_pdf):
    largura = 60 * mm
    altura = 100 * mm
    c = canvas.Canvas(output_pdf, pagesize=(largura, altura))

    # Cabeçalho
    c.setFont("Helvetica-Bold", 8)
    c.drawString(5*mm, altura - 10*mm, "DANFE SIMPLIFICADO - ETIQUETA")

    # Emitente
    c.setFont("Helvetica", 6)
    c.drawString(5*mm, altura - 15*mm, f"Emitente: {data['emit_nome'][:40]}")

    # Destinatário
    c.drawString(5*mm, altura - 20*mm, f"Dest: {data['dest_nome'][:40]}")

    # NF-e Número e Data
    c.drawString(5*mm, altura - 25*mm, f"Número: {data['nNF']}   Emissão: {data['data_emissao'][:10]}")

    # Valor total
    c.drawString(5*mm, altura - 30*mm, f"Valor Total: R$ {data['vNF']}")

    # Código de barras da chave de acesso (usando code128)
    barcode = code128.Code128(data['chave'], barHeight=20*mm, barWidth=0.4)
    barcode.drawOn(c, 5*mm, altura - 60*mm)

    # Chave de acesso (quebrada em blocos de 4 caracteres para leitura)
    chave_formatada = ' '.join([data['chave'][i:i+4] for i in range(0, len(data['chave']), 4)])
    c.setFont("Helvetica", 5)
    c.drawString(5*mm, altura - 65*mm, chave_formatada)

    c.showPage()
    c.save()

if __name__ == "__main__":
    xml_file = "xmlTeste.xml"  # substitua pelo seu arquivo XML da NF-e
    dados = parse_nfe_xml(xml_file)
    generate_danfe_etiqueta(dados, "danfe_etiqueta.pdf")
