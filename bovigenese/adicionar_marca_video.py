import cv2
import numpy as np
from PIL import Image
import os

class AdicionarMarcaVideo:
    def __init__(self, marca_dagua_path, opacidade=0.3):
        """
        Inicializa o objeto para adicionar marca d'água em vídeos
        :param marca_dagua_path: Caminho para a imagem da marca d'água
        :param opacidade: Valor de 0 a 1 para a opacidade da marca
        """
        # Carregar a marca d'água
        self.marca_dagua = cv2.cvtColor(
            np.array(Image.open(marca_dagua_path).convert('RGBA')), 
            cv2.COLOR_RGBA2BGRA
        )
        self.opacidade = opacidade

    def redimensionar_marca(self, frame_size):
        """
        Redimensiona a marca d'água mantendo a proporção
        :param frame_size: (largura, altura) do frame do vídeo
        """
        # Calcular tamanho desejado (30% do frame)
        tamanho_desejado = (
            int(frame_size[0] * 0.3),
            int(frame_size[1] * 0.3)
        )
        
        # Calcular ratio para manter proporção
        ratio = min(
            tamanho_desejado[0] / self.marca_dagua.shape[1],
            tamanho_desejado[1] / self.marca_dagua.shape[0]
        )
        
        novo_tamanho = (
            int(self.marca_dagua.shape[1] * ratio),
            int(self.marca_dagua.shape[0] * ratio)
        )
        
        return cv2.resize(self.marca_dagua, novo_tamanho, interpolation=cv2.INTER_LANCZOS4)

    def adicionar_marca_frame(self, frame, marca_redimensionada):
        """
        Adiciona marca d'água em um frame do vídeo
        """
        # Criar uma cópia do frame
        frame_rgba = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)
        
        # Calcular posição para centralizar
        x = (frame.shape[1] - marca_redimensionada.shape[1]) // 2
        y = (frame.shape[0] - marca_redimensionada.shape[0]) // 2
        
        # Criar máscara da marca d'água
        marca_alpha = marca_redimensionada[:, :, 3] / 255.0 * self.opacidade
        
        # Região onde a marca será aplicada
        roi = frame_rgba[y:y+marca_redimensionada.shape[0], 
                        x:x+marca_redimensionada.shape[1]]
        
        # Aplicar marca d'água com transparência
        for c in range(3):  # BGR channels
            roi[:, :, c] = roi[:, :, c] * (1 - marca_alpha) + \
                          marca_redimensionada[:, :, c] * marca_alpha
        
        return cv2.cvtColor(frame_rgba, cv2.COLOR_BGRA2BGR)

    def processar_video(self, video_path, output_path):
        """
        Adiciona marca d'água em todo o vídeo
        :param video_path: Caminho do vídeo de entrada
        :param output_path: Caminho para salvar o vídeo processado
        """
        # Abrir o vídeo
        video = cv2.VideoCapture(video_path)
        if not video.isOpened():
            raise ValueError("Não foi possível abrir o vídeo")
        
        # Obter propriedades do vídeo
        largura = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
        altura = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = video.get(cv2.CAP_PROP_FPS)
        total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
        
        # Redimensionar marca d'água uma única vez
        marca_redimensionada = self.redimensionar_marca((largura, altura))
        
        # Configurar o writer do vídeo
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        writer = cv2.VideoWriter(
            output_path, fourcc, fps, (largura, altura)
        )
        
        # Processar cada frame
        frames_processados = 0
        while True:
            ret, frame = video.read()
            if not ret:
                break
                
            # Adicionar marca d'água no frame
            frame_com_marca = self.adicionar_marca_frame(frame, marca_redimensionada)
            writer.write(frame_com_marca)
            
            # Atualizar progresso
            frames_processados += 1
            progresso = (frames_processados / total_frames) * 100
            print(f"Progresso: {progresso:.1f}%", end='\r')
        
        print("\nProcessamento concluído!")
        
        # Liberar recursos
        video.release()
        writer.release()

def main():
    # Criar pasta de saída se não existir
    output_dir = "videos_com_marca"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Instanciar o processador de vídeo
    processador = AdicionarMarcaVideo(
        marca_dagua_path="marca.png",
        opacidade=0.3
    )
    
    # Processar todos os vídeos MP4 na pasta
    for arquivo in os.listdir("."):
        if arquivo.lower().endswith(".mp4"):
            print(f"\nProcessando: {arquivo}")
            nome_base = os.path.splitext(arquivo)[0]
            output_path = os.path.join(output_dir, f"{nome_base}_marca.mp4")
            processador.processar_video(arquivo, output_path)

if __name__ == "__main__":
    main() 