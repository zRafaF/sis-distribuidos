Com certeza. Realizei a mesclagem, combinando a estrutura clara e os exemplos do seu README atual com a documentação técnica detalhada (esquema do banco, fluxogramas, etc.) que atende aos requisitos do professor. O resultado é um documento único e completo.

-----

# Sistema de Gerenciamento de Filmes via Sockets

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

Primeiro navegue até a pasta com:

```bash
cd atividadesSockets
```

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

### 2\. Estrutura e Fluxo dos Pacotes

A comunicação é baseada em "pacotes" que consistem em um cabeçalho de tamanho fixo seguido por uma mensagem de tamanho variável.

#### Enquadramento do Pacote (Framing)

Cada pacote enviado pela rede possui a seguinte estrutura de bytes:

| Parte | Tamanho (Bytes) | Descrição |
| :--- | :--- | :--- |
| **Cabeçalho** | 8 bytes | Um inteiro (big-endian) que representa o tamanho da mensagem que se segue. |
| **Mensagem** | Variável | A string da mensagem, codificada em UTF-8. |

#### Formato da Mensagem

A mensagem em si é uma string com campos delimitados por `@`, seguindo a estrutura geral já descrita:

`COMANDO@TABELA@ID_REGISTRO@PAYLOAD`

-----

### Detalhamento por Operação

A seguir, o detalhamento do pacote e o fluxo para cada método principal.

#### Operação: Criar (`CREATE`)

  - **Descrição:** Cria um novo registro (Filme ou Diretor).

  - **Requisição (Cliente -\> Servidor):**

      - Formato: `C@<tabela>@-1@<payload_com_dados>`
      - Exemplo (Filme): `C@MOV@-1@title=Pulp Fiction|director_id=1|rating=5|duration_min=154|gender=Crime`

  - **Resposta de Sucesso (Servidor -\> Cliente):**

      - Formato: `SUCCESS@<tabela>@<novo_id>@<payload_com_dados_e_id>`
      - Exemplo (Filme): `SUCCESS@MOV@25@id=25|title=Pulp Fiction|director_id=1|...`

  - **Resposta de Erro:**

      - Formato: `ERROR@<tabela>@-1@error=<descrição_do_erro>`

  - **Fluxograma (Criar Filme, lógica do cliente):**

    ```mermaid
    sequenceDiagram
        participant User as Usuário
        participant Client as Cliente
        participant Server as Servidor
        participant DB as Banco de Dados

        User->>Client: Inicia criação de filme
        Client->>Server: Requisição: R@DIR@-1@ (Listar todos os diretores)
        Server->>DB: SELECT * FROM Directors
        DB-->>Server: Retorna lista de diretores
        Server-->>Client: Resposta: SUCCESS@DIR@-1@directors=[...]

        alt Diretor NÃO existe na lista
            Client->>Server: Requisição: C@DIR@-1@name=Quentin Tarantino
            Server->>DB: INSERT INTO Directors...
            DB-->>Server: Retorna novo ID do diretor
            Server-->>Client: Resposta: SUCCESS@DIR@1@id=1|name=...
        end

        Client->>Server: Requisição: C@MOV@-1@title=Pulp Fiction|director_id=1|...
        Server->>DB: INSERT INTO Movies...
        DB-->>Server: Retorna novo ID do filme
        Server-->>Client: Resposta: SUCCESS@MOV@25@id=25|...
        Client->>User: Exibe mensagem de sucesso
    ```

#### Operação: Ler (`READ`)

  - **Descrição:** Lê um ou todos os registros de uma tabela.

  - **Requisição (Cliente -\> Servidor):**

      - Formato (Um registro): `R@<tabela>@<id>@`
      - Formato (Todos): `R@<tabela>@-1@`
      - Exemplo: `R@MOV@25@`

  - **Resposta de Sucesso (Servidor -\> Cliente):**

      - Formato: `SUCCESS@<tabela>@-1@<chave_plural>=[{...},{...}]`
      - Exemplo: `SUCCESS@MOV@-1@movies=[{'id': 25, 'title': 'Pulp Fiction', ...}]`

  - **Resposta de Erro:**

      - Formato: `ERROR@<tabela>@<id>@error=Movie not found`

  - **Fluxograma (Ler um Filme):**

    ```mermaid
    sequenceDiagram
        participant User as Usuário
        participant Client as Cliente
        participant Server as Servidor
        participant DB as Banco de Dados

        User->>Client: Pede para ver filme com ID 25
        Client->>Server: Requisição: R@MOV@25@
        Server->>DB: SELECT * FROM Movies WHERE id = 25
        DB-->>Server: Retorna dados do filme
        Server-->>Client: Resposta: SUCCESS@MOV@-1@movies=[{...}]
        Client->>User: Exibe dados do filme
    ```

