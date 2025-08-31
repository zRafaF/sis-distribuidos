import socket


import defines as d


sock = socket.socket()
sock.connect((d.HOST, d.PORT))
sock.settimeout(1.0)


class Movie:
    def __init__(
        self, director_id, movie_id, director_name, title, rating, gender, duration_min
    ):
        self.director_db_id = director_id
        self.movie_db_id = movie_id
        self.director_name = director_name
        self.title = title
        self.rating = rating
        self.gender = gender
        self.duration_min = duration_min

    def print_self(self):
        print(
            f"ID do filme no banco de dados: {self.movie_db_id}\n \
        Nome do filme: {self.title}\n \
        Nome do diretor: {self.director_name}\n \
        Gênero do filme: {self.gender}\n \
        Duração do filme em minutos: {self.duration_min}\n \
        Nota do filme (0 a 5): {self.rating}"
        )


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


def usr_interaction_create():
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


def usr_interaction_read():
    while True:
        print(
            "Insira o ID do filme que deseja visualizar, ou 'a' \
                para visualizar todos."
        )

        usr_input = input()
        if usr_input != "a":
            try:
                id = int(usr_input)
                return id
            except ValueError:
                continue
        else:
            return d.WILDCARD_ID


def handle_update():
    while True:
        print("Insira o ID do filme que deseja atualizar, ou 'e' para sair.")
        id_input = accept_only_int_input()
        if id_input < 0:
            continue

        movies = get_movie_data(id_input)

        if len(movies) > 1:
            print("Mais de um filme retornado, algo deu errado.")
            return -1

        movie = movies[0] if movies else None

        if movie is None:
            print("Filme não encontrado.")
            return -1
        else:
            updated_movie = Movie(
                movie.director_db_id,
                movie.movie_db_id,
                movie.director_name,
                movie.title,
                movie.rating,
                movie.gender,
                movie.duration_min,
            )

            while True:
                print(
                    "Você pode atualizar o nome do filme (n), nome do diretor (d), \
                      gênero do filme (g), a avaliação do filme (a), e a duração do filme (l). \
                      Também pode sair (e)."
                )

                usr_input = input()

                if usr_input == "n":
                    print("Insira o novo nome do filme")
                    updated_movie.title = input()
                    continue
                elif usr_input == "d":
                    print("Insira o nome do diretor do filme")
                    updated_movie.director = input()
                    if get_or_create_director(updated_movie.director, sock) != -1:
                        continue
                    print("LOG: Erro ao atualizar nome do diretor")
                elif usr_input == "g":
                    print("Insira o novo gênero do filme")
                    updated_movie.gender = input()
                    continue
                elif usr_input == "a":
                    print("Insira a nova avaliação do filme")
                    new_rating = -1
                    while new_rating > 5 or new_rating < 0:
                        new_rating = accept_only_int_input()
                    updated_movie.rating = new_rating
                    continue
                elif usr_input == "l":
                    print("Insira a nova duração do filme")
                    updated_movie.duration_min = accept_only_int_input()
                    continue
                elif usr_input == "e":
                    break
                else:
                    continue

            update_movie(updated_movie)


def update_movie(new_data: Movie):
    d.send_message(
        sock,
        d.create_message(
            d.CommandResponse.UPDATE,
            d.Table.DIRECTOR,
            record_id=new_data.director_db_id,
            payload_dict={"name": new_data.director_name},
        ),
    )

    # Checar se deu certo
    server_msg = d.receive_message(sock)
    if server_msg == None:
        return -1

    parsed_msg = d.parse_message(server_msg)
    if parsed_msg == None:
        return -1

    if parsed_msg.command == d.CommandResponse.ERROR:
        print("LOG: Falha na atualização do diretor")
        return -1

    d.send_message(
        sock,
        d.create_message(
            d.CommandResponse.UPDATE,
            d.Table.MOVIE,
            record_id=new_data.movie_db_id,
            payload_dict={
                "title": new_data.title,
                "director_id": new_data.director_db_id,
                "gender": new_data.gender,
                "rating": new_data.rating,
                "duration_min": new_data.duration_min,
            },
        ),
    )

    # Checar se deu certo
    server_msg = d.receive_message(sock)
    if server_msg == None:
        return -1

    parsed_msg = d.parse_message(server_msg)
    if parsed_msg == None:
        return -1

    if parsed_msg.command == d.CommandResponse.ERROR:
        print("LOG: Falha na atualização do filme")
        return -1

    return 0


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


