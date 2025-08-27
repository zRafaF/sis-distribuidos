import socket


import defines as d


# def crud_create(data, table, payload):
#     message = d.create_message(
#         d.Command.CREATE,
#         table,
#         record_id=d.WILDCARD_ID,
#         payload_dict={
#             "title": data[0],
#             "director": data[1],
#             "gender": data[2],
#             "rating": data[3],
#             "duration_min": data[4],
#         },
#     )

#     return message


# def crud_read(id=d.WILDCARD_ID):
#     # if id == wildcard_id, read all registry
#     message = d.create_message(
#         d.Command.READ, d.Table.MOVIE, record_id=id, payload_dict={}
#     )

#     return message

sock = socket.socket()
sock.connect((d.HOST, d.PORT))


def accept_only_int_input(disp_str=""):
    while True:
        if disp_str != "":
            print(disp_str)
        try:
            num_input = input()
            num_input = int(num_input)
        except ValueError:
            continue
        return num_input


def usr_create():
    new_data = []
    print("Insira o nome do filme: ")
    new_data.append(input())
    print("Insira o nome do diretor: ")
    new_data.append(input())
    print("Insira o gênero do filme: ")
    new_data.append(input())

    while True:
        num = accept_only_int_input("Insira a avaliação do filme (0 à 5): ")
        if num < 0 or num > 5:
            continue
        new_data.append(num)
        break

    new_data.append(accept_only_int_input("Insira a duração do filme em minutos: "))

    return new_data


def usr_read():
    while True:
        print(
            "Insira o ID do filme que deseja visualizar, ou 'a' \
                para visualizar todos."
        )

        usr_input = input()
        if usr_input != "a":
            try:
                id = int(usr_input)
            except ValueError:
                continue


def usr_update():
    while True:
        print("Insira o ID do filme que deseja atualizar, ou 'e' para sair.")
        id_input = accept_only_int_input()
        if id_input < 0:
            continue

        d.send_message(
            sock,
            d.create_message(
                d.CommandResponse.READ,
                d.Table.MOVIE,
                record_id=id_input,
                payload_dict={},
            ),
        )

        while True:
            print(
                "Você pode atualizar o nome do filme (n), nome do diretor (d), \
                  gênero do filme (g), a avaliação do filme (a), e a duração do filme (l). \
                  Também pode sair (e)."
            )

            new_data = {}
            if id_input == "n":
                new_data.update()
            elif id_input == "d":
                pass
            elif id_input == "g":
                pass
            elif id_input == "a":
                pass
            elif id_input == "l":
                pass
            elif id_input == "e":
                break
            else:
                continue


def get_or_create_director(name: str, sock: socket.socket) -> int:
    d.send_message(
        sock,
        d.create_message(
            d.CommandResponse.READ,
            d.Table.DIRECTOR,
            record_id=d.WILDCARD_ID,
            payload_dict={},
        ),
    )
    sock.settimeout(1.0)

    try:
        response = d.receive_message(sock)
    except socket.timeout:
        print("No response received within 1 second.")
        return -1

    parsed_msg = d.parse_message(response)
    if parsed_msg:
        directors_list = parsed_msg.payload

        for director in directors_list.get("directors", []):
            if director.get("name") == name:
                print("Director found:", director)
                return director.get("id")

        print("Director not found, creating a new one.")
        # Se o diretor não for encontrado, cria um novo
        d.send_message(
            sock,
            d.create_message(
                d.CommandResponse.CREATE,
                d.Table.DIRECTOR,
                record_id=d.WILDCARD_ID,
                payload_dict={"name": name},
            ),
        )

        try:
            response = d.receive_message(sock)
        except socket.timeout:
            print("No response received within 1 second.")
            return -1

        parsed_director_response = d.parse_message(response)

        if parsed_director_response:
            return parsed_director_response.payload.get("id")

    return -1  # Indica que houve um erro


def usr_interaction():
    print("banco de dados de filmes")

    while True:
        print(
            "Voce pode inserir (c), ler (r), atualizar (u), deletar registros (d) \
            ou sair (e)"
        )

        usr_input = input()
        if usr_input == "c":
            new_data = usr_create()

            new_director_id = get_or_create_director(new_data[1], sock)

            if new_director_id == -1:
                print("Erro ao obter ou criar o diretor.")
                return

            d.send_message(
                sock,
                d.create_message(
                    d.CommandResponse.CREATE,
                    d.Table.MOVIE,
                    record_id=d.WILDCARD_ID,
                    payload_dict={
                        "title": new_data[0],
                        "director_id": new_director_id,
                        "gender": new_data[2],
                        "rating": new_data[3],
                        "duration_min": new_data[4],
                    },
                ),
            )

            try:
                response = d.receive_message(sock)
                if response:
                    print("Received response from server:", response)
            except socket.timeout:
                print("No response received within 1 second.")

        elif usr_input == "r":
            id = usr_read()
            d.send_message(
                sock,
                d.create_message(
                    d.CommandResponse.READ,
                    d.Table.MOVIE,
                    record_id=id if id != "a" else d.WILDCARD_ID,
                    payload_dict={},
                ),
            )

        elif usr_input == "u":
            id = usr_update()

        elif usr_input == "d":
            pass
        elif usr_input == "e":
            pass
        else:  # input not in possible inputs
            continue


def main():
    usr_interaction()


if __name__ != "main":
    main()
