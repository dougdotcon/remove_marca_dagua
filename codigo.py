!apt-get install -y poppler-utils
!pip install opencv-python numpy pdf2image pillow pytesseract python-docx

import cv2
import numpy as np
from pdf2image import convert_from_path
from PIL import Image
import os
from google.colab import files

# Upload do arquivo PDF
uploaded = files.upload()
pdf_path = list(uploaded.keys())[0]

# Converter PDF para imagens (300 DPI para qualidade alta)
images = convert_from_path(pdf_path, 300)

# Criar uma pasta para armazenar imagens temporárias
output_folder = "processed_pages"
os.makedirs(output_folder, exist_ok=True)

def remove_gray_watermark(image):
    """Remove marcas d'água substituindo por branco puro, sem borrar"""
    # Converter para escala de cinza
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Criar uma máscara que detecta tons de cinza (entre preto e branco puros)
    lower_gray = 180  # Ajuste este valor se necessário
    upper_gray = 250  # Ajuste este valor se necessário
    mask = cv2.inRange(gray, lower_gray, upper_gray)

    # Substituir a marca d'água por branco puro (255)
    image[mask > 0] = [255, 255, 255]

    return image

processed_images = []

# Processar todas as páginas
for i, image in enumerate(images):
    # Converter a imagem para um formato compatível com OpenCV
    img_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

    # Remover a marca d'água substituindo por branco
    cleaned_img = remove_gray_watermark(img_cv)

    # Converter de volta para formato PIL e armazenar
    processed_images.append(Image.fromarray(cv2.cvtColor(cleaned_img, cv2.COLOR_BGR2RGB)))

# Criar um novo PDF sem marcas d'água diretamente com Pillow
output_pdf = "/content/PDF_sem_marca.pdf"
processed_images[0].save(output_pdf, save_all=True, append_images=processed_images[1:])

print(f"Processo concluído! O PDF sem marca d'água foi salvo como '{output_pdf}'.")
