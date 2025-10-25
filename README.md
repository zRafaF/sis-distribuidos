**Grupo:**
* Rafael Farias Meneses / 2263831
* Fábio Bays de Araujo / 2370441

# Sistema de Gerenciamento de Filmes via Socwebserverkets

Este projeto implementa um sistema cliente-servidor para gerenciar um banco de dados de filmes e diretores. A comunicação entre o cliente e o servidor é realizada através de um protocolo de texto simples sobre TCP/IP.

O servidor é responsável por processar as requisições, interagir com um banco de dados SQLite (usando a ORM Peewee) e retornar as respostas apropriadas. O cliente fornece uma interface de linha de comando para que o usuário possa realizar operações de CRUD (Criar, Ler, Atualizar, Deletar) no banco de dados.

## Funcionalidades

  * **Gerenciamento de Filmes:**
      * Criar novos registros de filmes (título, diretor, avaliação, duração, gênero).
      * Ler um filme específico por ID ou listar todos os filmes.
      * Atualizar as informações de um filme existente.
      * Deletar um filme do banco de dados.
  * **Gerenciamento de Diretores:**
      * Criar novos diretores. Se um filme é adicionado com um diretor que não existe, ele é criado automaticamente.
      * Atualizar o nome de um diretor.
  * **Comunicação via Sockets:** Utiliza um protocolo customizado para troca de mensagens entre cliente e servidor de forma estruturada.

## Como Executar

### Pré-requisitos

  - Python 3.x
  - `pip` para instalar as dependências

### Instalação

Clone o repositório e instale as dependências necessárias:

```bash
# Instale as bibliotecas necessárias
pip install -r requirements.txt
```

### Execução

Você precisará de dois terminais: um para o servidor e outro para o cliente.


1.  **Inicie o Servidor:**
    O servidor irá inicializar o banco de dados `database1.db` (se não existir) e começará a escutar por conexões.

    ```bash
    make server
    ```

2.  **Inicie o Cliente:**
    Em outro terminal, execute o cliente para se conectar ao servidor e interagir com o sistema.

    ```bash
    make client
    ```

-----

## Documentação Técnica (Conforme Requisitos)

Esta seção detalha a arquitetura do banco de dados e o protocolo de comunicação, conforme solicitado.

### 1\. Estrutura do Banco de Dados

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
| `rating` | `REAL` | Avaliação do filme (ex: 4.5). |
| `duration_min`| `INTEGER` | Duração do filme em minutos. |
| `gender` | `VARCHAR` | Gênero do filme (ex: Ação, Comédia). |
| `created_at`| `DATETIME` | Data e hora da criação do registro. |
| `updated_at`| `DATETIME` | Data e hora da última atualização. |

-----

-----

### Validação de inputs
Todas as validações são realizadas através do processo interno do fastAPI que faz uso do pydantic. São realizadas validação sintática quanto semantica.

Por exemplo, o campo `age` da tabela `director` aceita apenas números inteiros positivos. Caso o usuário passe um valor negativo para o _endpoint_ ele terá a seguinte resposta:

> Status: `422 Unprocessable Content`

```shell
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