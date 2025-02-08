import os
from docx import Document
from PIL import Image
from io import BytesIO

# Caminhos dos arquivos
doc_path = r"C:\Users\Douglas\Desktop\NOMARKWATER\PDF_BASE.docx"
nova_imagem_path = r"C:\Users\Douglas\Desktop\NOMARKWATER\NOMARKWATER.png"
output_path = r"C:\Users\Douglas\Desktop\NOMARKWATER\PDF_BASE_NOMARKWATER.docx"

def substituir_imagens_em_todas_paginas(doc_path, nova_imagem_path, output_path):
    # Abre o documento Word
    doc = Document(doc_path)
    
    # Carrega a nova imagem
    nova_imagem = Image.open(nova_imagem_path)
    
    # Itera sobre todas as imagens no documento
    for rel in list(doc.part.rels.values()):
        if "image" in rel.target_ref:
            # Obtém a imagem original
            img_part = rel.target_part
            img_data = img_part.blob

            # Carrega a imagem original para obter dimensões
            img_original = Image.open(BytesIO(img_data))
            largura_original, altura_original = img_original.size

            # Redimensiona a nova imagem para as dimensões da original
            nova_imagem_redimensionada = nova_imagem.resize((largura_original, altura_original), Image.Resampling.LANCZOS)

            # Converte a imagem para bytes
            img_bytes = BytesIO()
            nova_imagem_redimensionada.save(img_bytes, format='PNG')  # Salva no formato PNG
            img_part._blob = img_bytes.getvalue()  # Substitui a imagem no documento

            print(f"Substituiu uma imagem ({largura_original}px x {altura_original}px).")
    
    # Salva o documento modificado
    doc.save(output_path)
    print(f"Documento salvo com sucesso em: {output_path}")

# Chama a função para substituir as imagens
substituir_imagens_em_todas_paginas(doc_path, nova_imagem_path, output_path)
