# Adicionar Marca D'água

Este script permite adicionar uma imagem como marca d'água em diferentes tipos de arquivos:
- PDF
- Documentos Word (.doc, .docx)
- Planilhas Excel (.xlsx)
- Imagens (.jpg, .jpeg, .png)
- Vídeos (.mp4)

## Requisitos

```bash
pip install -r requirements.txt
```

Para PDFs, você também precisa instalar o Poppler:

Windows:
- Baixe o binário do Poppler para Windows
- Adicione o caminho do Poppler às variáveis de ambiente

Linux:
```bash
sudo apt-get install poppler-utils
```

## Integração com Laravel e React

### 1. Configuração no Laravel

1. Crie uma pasta `python_scripts` na raiz do seu projeto Laravel:
```bash
mkdir python_scripts
```

2. Copie os arquivos Python e requirements.txt para esta pasta:
- `adicionar_marca.py`
- `adicionar_marca_video.py`
- `requirements.txt`

3. Instale as dependências Python no servidor:
```bash
cd python_scripts
pip install -r requirements.txt
```

4. Crie um Controller para gerenciar os downloads:

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Symfony\Component\Process\Process;
use Illuminate\Support\Facades\Storage;

class DocumentoController extends Controller
{
    protected $tiposPermitidos = [
        'pdf', 'doc', 'docx', 'xlsx', 'jpg', 'jpeg', 'png', 'mp4'
    ];

    public function download(Request $request, $id)
    {
        try {
            // Buscar documento no banco de dados
            $documento = Documento::findOrFail($id);
            
            // Verificar permissões do usuário
            if (!auth()->user()->can('download', $documento)) {
                throw new \Exception('Sem permissão para download');
            }
            
            $arquivo_original = Storage::path($documento->caminho);
            
            // Determinar tipo de arquivo
            $extensao = strtolower(pathinfo($arquivo_original, PATHINFO_EXTENSION));
            
            // Verificar se o tipo de arquivo é permitido
            if (!in_array($extensao, $this->tiposPermitidos)) {
                throw new \Exception('Tipo de arquivo não suportado');
            }
            
            // Criar pasta temporária se não existir
            $temp_dir = storage_path('app/temp');
            if (!file_exists($temp_dir)) {
                mkdir($temp_dir, 0755, true);
            }
            
            // Criar nome para arquivo temporário
            $temp_output = storage_path('app/temp/' . uniqid() . '_marca.' . $extensao);
            
            // Selecionar script Python apropriado
            if ($extensao === 'mp4') {
                $script = base_path('python_scripts/adicionar_marca_video.py');
            } else {
                $script = base_path('python_scripts/adicionar_marca.py');
            }
            
            // Executar script Python
            $process = new Process([
                'python',
                $script,
                $arquivo_original,
                $temp_output,
                base_path('python_scripts/marca.png')
            ]);
            
            // Aumentar tempo limite para arquivos grandes
            $process->setTimeout(3600); // 1 hora
            
            // Executar processo
            $process->run();
            
            // Verificar se o processo foi bem sucedido
            if (!$process->isSuccessful()) {
                \Log::error('Erro ao processar arquivo: ' . $process->getErrorOutput());
                throw new \Exception('Erro ao processar arquivo');
            }
            
            // Registrar o download
            $this->registrarDownload($documento);
            
            // Fazer download do arquivo processado
            return response()->download($temp_output, $documento->nome)
                ->deleteFileAfterSend(true);
                
        } catch (\Exception $e) {
            // Limpar arquivos temporários em caso de erro
            if (isset($temp_output) && file_exists($temp_output)) {
                unlink($temp_output);
            }
            
            return response()->json([
                'error' => $e->getMessage()
            ], 500);
        }
    }
    
