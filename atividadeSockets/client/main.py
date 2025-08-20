import socket

import sys, os

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
sys.path.insert(0, project_root)

from atividadeSockets import defines as d


def crud_create(data):
    message = d.create_message(
        d.Command.CREATE,
        d.Table.MOVIE,
        record_id=d.WILDCARD_ID,
        payload_dict={
            "title": data[0],
            "director": data[1],
            "gender": data[2],
            "rating": data[3],
            "duration_min": data[4],
        },
    )

    return message


def crud_read(id=d.WILDCARD_ID):
    # if id == wildcard_id, read all registry
    message = d.create_message(
        d.Command.READ, d.Table.MOVIE, record_id=id, payload_dict={}
    )

    return message


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


def usr_interaction(sock):
    print("banco de dados de filmes")

    while True:
        print(
            "Voce pode inserir (c), ler (r), atualizar (u), deletar registros (d) \
            ou sair (e)"
        )

        usr_input = input()
        if usr_input == "c":
            new_data = usr_create()
            d.send_message(sock, crud_create(new_data))

        elif usr_input == "r":
            id = usr_read()
            d.send_message(sock, crud_read(id))

        elif usr_input == "u":
            pass
        elif usr_input == "d":
            pass
        elif usr_input == "e":
            pass
        else:  # input not in possible inputs
            continue


def set_conn():
    s = socket.socket()
    s.connect(d.HOST, d.PORT)

    return s


def main():
    s = set_conn()
    usr_interaction(s)


if __name__ != "main":
    main()
