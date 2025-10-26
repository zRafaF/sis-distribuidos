# Sistema de Gerenciamento de Filmes (API REST)

Este projeto é um servidor de API REST desenvolvido como trabalho acadêmico. O servidor gerencia um banco de dados de filmes e diretores, expondo endpoints para operações CRUD (Create, Read, Update, Delete).

## Autores

* Rafael Farias Meneses / 2263831
* Fábio Bays de Araujo / 2370441

## Funcionalidades Principais

* CRUD completo para Diretores.
* CRUD completo para Filmes.
* Relacionamento 1-N entre Diretores e Filmes.
* Filtros de busca para diretores (por `name` e `age`).
* Paginação em todos os endpoints de listagem (`page` e `size`).
* Validação de dados de entrada robusta usando Pydantic.

## Tecnologias Utilizadas

* [**Python 3.10+**](https://www.python.org/): Linguagem de programação base.
* [**FastAPI**](https://fastapi.tiangolo.com/): Framework web de alta performance para a construção da API.
* [**Peewee**](http://docs.peewee-orm.com/): Um ORM (Object-Relational Mapper) simples e leve para interagir com o banco de dados.
* [**SQLite**](https://www.sqlite.org/index.html): Banco de dados relacional embarcado (arquivo `database1.db`).

## Instalação e Execução

### 1. Pré-requisitos

* Python 3.10 ou superior
* `pip` (gerenciador de pacotes do Python)
* `make` para usar o comando de atalho.

### 2. Instalação

1.  Clone o repositório:
    ```bash
    git clone https://github.com/zRafaF/sis-distribuidos/ -b webservice
    cd sis-distribuidos
    ```

2.  (Recomendado) Crie e ative um ambiente virtual:
    ```bash
    python -m venv venv
    # Linux/macOS
    source venv/bin/activate
    # Windows
    # venv\Scripts\activate
    ```

3.  Instale as dependências:
    ```bash
    pip install -r requirements.txt
    ```

### 3. Execução

O servidor irá inicializar o banco de dados `database1.db` (se não existir) e começará a escutar em `http://127.0.0.1:8000`.

Use o comando `make` para iniciar:

```bash
make server
```

## Documentação e Endpoints da API

### Acesso à Documentação Interativa

Após iniciar o servidor, você pode acessar a documentação interativa (Swagger UI) e a documentação alternativa (ReDoc) geradas automaticamente:

  * **Swagger UI**: `http://127.0.0.1:8000/docs`
  * **ReDoc**: `http://127.0.0.1:8000/redoc`

Você pode testar todos os endpoints diretamente através destas interfaces.

-----

### Endpoints de Diretores

  * `GET /directors`: Lista todos os diretores.
      * Parâmetros de consulta opcionais: `name` (string), `age` (int), `page` (int), `size` (int).
  * `GET /directors/{id}`: Obtém um diretor específico pelo ID.
  * `POST /directors`: Cria um novo diretor.
  * `PUT /directors/{id}`: Atualiza um diretor existente.
  * `DELETE /directors/{id}`: Deleta um diretor.

### Endpoints de Filmes

  * `GET /movies`: Lista todos os filmes.
      * Parâmetros de consulta opcionais: `page` (int), `size` (int).
  * `POST /movies`: Cria um novo filme.
  * `GET /movies/{id}`: Obtém um filme específico pelo ID.
  * `PUT /movies/{id}`: Atualiza um filme existente.
  * `DELETE /movies/{id}`: Deleta um filme.

> **Paginação:** As listagens (`GET /directors` e `GET /movies`) permitem paginação. Por padrão, `page=1` e `size=10`.

## Exemplos de Uso (cURL)

### Criar um novo diretor

```bash
curl -X 'POST' \
  '[http://127.0.0.1:8000/directors](http://127.0.0.1:8000/directors)' \
  -H 'Content-Type: application/json' \
  -d '{
    "name": "Christopher Nolan",
    "age": 53
  }'
```

### Criar um novo filme

(Assumindo que o diretor com `id=1` já existe)

```bash
curl -X 'POST' \
  '[http://127.0.0.1:8000/movies](http://127.0.0.1:8000/movies)' \
  -H 'Content-Type: application/json' \
  -d '{
    "title": "Inception",
    "director_id": 1,
    "rating": 8.8,
    "duration_min": 148,
    "genre": "Sci-Fi"
  }'
```

### Listar todos os filmes (Página 1, 5 por página)

```bash
curl -X 'GET' '[http://127.0.0.1:8000/movies?page=1&size=5](http://127.0.0.1:8000/movies?page=1&size=5)'
```

### Obter diretor com ID 1

```bash
curl -X 'GET' '[http://127.0.0.1:8000/directors/1](http://127.0.0.1:8000/directors/1)'
```

-----

## Detalhes Técnicos

### Estrutura do Banco de Dados

O sistema utiliza **SQLite** com a ORM **Peewee**. A função `initialize_db()` (em `server/db_core.py`) cria as tabelas automaticamente na inicialização do servidor.

#### Tabela: `Directors`

Armazena os dados dos diretores.

| Coluna | Tipo de Dado | Descrição |
| :--- | :--- | :--- |
| `id` | `INTEGER` | Chave Primária, autoincremento. |
| `name` | `VARCHAR` | Nome do diretor. |
| `age` | `INTEGER` | Idade do diretor. |
| `created_at`| `DATETIME` | Data e hora da criação do registro. |
| `updated_at`| `DATETIME` | Data e hora da última atualização. |

#### Tabela: `Movies`

Armazena os dados dos filmes e referencia a tabela `Directors`.

| Coluna | Tipo de Dado | Descrição |
| :--- | :--- | :--- |
| `id` | `INTEGER` | Chave Primária, autoincremento. |
| `title` | `VARCHAR` | Título do filme. |
| `director_id`| `INTEGER` | Chave Estrangeira (`Directors.id`). |
| `rating` | `REAL` | Avaliação do filme (ex: 4.5). |
| `duration_min`| `INTEGER` | Duração do filme em minutos. |
| `genre` | `VARCHAR` | Gênero do filme (ex: Ação, Comédia). |
| `created_at`| `DATETIME` | Data e hora da criação do registro. |
| `updated_at`| `DATETIME` | Data e hora da última atualização. |

### Validação de Inputs

A validação dos dados de entrada (inputs) é feita de forma automática pelo **FastAPI**, que usa modelos **Pydantic** (`BaseModel`). Na prática, isso significa que definimos o "formato" esperado dos dados (como os campos `name` e `age` de um diretor) diretamente nos modelos Pydantic.

Dessa forma, o próprio FastAPI verifica os dados recebidos antes que eles cheguem à nossa lógica, garantindo:

1.  **Validação de Tipo:** Se o campo `age` espera um `int` e recebe uma `string` (ex: `"cinquenta"`), a API rejeita o dado.
2.  **Campos Obrigatórios:** Se um campo obrigatório (como `name`) não for enviado no JSON, a API acusa o erro.
3.  **Validação de Valores:** Também é possível definir validações mais específicas. Por exemplo, o campo `age` foi configurado para aceitar apenas inteiros positivos.

Se uma validação falhar, a API retorna automaticamente um erro `422 Unprocessable Entity`.

Por exemplo, ao tentar cadastrar um diretor com idade negativa, a API retorna uma resposta clara, indicando exatamente qual campo falhou e o motivo:

**Requisição Inválida (Exemplo):**

```json
{
  "name": "Mike",
  "age": -99
}
```

**Resposta de Erro (Status 422):**

```json
{
  "detail": [
    {
      "type": "greater_than",
      "loc": [
        "body",
        "age"
      ],
      "msg": "Input should be greater than 0",
      "input": -99,
      "ctx": {
        "gt": 0
      }
    }
  ]
}
```

```
```