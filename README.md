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
- Recomenda-se usar a imagem oficial do Playwright (já inclui navegadores e dependências) quando desejar suporte completo ao Chromium sem precisar instalar dependências do sistema.
- Em containers, prefira rodar em *headless* (`headless=True`) para evitar a necessidade de interface gráfica.
- Monte volumes para `downloads/` e `logs/` para persistência dos arquivos.

Sobre o `Dockerfile` presente no repositório
- O `Dockerfile` atual é multi-stage e utiliza `ghcr.io/astral-sh/uv:...` como *builder*.
- Fluxo principal:
  1. **Builder**: instala Python via `uv` (`uv python install 3.14.2`) e usa `uv sync` (com `uv.lock`/`pyproject.toml`) para preparar as dependências.
  2. **Development**: parte da imagem `debian:trixie-slim`, copia `/python` e `/app` do *builder*, configura `PATH` para `/app/.venv/bin` e roda como usuário não-root (`uid 1000`).
- O `Dockerfile` **não foi alterado** no build — ele permanece configurado para executar `uvicorn` (parece um resquício de outro projeto). Para executar a automação (`main.py`) **sem mudar o Dockerfile**, sobrescreva o comando no `docker run` ou no `docker-compose` (ex.: `docker run ... rpa-challenge:latest python main.py`).
- Se desejar que eu adapte o build para instalar os navegadores do Playwright e executar `main.py` por padrão, posso aplicar essa alteração mediante sua confirmação.

Exemplos e ajustes rápidos

- Build:
```powershell
docker build -t rpa-challenge:latest .
```

- Run (sobrescrevendo o CMD para rodar a automação `main.py` e persistindo downloads/logs):
```powershell
docker run --rm -v ${PWD}:/app -v ${PWD}/downloads:/app/downloads -v ${PWD}/logs:/app/logs --user 1000 rpa-challenge:latest python main.py
```

- Se preferir ajustar o `Dockerfile` para instalar os navegadores do Playwright dentro da imagem (recomendado para execução em container), adicione em uma das etapas:
```dockerfile
RUN python -m playwright install --with-deps
```

- Exemplo de `docker-compose.yml` (com override de comando):
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
    command: ["python", "main.py"]
```

Uso de `docker-compose.override.yml` (pronto para executar `main.py`)
- Foi adicionado um arquivo `docker-compose.override.yml` que sobrescreve o comando do serviço para executar `python main.py`, monta os volumes (`downloads/` e `logs/`), define `HEADLESS=1` e roda com o usuário `1000`.

Exemplo (`docker-compose.override.yml`):
```yaml
version: '3.8'
services:
  rpa:
    command: ["python", "main.py"]
    volumes:
      - ./downloads:/app/downloads
      - ./logs:/app/logs
    environment:
      - PYTHONUNBUFFERED=1
      - HEADLESS=1
    user: "1000"
    shm_size: '1gb'
```

Como usar (exemplos):
```powershell
# build (uma vez):
docker compose build

# subir com o override (sobrescreve o comando definido no Dockerfile para rodar main.py):
docker compose up

# ou, sem compose v2:
docker-compose up --build
```

Dicas finais:
- O `Dockerfile` do repositório não foi alterado (mantém `uvicorn` como CMD). O `docker-compose.override.yml` é uma forma não intrusiva de executar `main.py` em containers sem alterar o build.
- Se quiser, posso também ajustar `main.py` para respeitar a variável `HEADLESS` (recomendado) — quer que eu faça isso?

## Observações e boas práticas
- Garanta que a versão do Python seja compatível (>=3.13).
- Em ambientes CI, prefira rodar em headless e use `python -m playwright install --with-deps` quando necessário.
- Caso o site altere os seletores, atualize os seletores CSS em `main.py` e em `pages/*`.

## Licença

Porjeto de estudo, com um dos desafios mais conhecidos da internet

## Contato

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Perfil-blue?logo=linkedin)](https://www.linkedin.com/in/vitor-zavan-831907297/)