    protected function registrarDownload($documento)
    {
        // Registrar o download no banco de dados
        Download::create([
            'documento_id' => $documento->id,
            'user_id' => auth()->id(),
            'ip' => request()->ip(),
            'data' => now()
        ]);
    }
}
```

5. Adicione a rota no `routes/web.php`:
```php
Route::get('/download/{id}', [DocumentoController::class, 'download']);
```

### 2. Modificações nos Scripts Python

Modifique a função `main()` dos scripts Python para aceitar argumentos da linha de comando:

```python
def main():
    if len(sys.argv) != 4:
        print("Uso: python script.py arquivo_entrada arquivo_saida marca_dagua")
        sys.exit(1)
        
    arquivo_entrada = sys.argv[1]
    arquivo_saida = sys.argv[2]
    marca_dagua = sys.argv[3]
    
    processador = AdicionarMarcaDagua(
        marca_dagua_path=marca_dagua,
        opacidade=0.3
    )
    
    # Processar o arquivo
    if arquivo_entrada.lower().endswith(('.jpg', '.jpeg', '.png')):
        processador.adicionar_marca_imagem(arquivo_entrada, arquivo_saida)
    elif arquivo_entrada.lower().endswith('.pdf'):
        processador.adicionar_marca_pdf(arquivo_entrada, arquivo_saida)
    elif arquivo_entrada.lower().endswith(('.doc', '.docx')):
        processador.adicionar_marca_doc(arquivo_entrada, arquivo_saida)
    elif arquivo_entrada.lower().endswith('.xlsx'):
        processador.adicionar_marca_excel(arquivo_entrada, arquivo_saida)
```

### 3. Componente React

Crie um componente para o botão de download:

```jsx
import React from 'react';
import axios from 'axios';

const DownloadButton = ({ documentId, fileName }) => {
    const handleDownload = async () => {
        try {
            // Iniciar download com marca d'água
            const response = await axios.get(`/api/download/${documentId}`, {
                responseType: 'blob'
            });
            
            // Criar URL do blob e fazer download
            const url = window.URL.createObjectURL(new Blob([response.data]));
            const link = document.createElement('a');
            link.href = url;
            link.setAttribute('download', fileName);
            document.body.appendChild(link);
            link.click();
            link.remove();
            window.URL.revokeObjectURL(url);
        } catch (error) {
            console.error('Erro ao fazer download:', error);
            alert('Erro ao fazer download do arquivo');
        }
    };

    return (
        <button onClick={handleDownload} className="btn btn-primary">
            Download
        </button>
    );
};

export default DownloadButton;
```

### 4. Uso no Componente Principal

```jsx
import DownloadButton from './components/DownloadButton';

function DocumentoList({ documentos }) {
    return (
        <div>
            {documentos.map(doc => (
                <div key={doc.id} className="documento-item">
                    <h3>{doc.nome}</h3>
                    <DownloadButton 
                        documentId={doc.id} 
                        fileName={doc.nome} 
                    />
                </div>
            ))}
        </div>
    );
}
```

### 5. Considerações de Segurança

1. Certifique-se de validar permissões do usuário antes de permitir downloads
2. Limpe arquivos temporários regularmente
3. Valide tipos de arquivos permitidos
4. Use filas (Laravel Queue) para processar arquivos grandes
5. Configure limites de tamanho de arquivo

### 6. Otimizações Recomendadas

1. Implemente cache para arquivos processados frequentemente
2. Use Laravel Queue para processar arquivos em background
3. Implemente progress bar no frontend
4. Adicione sistema de retry em caso de falhas
5. Monitore uso de recursos do servidor

## Exemplo de Queue Job

```php
<?php

namespace App\Jobs;

use Illuminate\Bus\Queueable;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Foundation\Bus\Dispatchable;
use Illuminate\Queue\InteractsWithQueue;
use Illuminate\Queue\SerializesModels;

class ProcessarMarcaDagua implements ShouldQueue
{
    use Dispatchable, InteractsWithQueue, Queueable, SerializesModels;

    protected $documentoId;

    public function __construct($documentoId)
    {
        $this->documentoId = $documentoId;
    }

    public function handle()
    {
        // Lógica de processamento aqui
        // Notificar usuário quando concluir
    }
}
```

## Saída

Os arquivos processados serão salvos temporariamente e enviados para download com a marca d'água aplicada. 