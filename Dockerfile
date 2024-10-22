# Use a imagem base oficial do Python
FROM python:3.11-slim

# Definir o diretório de trabalho dentro do contêiner
WORKDIR /app

# Instalar o Poetry
RUN apt-get update && apt-get install -y curl && \
    curl -sSL https://install.python-poetry.org | python3 - && \
    apt-get remove -y curl && \
    rm -rf /var/lib/apt/lists/*

# Adicionar o Poetry ao PATH
ENV PATH="/root/.local/bin:$PATH"

# Copiar apenas o arquivo pyproject.toml e poetry.lock primeiro (para cache)
COPY pyproject.toml poetry.lock* /app/

# Instalar as dependências do projeto
RUN poetry config virtualenvs.create false \
    && poetry install --no-dev --no-interaction --no-ansi

# Copiar o restante do código da aplicação
COPY . /app

# Comando para rodar o servidor FastAPI com Uvicorn
CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
