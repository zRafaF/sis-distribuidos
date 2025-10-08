**Grupo:**
* Rafael Farias Meneses / 2263831
* Fábio Bays de Araujo / 2370441

# Sistema Distribuído de Gerenciamento de filmes com Pyro5 (RMI)

Este projeto implementa um sistema distribuído para gerenciamento de filmes e diretores utilizando a API de Remote Method Invocation (RMI) do Pyro5 em Python.


O servidor é responsável por processar as requisições, interagir com um banco de dados SQLite (usando a ORM Peewee) e retornar as respostas apropriadas. O cliente fornece uma interface de linha de comando para que o usuário possa realizar operações de CRUD (Criar, Ler, Atualizar, Deletar) no banco de dados.

## Descrição

O sistema é composto por um **servidor**, que expõe métodos remotos para manipulação e consulta de dados de filmes e diretores, e um **cliente**, que consome esses métodos remotamente via Pyro5. Toda a comunicação entre cliente e servidor é feita por meio de chamadas de métodos remotos, abstraindo detalhes de rede e serialização.

## Funcionalidades

  * **Gerenciamento de Filmes:**
      * Criar novos registros de filmes (título, diretor, avaliação, duração, gênero).
      * Ler um filme específico por ID ou listar todos os filmes.
      * Atualizar as informações de um filme existente.
      * Deletar um filme do banco de dados.
  * **Gerenciamento de Diretores:**
      * Criar novos diretores. Se um filme é adicionado com um diretor que não existe, ele é criado automaticamente.
      * Atualizar o nome de um diretor.
  * **Comunicação via Pyro5:** A API abstrai as complexidades de comunicação em redes.


## Estrutura do Projeto

```
atividadePyro5/
│
├── defines.py
├── makefile
├── Movie.py
├── requirements.txt
├── schema.py
│
├── client/
│   └── main.py
│
└── server/
    ├── main.py
    └── database/
        ├── __init__.py
        ├── core.py
        ├── director.py
        └── movie.py
```

- **server/main.py**: Inicializa o servidor Pyro5 e registra os objetos remotos.
- **server/database/**: Contém a lógica de negócio para filmes e diretores.
- **client/main.py**: Conecta-se ao servidor Pyro5 e invoca métodos remotos.

## Como Executar

### Execução

Você precisará de três terminais: um para o servidor e outro para o cliente e outro para o Name Server do Pyro5.

1. Primeiro navegue até a pasta com:

    ```bash
    cd atividadesPyro5
    ```

1. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
2. Inicie o Name Server do Pyro5:
    ```
    make pyro5
    ```
2. Inicie o servidor:
   ```
   make server
   ```

3. Execute o cliente:
   ```
   make client
   ```

## Estrutura do Banco de Dados

O sistema utiliza **SQLite** como banco de dados, com a interação sendo gerenciada pela ORM **Peewee**. A função `initialize_db()` no arquivo `server/database/core.py` é responsável por criar as tabelas no momento da inicialização do servidor, caso elas não existam.

A estrutura é composta por duas tabelas: `Directors` e `Movies`.

#### Tabela: `Directors`

Armazena os nomes dos diretores.

| Coluna | Tipo de Dado | Descrição |
| :--- | :--- | :--- |
| `id` | `INTEGER` | Chave Primária, autoincremento. |
| `name` | `VARCHAR` | Nome do diretor. |
| `created_at`| `DATETIME` | Data e hora da criação do registro. |
| `updated_at`| `DATETIME` | Data e hora da última atualização. |

#### Tabela: `Movies`

Armazena as informações dos filmes, com uma referência à tabela `Directors`.

| Coluna | Tipo de Dado | Descrição |
| :--- | :--- | :--- |
| `id` | `INTEGER` | Chave Primária, autoincremento. |
| `title` | `VARCHAR` | Título do filme. |
| `director_id`| `INTEGER` | Chave Estrangeira que referencia `Directors.id`. |
| `rating` | `REAL` | Avaliação do filme (ex: 5). |
| `duration_min`| `INTEGER` | Duração do filme em minutos. |
| `gender` | `VARCHAR` | Gênero do filme (ex: Ação, Comédia). |
| `created_at`| `DATETIME` | Data e hora da criação do registro. |
| `updated_at`| `DATETIME` | Data e hora da última atualização. |


## Tecnologias Utilizadas

- Python 3.10+
- [Pyro5](https://pyro5.readthedocs.io/en/latest/)
- [peewee](https://docs.peewee-orm.com/en/latest/)

## Observações

- Toda a comunicação é feita via RMI com Pyro5, sem uso de sockets manuais.
- O projeto é modular, facilitando manutenção e expansão das funcionalidades.