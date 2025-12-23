# RPA Challenge 2.0

Automação em Python que executa o desafio do site RPA Challenge (https://rpachallenge.com). O script usa Playwright para navegar no site, baixar um arquivo Excel com dados e preencher um formulário automaticamente com as informações do arquivo.

Este repositório contém uma implementação simples e direta pensada para ser fácil de entender e estender.

## Recursos
- Inicia o desafio no site e aciona o download do arquivo com os dados.
- Lê o arquivo Excel usando pandas / openpyxl.
- Preenche o formulário do site automaticamente via Playwright.
- Logging com rotação de arquivos (RotatingFileHandler).

## Requisitos
- Python 3.13 ou superior
- Dependências listadas em `pyproject.toml`: playwright, pandas, openpyxl, chromium (driver)

Recomenda-se criar e usar um ambiente virtual para instalar dependências.

## Instalação (Windows / PowerShell)

1. Criar ambiente virtual (opcional, mas recomendado):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Atualizar pip e instalar dependências:

```powershell
python -m pip install --upgrade pip
python -m pip install -e .
```

Observação: o projeto usa `pyproject.toml`. O comando `pip install -e .` instalará as dependências listadas nesse arquivo.

3. Instalar os navegadores do Playwright (necessário na primeira execução):

```powershell
python -m playwright install
```

Se desejar apenas o Chromium, rode:

```powershell
python -m playwright install chromium
```

## Como executar

O ponto de entrada é o arquivo `main.py`. Execute-o com o ambiente virtual ativado:

```powershell
python main.py
```

Durante a execução o navegador será aberto (a configuração atual utiliza headless=False). A automação irá:

1. Abrir a página do desafio
2. Clicar em Start
3. Fazer o download do arquivo Excel para a pasta `downloads/`
4. Ler o arquivo com pandas
5. Preencher o formulário linha a linha
6. Capturar a mensagem final exibida pelo site

## Estrutura do projeto

- `main.py` - script principal que orquestra a automação.
- `pyproject.toml` - metadados do projeto e dependências.
- `config/logging_config.py` - configuração de logging com rotação de arquivo em `logs/app.log`.
- `pages/` - módulos com responsabilidades separadas:
	- `start_challenge.py` - navegação inicial e clique no botão Start.
	- `download_page.py` - trata do download do arquivo Excel.
	- `read_file.py` - lê o Excel com pandas.
	- `form_filer.py` - preenche o formulário e captura resultado final.
- `downloads/` - pasta onde o Excel é salvo (criada automaticamente).
- `logs/` - pasta onde os logs são gravados (criada automaticamente).

## Configurações úteis
- Para alterar a URL, seletores ou o diretório de download, veja e edite as variáveis no início de `main.py`.
- Para ativar headless mode (execução sem abrir janela do navegador), altere `browser = p.chromium.launch(headless=False)` para `headless=True` em `main.py`.

## Uso com Docker 🔧
Abaixo estão orientações e exemplos para empacotar e rodar a automação em um container Docker.

Observações rápidas:
- Recomenda-se usar a imagem oficial do Playwright (já inclui navegadores e dependências).
- Em containers, prefira rodar em *headless* (`headless=True`) para evitar a necessidade de interface gráfica.
- Monte volumes para `downloads/` e `logs/` para persistência dos arquivos.

Exemplo 1 — usando a imagem oficial do Playwright (recomendado):

```dockerfile
# Dockerfile (recomendado)
FROM mcr.microsoft.com/playwright/python:latest

WORKDIR /app

COPY pyproject.toml ./
COPY . .

RUN pip install --no-cache-dir -e .
# A imagem oficial já inclui os navegadores; se necessário:
# RUN python -m playwright install

ENV PYTHONUNBUFFERED=1

VOLUME ["/app/downloads", "/app/logs"]

CMD ["python", "main.py"]
```

Exemplo 2 — usando uma imagem base Python (instalando dependências do sistema):

```dockerfile
# Dockerfile alternativo (python:3.13-slim)
FROM python:3.13-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    libnss3 libatk1.0-0 libatk-bridge2.0-0 libcups2 libxkbcommon0 libxcomposite1 libxrandr2 libgbm1 libgtk-3-0 libpangocairo-1.0-0 libx11-6 libxss1 libasound2 \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY pyproject.toml ./
COPY . .

RUN pip install --upgrade pip \
 && pip install -e . \
 && python -m playwright install --with-deps

ENV PYTHONUNBUFFERED=1
VOLUME ["/app/downloads", "/app/logs"]

CMD ["python", "main.py"]
```

Exemplo `docker-compose.yml`:

```yaml
version: '3.8'
services:
  rpa:
    build: .
    image: rpa-challenge:latest
    volumes:
      - ./downloads:/app/downloads
      - ./logs:/app/logs
    environment:
      - PYTHONUNBUFFERED=1
    shm_size: '1gb'
    # command: ["python", "main.py"] # opcional
```

Comandos úteis:

```powershell
# build
docker build -t rpa-challenge:latest .

# run (persistindo downloads e logs)
docker run --rm -v ${PWD}:/app -v ${PWD}/downloads:/app/downloads -v ${PWD}/logs:/app/logs rpa-challenge:latest

# ou
docker-compose up --build
```

Dicas:
- Se optar por `python:3.13-slim`, use `python -m playwright install --with-deps` no Dockerfile para instalar dependências do navegador.
- Pode ser necessário aumentar `--shm-size` (ex.: `--shm-size=1g`) ao executar com `docker run` para evitar problemas com o Chromium.

## Observações e boas práticas
- Garanta que a versão do Python seja compatível (>=3.13).
- Em ambientes CI, prefira rodar em headless e use `python -m playwright install --with-deps` quando necessário.
- Caso o site altere os seletores, atualize os seletores CSS em `main.py` e em `pages/*`.

## Licença

Porjeto de estudo, com um dos desafios mais conhecidos da internet

## Contato

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Perfil-blue?logo=linkedin)](https://www.linkedin.com/in/vitor-zavan-831907297/)