def handle_create():
    new_data = usr_interaction_create()

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


def get_movie_data(id):
    # Get the movie's data
    d.send_message(
        sock,
        d.create_message(
            d.CommandResponse.READ,
            d.Table.MOVIE,
            record_id=id,
            payload_dict={},
        ),
    )

    server_msg = d.receive_message(sock)

    if server_msg == None:
        return -1

    parsed_msg = d.parse_message(server_msg)

    if parsed_msg == None:
        return -1

    if parsed_msg.command == d.CommandResponse.ERROR:
        print("Esse filme não está presente no banco de dados.")
        return None

    movies_list = parsed_msg.payload

    if movies_list == {}:
        return -1

    movies: list[Movie] = []

    for movie in movies_list.get("movies", []):
        d.send_message(
            sock,
            d.create_message(
                d.CommandResponse.READ,
                d.Table.DIRECTOR,
                record_id=movie.get("director_id"),
                payload_dict={},
            ),
        )

        director_msg = d.receive_message(sock)
        directors_list = d.parse_message(director_msg).payload.get("directors", [])

        director = directors_list[0]

        movies.append(
            Movie(
                director_id=movie.get("director_id"),
                movie_id=movie.get("id"),
                director_name=director.get("name") if director else "Unknown",
                title=movie.get("title"),
                rating=movie.get("rating"),
                gender=movie.get("gender"),
                duration_min=movie.get("duration_min"),
            )
        )

    return movies


def handle_delete():
    print("Insira o ID do filme que deseja deletar")
    id = -1
    while id < 0:
        id = accept_only_int_input()

    d.send_message(
        sock,
        d.create_message(
            d.CommandResponse.DELETE, d.Table.MOVIE, record_id=id, payload_dict={}
        ),
    )

    # Checar se deu certo
    server_msg = d.receive_message(sock)
    if server_msg == None:
        return -1

    parsed_msg = d.parse_message(server_msg)
    if parsed_msg == None:
        return -1

    if parsed_msg.command == d.CommandResponse.ERROR:
        print("LOG: erro ao deletar o registro")
        return -1

    if parsed_msg.command == d.CommandResponse.SUCCESS:
        print("Filme deletado com sucesso do banco de dados")
        return 0


def ler_todos_diretores():
    d.send_message(
        sock,
        d.create_message(
            d.CommandResponse.READ, d.Table.DIRECTOR, d.WILDCARD_ID, payload_dict={}
        ),
    )

    msg = d.receive_message(sock)

    parsed_msg = d.parse_message(msg)

    parsed_payload = d.parse_payload(parsed_msg.payload)

    print("diretores:")
    for values in parsed_payload.values:
        print(values)


def usr_interaction():
    print("banco de dados de filmes")

    while True:
        print(
            "Voce pode inserir (c), ler (r), atualizar (u), deletar registros (d) \
            ou sair (e)"
        )

        usr_input = input()
        if usr_input == "c":
            handle_create()
        elif usr_input == "r":
            id = usr_interaction_read()
            movies = get_movie_data(id)
            if movies == None:
                continue
            print("\n" * 5)
            for movie in movies:
                print("-_-_" * 20)
                movie.print_self()
                print()
        elif usr_input == "l":
            ler_todos_diretores()
        elif usr_input == "u":
            handle_update()
        elif usr_input == "d":
            handle_delete()
        elif usr_input == "e":
            sock.shutdown(socket.SHUT_RDWR)
            return 0
        else:  # input not in possible inputs
            continue


def main():
    usr_interaction()
    return 0


if __name__ != "main":
    main()
