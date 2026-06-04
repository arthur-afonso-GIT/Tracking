# Tracking
Este repositório reúne um conjunto de aplicações práticas focadas em visão computacional e rastreamento em tempo real. Desenvolvido como parte dos meus estudos de lógica de programação e inteligência artificial, o projeto utiliza processamento de imagem para interagir com o usuário através de reconhecimento facial, mapeamento anatômico de mãos e detecção de postura corpórea.

O objetivo principal deste espaço é servir como portfólio, demonstrando a aplicação de matrizes, geometria coordenada e algoritmos estruturados no desenvolvimento de interfaces inteligentes via webcam.

O repositório é composto por três scripts principais, cada um explorando uma vertente diferente das ferramentas de rastreamento:

### 1. tracking.py
O script principal de rastreamento do ecossistema. Ele combina a detecção de pose corporal (Pose Tracking) e o mapeamento das mãos (Hands Tracking) para criar um tradutor de comandos físicos em tempo real.
* Monitora a posição dos braços em relação aos ombros para identificar comandos de postura (como braços levantados).
* Analisa a anatomia dos dedos, identificando se estão abertos ou fechados através de cálculos no plano cartesiano da imagem.
* Converte gestos específicos (como mão aberta, mão fechada ou sinais direcionais) em strings de comando configuradas em um dicionário estruturado.

### 2. tracking_rosto.py
Aplicação dedicada ao rastreamento e delimitação facial (Face Mesh / Face Detection).
* Captura o frame da webcam e isola a região do rosto humano.
* Cria uma malha de pontos de referência sobre a face para monitorar movimentos e expressões em tempo real.
* Desenha delimitadores visuais na tela para acompanhar o deslocamento do usuário de forma fluida.

### 3. desenho.py
Um módulo de interação artística e interativa baseado no rastreamento do dedo indicador.
* Utiliza a biblioteca de visão computacional para isolar os pontos da mão principal.
* Detecta quando apenas o dedo indicador está levantado, transformando as coordenadas do pixel da ponta do dedo em um "pincel virtual".
* Permite que o usuário desenhe diretamente na tela sobrepondo linhas coloridas ao vídeo da webcam, além de contar com lógica de limpeza total da tela ao abrir a mão completa.

## Como Executar os Projetos

Para rodar qualquer um dos scripts localmente, certifique-se de ter o Python instalado (recomenda-se versões 3.11 ou 3.12) e siga as etapas no terminal:

1. Clone este repositório:
   git clone https://github.com/seu-usuario/nome-do-repositorio.git
   cd nome-do-repositorio

2. Crie e ative um ambiente virtual isolado para não conflitar com pacotes globais do seu sistema:
   python -m venv .venv
   
   No Windows (PowerShell):
   .venv/Scripts/Activate.ps1

3. Instale as dependências necessárias utilizando o arquivo de requerimentos:
   pip install -r requirements.txt

4. Execute o script desejado alterando o nome do arquivo:
   python tracking.py