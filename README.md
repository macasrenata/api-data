# User Data API

## Descrição

Esta aplicação é uma API REST construída com **FastAPI**, que recebe dados de usuários em formatos **CSV** e **JSON**, os transforma de acordo com regras de negócios específicas e os serve para o consumo, incluindo funcionalidades de paginação e classificação de usuários com base na localização.

### Regras de Negócio

- Classificação dos usuários em três categorias: **ESPECIAL**, **NORMAL**, ou **TRABALHOSO**.
- Transformação de dados de telefone para o formato E.164.
- Inclusão do campo de nacionalidade com valor padrão "BR".
- Transformação de gênero de "male"/"female" para "M"/"F".
- Reestruturação de dados e remoção de campos desnecessários.

### Tecnologias Utilizadas

- **Python 3.11**
- **FastAPI** - Framework para construção da API.
- **Pytest** - Ferramenta de testes unitários.
- **Docker** - Contêiner para empacotamento da aplicação.

### Clone o repositório

```bash
git clone git@github.com:macasrenata/api-data.git
cd api-data
```

### Instale o Poetry

```bash
curl -sSL https://install.python-poetry.org | python3 -
export PATH="$HOME/.local/bin:$PATH"
```

### Instale as dependências

```bash
poetry install
```

### Rodar a aplicação localmente: Para iniciar o servidor com FastAPI

```bash
poetry run uvicorn app.main:app --reload
```

### Executar Testes: Para rodar os testes unitários com Pytest

```bash
poetry run pytest
```

or

```bash
pytest
```

## Utilizando Docker

Se preferir utilizar Docker, ainda pode seguir o processo padrão com o Dockerfile:

### Build da Imagem

```bash
docker build -t user-api .
```

### Rodando o contêiner

```bash
docker run -p 8080:8080 user-api
```

## Acessando a documentação da API

A documentação interativa estará disponível em:

```bash
http://localhost:8080/docs
```
