#!/usr/bin/env python3
import os
import cv2
import numpy as np
from pdf2image import convert_from_path
from PIL import Image
import tkinter as tk
from tkinter import filedialog, messagebox
import sys

def remove_gray_watermark(image):
    """
    Remove marcas d'água cinzentas substituindo por branco puro.
    Converte a imagem para escala de cinza, cria uma máscara para tons de cinza
    e substitui as áreas detectadas por branco.
    """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    lower_gray = 180  # Valor mínimo para detecção de cinza (ajuste se necessário)
    upper_gray = 250  # Valor máximo para detecção de cinza (ajuste se necessário)
    mask = cv2.inRange(gray, lower_gray, upper_gray)
    image[mask > 0] = [255, 255, 255]
    return image

def process_pdf(pdf_path, output_pdf):
    """
    Converte um PDF em imagens com 300 DPI, processa cada página para remover marcas d'água e
    gera um novo PDF com as páginas processadas.
    """
    # Define o caminho do poppler se o sistema for Windows e se a pasta estiver incluída localmente
    poppler_path = None
    if os.name == 'nt':
        # Em um executável gerado pelo PyInstaller, use sys._MEIPASS para localizar arquivos adicionados
        base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
        poppler_path = os.path.join(base_path, "poppler", "bin")
    
    try:
        # Converter PDF para imagens (300 DPI para alta qualidade)
        if poppler_path:
            images = convert_from_path(pdf_path, dpi=300, poppler_path=poppler_path)
        else:
            images = convert_from_path(pdf_path, dpi=300)
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao converter PDF: {e}")
        return

    processed_images = []
    for i, image in enumerate(images):
        img_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        cleaned_img = remove_gray_watermark(img_cv)
        processed_images.append(Image.fromarray(cv2.cvtColor(cleaned_img, cv2.COLOR_BGR2RGB)))

    try:
        processed_images[0].save(output_pdf, save_all=True, append_images=processed_images[1:])
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao salvar o PDF: {e}")
        return

    messagebox.showinfo("Concluído", f"Processo concluído!\nO PDF sem marca d'água foi salvo como:\n{output_pdf}")

class PDFWatermarkRemoverApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Remover Marca d'Água de PDF")
        self.geometry("500x150")
        self.pdf_path = None

        self.btn_select = tk.Button(self, text="Selecionar PDF", command=self.select_pdf, width=20)
        self.btn_select.pack(pady=10)

        self.label_file = tk.Label(self, text="Nenhum arquivo selecionado")
        self.label_file.pack(pady=5)

        self.btn_process = tk.Button(self, text="Processar PDF", command=self.process_pdf_gui, width=20, state=tk.DISABLED)
        self.btn_process.pack(pady=10)

    def select_pdf(self):
        filetypes = [("PDF Files", "*.pdf")]
        selected_file = filedialog.askopenfilename(title="Selecione um arquivo PDF", filetypes=filetypes)
        if selected_file:
            self.pdf_path = selected_file
            self.label_file.config(text=f"Selecionado: {os.path.basename(self.pdf_path)}")
            self.btn_process.config(state=tk.NORMAL)

    def process_pdf_gui(self):
        if not self.pdf_path:
            messagebox.showwarning("Aviso", "Por favor, selecione um arquivo PDF primeiro.")
            return

        output_pdf = os.path.join(os.path.dirname(self.pdf_path), "PDF_sem_marca.pdf")
        os.makedirs("processed_pages", exist_ok=True)
        process_pdf(self.pdf_path, output_pdf)

if __name__ == "__main__":
    app = PDFWatermarkRemoverApp()
    app.mainloop()
