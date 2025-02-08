import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Caminho do ChromeDriver
driver_path = r"C:\chromedriver-win64\chromedriver.exe"
# Caminho do PDF a ser convertido
pdf_path = r"C:\Users\Douglas\Desktop\NOMARKWATER\PDF_BASE.pdf"
# Pasta para salvar o arquivo convertido
download_folder = r"C:\Users\Douglas\Desktop\NOMARKWATER"


def setup_browser(download_dir):
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")  # Inicia o navegador maximizado

    # Configurações de download
    prefs = {
        "download.default_directory": download_dir,  # Define a pasta de download
        "download.prompt_for_download": False,       # Não solicita confirmação de download
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    }
    chrome_options.add_experimental_option("prefs", prefs)

    service = Service(driver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def main():
    url = "https://www.ilovepdf.com/pt/pdf_para_word"
    driver = setup_browser(download_folder)
    wait = WebDriverWait(driver, 30)  # Timeout de 30 segundos
    try:
        driver.get(url)
        
        # Aguarda o botão de upload estar presente
        upload_button = wait.until(EC.presence_of_element_located((By.ID, "pickfiles")))
        upload_button.click()
        
        # Aguarda a janela de seleção de arquivos e envia o arquivo
        # Usaremos o Selenium para interagir com o sistema de arquivos
        # Selenium não pode interagir diretamente com diálogos do sistema operacional
        # Portanto, precisamos usar uma solução alternativa, como enviar o caminho do arquivo via clipboard
        # ou usar uma biblioteca como pywinauto para interagir com a janela

        # Alternativa 1: Usar input de arquivo, se disponível
        # Verifique se existe um input de tipo file

        try:
            file_input = driver.find_element(By.XPATH, "//input[@type='file']")
            file_input.send_keys(pdf_path)
            print("Arquivo enviado via input de arquivo.")
        except Exception as e:
            print("Não foi possível enviar o arquivo via input de arquivo:", e)
            # Se não for possível, retornar ao método anterior usando PyAutoGUI ou outra abordagem

            # Opcional: Reverter para o uso do PyAutoGUI
            raise NotImplementedError("Método de envio de arquivo via Selenium não implementado.")
        
        # Aguarda o upload completar
        # Dependendo do site, pode haver indicadores de progresso
        time.sleep(5)  # Ajuste conforme necessário

        # Clica no botão de converter
        converter_button = wait.until(EC.element_to_be_clickable((By.ID, "processTask")))
        converter_button.click()

        # Aguarda a conversão
        # Pode ser necessário aguardar até que o botão de download esteja clicável
        baixar_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@id='pickfiles']")))  # Ajuste o seletor conforme necessário
        # Alternativamente, você pode aguardar até que o download comece

        print("Conversão concluída. O arquivo deve estar sendo baixado.")

        # Aguarde o download finalizar
        # Isso pode ser feito verificando a existência do arquivo na pasta de download
        # Por exemplo:
        download_file = os.path.join(download_folder, "PRIMEASSIST_MOD_2.docx")
        timeout = 60  # Tempo máximo de espera em segundos
        start_time = time.time()
        while not os.path.exists(download_file):
            if time.time() - start_time > timeout:
                print("Tempo esgotado aguardando o download.")
                break
            time.sleep(1)
        
        if os.path.exists(download_file):
            print(f"Arquivo baixado com sucesso: {download_file}")
        else:
            print("Falha ao baixar o arquivo.")

    except Exception as e:
        print(f"Ocorreu um erro: {e}")
    finally:
        driver.quit()
        print("Processo finalizado.")

if __name__ == "__main__":
    main()