#### Operação: Atualizar (`UPDATE`)

  - **Descrição:** Modifica um registro existente.

  - **Requisição (Cliente -\> Servidor):**

      - Formato: `U@<tabela>@<id>@<payload_com_dados_a_mudar>`
      - Exemplo: `U@MOV@25@rating=4.9|title=Pulp Fiction!`

  - **Resposta de Sucesso (Servidor -\> Cliente):**

      - Formato: `SUCCESS@<tabela>@<id>@<payload_com_todos_dados_atualizados>`
      - Exemplo: `SUCCESS@MOV@25@id=25|title=Pulp Fiction!|rating=4.9|...`

  - **Resposta de Erro:**

      - Formato: `ERROR@<tabela>@<id>@error=Movie not found`

  - **Fluxograma (Atualizar um Filme):**

    ```mermaid
    sequenceDiagram
        participant User as Usuário
        participant Client as Cliente
        participant Server as Servidor
        participant DB as Banco de Dados

        User->>Client: Pede para atualizar filme ID 25
        Client->>Server: Requisição: U@MOV@25@rating=4.9
        Server->>DB: UPDATE Movies SET rating = 4.9 WHERE id = 25
        DB-->>Server: Confirmação de atualização
        Server-->>Client: Resposta: SUCCESS@MOV@25@id=25|...
        Client->>User: Exibe mensagem de sucesso
    ```

#### Operação: Deletar (`DELETE`)

  - **Descrição:** Remove um registro do banco de dados.

  - **Requisição (Cliente -\> Servidor):**

      - Formato: `D@<tabela>@<id>@`
      - Exemplo: `D@MOV@25@`

  - **Resposta de Sucesso (Servidor -\> Cliente):**

      - Formato: `SUCCESS@<tabela>@<id>@id=<id>`
      - Exemplo: `SUCCESS@MOV@25@id=25`

  - **Resposta de Erro:**

      - Formato: `ERROR@<tabela>@<id>@error=Movie not found`

  - **Fluxograma (Deletar um Filme):**

    ```mermaid
    sequenceDiagram
        participant User as Usuário
        participant Client as Cliente
        participant Server as Servidor
        participant DB as Banco de Dados

        User->>Client: Pede para deletar filme ID 25
        Client->>Server: Requisição: D@MOV@25@
        Server->>DB: DELETE FROM Movies WHERE id = 25
        DB-->>Server: Confirmação de exclusão
        Server-->>Client: Resposta: SUCCESS@MOV@25@id=25
        Client->>User: Exibe mensagem de sucesso
    ```

-----

## Interação do Cliente

O cliente (`client.py`) oferece uma interface de menu simples para o usuário final.

```
Banco de Dados de Filmes
Voce pode inserir (c), ler (r), atualizar (u), deletar registros (d) ou sair (e)
```

  - **`c` (Criar):** O programa solicita ao usuário o nome do filme, nome do diretor, gênero, avaliação e duração. Em seguida, ele primeiro verifica se o diretor já existe no banco de dados (enviando uma mensagem `R@DIR@-1@...`). Se não existir, ele cria o diretor (com uma mensagem `C@DIR@-1@...`) e, por fim, cria o filme com o ID do diretor correspondente (`C@MOV@-1@...`).
  - **`r` (Ler):** O usuário pode inserir o ID de um filme específico para ver seus detalhes ou a letra `a` para listar todos os filmes no banco de dados.
  - **`u` (Atualizar):** O usuário informa o ID do filme que deseja modificar e, em seguida, escolhe quais campos (nome, diretor, gênero, etc.) deseja alterar. O cliente monta e envia a mensagem de `UPDATE` correspondente.
  - **`d` (Deletar):** O usuário informa o ID do filme a ser removido, e o cliente envia uma mensagem de `DELETE`.
  - **`e` (Sair):** Encerra a conexão com o servidor e finaliza o programa cliente.

## Limitações e Pontos de Melhoria

Como um projeto com fins didáticos, a implementação atual possui algumas simplificações e limitações conhecidas que seriam abordadas em um ambiente de produção:

  * **Robustez do Protocolo de Mensagens:** O protocolo utiliza os caracteres `@`, `|` e `=` como delimitadores. Se algum desses caracteres for inserido em um campo de texto (como o nome de um filme), a lógica de parse da mensagem falhará, causando um erro. Uma solução em um sistema real seria tratar esses valores, por exemplo, com URL encoding.

  * **Gerenciamento de Diretores no Cliente:** A lógica para verificar se um diretor já existe antes de criar um filme está implementada no lado do cliente. Isso resulta em múltiplas chamadas de rede para uma única operação do usuário. Uma implementação mais eficiente transferiria essa responsabilidade para o servidor.

  * **Esquema do Banco de Dados:** A separação dos diretores em uma tabela própria serve principalmente para demonstrar a interação entre duas tabelas. O esquema como um todo é simplificado e poderia ser expandido com mais campos e relações (ex: atores, estúdios, etc.).

  * **Ausência de Paginação:** A requisição para ler múltiplos registros (ex: listar todos os filmes) retorna o conjunto de dados completo de uma só vez. Em um banco de dados com milhares de registros, isso seria extremamente ineficiente. Uma implementação de produção exigiria paginação.

  * **Falta de Segurança e Autenticação:** O sistema não possui nenhuma camada de autenticação ou autorização. Qualquer pessoa com acesso à rede pode se conectar ao servidor e executar qualquer operação.

  * **Tratamento de Erros Simplificado:** As respostas de erro são genéricas. A utilização de códigos de erro específicos permitiria que o cliente tratasse as falhas de forma mais inteligente e apresentasse feedback mais útil ao usuário.