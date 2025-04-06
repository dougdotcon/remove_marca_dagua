# NOMARKWATER

Ferramenta para remoção e substituição de marcas d'água em arquivos PDF e DOCX, com interface gráfica e automação via navegador.

---

## Funcionalidades

- **Remover marcas d'água cinzas** de arquivos PDF convertendo páginas em imagens e processando-as.
- **Substituir imagens** em documentos DOCX por uma nova imagem.
- **Automação com navegador** para converter PDFs usando serviços online.
- **Interface gráfica (GUI)** simples para facilitar o uso.

---

## Pré-requisitos

- **Python 3.7+**
- **Google Chrome** instalado
- **ChromeDriver** compatível com sua versão do Chrome:  
  [https://googlechromelabs.github.io/chrome-for-testing/](https://googlechromelabs.github.io/chrome-for-testing/)
- Bibliotecas Python:
  - `tkinter`
  - `selenium`
  - `Pillow`
  - `python-docx`
  - Outras dependências listadas no seu ambiente

---

## Instalação

1. Clone este repositório:
   ```bash
   git clone https://seurepositorio.git
   cd NOMARKWATER
   ```

2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
   *(Crie um arquivo `requirements.txt` com as dependências caso ainda não exista.)*

3. Baixe o **ChromeDriver** compatível e extraia para uma pasta no seu computador.

---

## Configuração

Edite os arquivos para ajustar os caminhos conforme seu ambiente:

### `app.py`
```python
# Caminho do ChromeDriver
driver_path = r"C:\\caminho\\para\\chromedriver.exe"

# Caminho do PDF a ser convertido
pdf_path = r"C:\\caminho\\para\\seuarquivo.pdf"

# Pasta para salvar o arquivo convertido
download_folder = r"C:\\caminho\\para\\pasta\\destino"
```

### `delete.py`
```python
# Caminho do arquivo DOCX original
doc_path = r"C:\\caminho\\para\\seuarquivo.docx"

# Caminho da nova imagem para substituir
nova_imagem_path = r"C:\\caminho\\para\\nova_imagem.png"

# Caminho do arquivo DOCX de saída
output_path = r"C:\\caminho\\para\\saida.docx"
```

---

## Como usar

### Interface Gráfica (GUI)

Execute:
```bash
python app.py
```
- Selecione o PDF desejado.
- O programa irá processar e remover as marcas d'água automaticamente.

### Script de conversão automatizada

Execute:
```bash
python converter.py
```
- O script abrirá o navegador, fará o upload do PDF e baixará o arquivo convertido.

### Script para substituir imagens em DOCX

Execute:
```bash
python delete.py
```
- O script substituirá todas as imagens do arquivo DOCX pela nova imagem especificada.

---

## Estrutura do Projeto

- `app.py` — Interface gráfica para remoção de marcas d'água em PDFs.
- `converter.py` — Automação via navegador para converter PDFs.
- `delete.py` — Substituição de imagens em arquivos DOCX.
- `assets/` — Imagens e outros recursos.
- `dist/` — Binários gerados (ex: `.exe`).
- `build/` — Arquivos de build.
- `PDF_BASE.pdf` — Exemplo de PDF original.
- `PDF_BASE_NOMARKWATER.docx` — Exemplo de saída após substituição.

---

## Licença

Este projeto está licenciado sob os termos da licença MIT.

---

## Créditos

Desenvolvido por Douglas.

---

## Observações

- **Nunca compartilhe seus arquivos com dados sensíveis.**
- **Sempre faça backup dos arquivos originais antes de processá-los.**
