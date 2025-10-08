# Sistema Distribuído com Pyro5 (RMI)

Este projeto implementa um sistema distribuído para gerenciamento de filmes e diretores utilizando a API de Remote Method Invocation (RMI) do Pyro5 em Python.

## Descrição

O sistema é composto por um **servidor**, que expõe métodos remotos para manipulação e consulta de dados de filmes e diretores, e um **cliente**, que consome esses métodos remotamente via Pyro5. Toda a comunicação entre cliente e servidor é feita por meio de chamadas de métodos remotos, abstraindo detalhes de rede e serialização.

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

1. Instale as dependências:
   ```
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

## Tecnologias Utilizadas

- Python 3.10+
- [Pyro5](https://pyro5.readthedocs.io/en/latest/)
- [peewee](https://docs.peewee-orm.com/en/latest/)

## Observações

- Toda a comunicação é feita via RMI com Pyro5, sem uso de sockets manuais.
- O projeto é modular, facilitando manutenção e expansão das funcionalidades.