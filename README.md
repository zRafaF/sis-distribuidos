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
    O servidor irá inicializar o banco de dados `database.db` (se não existir) e começará a escutar por conexões.

    ```bash
    make server
    ```

2.  **Inicie o Cliente:**
    Em outro terminal, execute o cliente para se conectar ao servidor e interagir com o sistema.

    ```bash
    make client
    ```

## Protocolo de Comunicação

A comunicação é baseada em mensagens de texto com uma estrutura bem definida, separada por delimitadores.

### Transporte e Enquadramento de Mensagem

Para garantir que as mensagens sejam recebidas de forma completa e sem corrupção, o protocolo utiliza um cabeçalho de tamanho fixo. Antes de qualquer mensagem ser enviada, seu tamanho total em bytes é calculado. Esse tamanho é então enviado como um cabeçalho de 8 bytes (`MSG_SIZE_HEADER`). O receptor primeiro lê esses 8 bytes para determinar o tamanho da mensagem que está por vir e, em seguida, lê exatamente esse número de bytes para obter a mensagem completa.

A estrutura enviada pelo socket é: `[CABEÇALHO DE 8 BYTES COM O TAMANHO][MENSAGEM COMPLETA]`

### Estrutura Geral da Mensagem

Cada mensagem de texto (enviada após o cabeçalho de tamanho) é formatada da seguinte maneira:

`COMANDO@TABELA@ID_REGISTRO@PAYLOAD`

  - **`COMANDO`**: Representa a operação (para o cliente) ou o status da resposta (para o servidor).
      - **Comandos do Cliente**: `C` (Create), `R` (Read), `U` (Update), `D` (Delete).
      - **Respostas do Servidor**: `SUCCESS`, `ERROR`.
  - **`TABELA`**: Um código de 3 letras que identifica a tabela do banco de dados.
      - `DIR`: Tabela de Diretores (`Directors`)
      - `MOV`: Tabela de Filmes (`Movies`)
  - **`ID_REGISTRO`**: O ID numérico do registro a ser afetado. Para operações que não visam um registro específico (como criar um novo ou listar todos), utiliza-se o valor `WILDCARD_ID`, que é **-1**.
  - **`PAYLOAD`**: Uma string contendo os dados da requisição ou resposta, com o formato `chave1=valor1|chave2=valor2`.

### Estrutura do Payload

O payload é uma série de pares chave-valor:

  - Pares são separados pelo caractere pipe (`|`).
  - A chave e o valor dentro de um par são separados pelo sinal de igual (`=`).

### Codificação de Tipos Complexos (Arrays e Dicionários)

O payload pode transportar não apenas valores simples, mas também estruturas de dados complexas como listas (arrays) e dicionários.

  - **Envio**: Ao criar uma mensagem, qualquer valor que seja uma lista ou dicionário é convertido para sua representação em formato de string. Por exemplo, uma lista de filmes é formatada como uma string que se parece com uma lista literal do Python.
  - **Recebimento**: O receptor utiliza a função `ast.literal_eval` para analisar a string e reconstruir a estrutura de dados original (lista, dicionário, etc.) de forma segura.

Isso é comumente usado em respostas de leitura (`READ`) que retornam múltiplos registros.

### Respostas do Servidor

Para cada requisição do cliente, o servidor envia uma resposta. A estrutura da resposta segue o mesmo formato da mensagem, mas o campo `COMANDO` indica o resultado da operação.

#### Respostas de Sucesso

Ocorrem quando a operação solicitada foi concluída com êxito. O comando da mensagem será `SUCCESS`.

  - **Ao Criar (`CREATE`):** A resposta contém no payload os dados completos do novo registro, incluindo o ID gerado pelo banco de dados.
  - **Ao Ler (`READ`):** O payload da resposta contém o registro solicitado ou uma lista de registros.
  - **Ao Atualizar (`UPDATE`):** A resposta contém os dados atualizados do registro para confirmação.
  - **Ao Deletar (`DELETE`):** A resposta confirma a remoção, geralmente retornando o ID do registro que foi deletado no payload.

#### Respostas de Erro

Ocorrem quando a operação não pôde ser concluída. O comando da mensagem será `ERROR`.

  - O payload da resposta geralmente contém uma chave `error` com uma string descrevendo o problema.
  - Erros comuns incluem registro não encontrado, dados faltando na requisição ou formato de mensagem inválido.

### Exemplos de Mensagens

  * **Cliente para Servidor: Criar um novo diretor**
    ```
    C@DIR@-1@name=Christopher Nolan
    ```
  * **Cliente para Servidor: Ler todos os filmes (usando o `WILDCARD_ID`)**
    ```
    R@MOV@-1@
    ```
  * **Servidor para Cliente: Resposta de sucesso com uma lista de filmes**
    O payload contém uma chave "movies" cujo valor é a representação em string de uma lista de dicionários.
    ```
    SUCCESS@MOV@-1@movies=[{'id': 15, 'title': 'Inception', 'director_id': 1}, {'id': 16, 'title': 'The Dark Knight', 'director_id': 1}]
    ```
  * **Servidor para Cliente: Resposta de erro ao buscar um filme**
    ```
    ERROR@MOV@99@error=Movie not found
    ```

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

* **Gerenciamento de Diretores no Cliente:** A lógica para verificar se um diretor já existe antes de criar um filme está implementada no lado do cliente. Isso resulta em múltiplas chamadas de rede para uma única operação do usuário (uma para ler os diretores, possivelmente outra para criar um novo diretor, e uma terceira para criar o filme). Uma implementação mais eficiente transferiria essa responsabilidade para o servidor, que resolveria a dependência do diretor em uma única requisição.

* **Esquema do Banco de Dados:** A separação dos diretores em uma tabela própria é uma prática de normalização correta, mas a forma como é utilizada serve principalmente para demonstrar a interação entre duas tabelas em um sistema cliente-servidor. O esquema como um todo é simplificado para este exemplo e poderia ser expandido com mais campos e relações (ex: atores, estúdios, etc.).

* **Ausência de Paginação:** A requisição para ler múltiplos registros (ex: listar todos os filmes) retorna o conjunto de dados completo de uma só vez. Em um banco de dados com milhares de registros, isso seria extremamente ineficiente, consumindo uma grande quantidade de memória no servidor, banda de rede e recursos no cliente. Uma implementação de produção exigiria paginação, permitindo que o cliente solicitasse os dados em "páginas" menores (ex: "traga os 20 primeiros filmes", "agora traga os próximos 20").