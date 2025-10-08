import Pyro5.api
import Pyro5.client
import Movie 

import defines as d

def accept_only_int_input(disp_str=''):
    while True:
        if disp_str != '':
            print(disp_str)
        try:
            num_input = input('--> ')
            num_input = int(num_input)
        except ValueError:
            continue

        return num_input

def create():
    new_movie = {}
    
    print('Insira o nome do filme: ')
    new_movie['name'] = input('--> ')

    print('Insira o nome do diretor: ')
    new_movie['director_name'] = input('--> ')

    print('Insira o gênero do filme: ')
    new_movie['gender'] = input('--> ')
    
    while True:
        num = accept_only_int_input("Insira a avaliação do filme (0 à 5): ")
        if num < 0 or num > 5:
            continue
        new_movie['rating'] = num
        break

    new_movie['length'] = accept_only_int_input('Insira a duração do filme em minutos; ')

    # Movie's and director's IDs will be set serverside 
    movie = Movie.Movie(None, None, new_movie['name'], new_movie['director_name'],
                        new_movie['length'], new_movie['gender'],
                        new_movie['rating']
                    ) 
    
    CRUD_proxy.create_movie(movie)

def read():
    movid = accept_only_int_input(f'Insira o ID do filme que deseja ler, ou {d.WILDCARD_ID} para ler todos.')
    
    movies = CRUD_proxy.read_movie(movid)

    # To aid in wireshark packet capture
    #input('Executou read_movie()\n*--> ')

    if len(movies) == 0:
        print('Não há filme com esse ID, :(')

    else:
        print('\n'*50)
        for movie in movies:
            print('-'*30, '\n')
            print(f"Título : {movie.title}\n" \
                    f"Diretor : {movie.director_name}\n" \
                    f"Gênero : {movie.gender}\n" \
                    f"Duração : {movie.length_minutes} minutos\n" \
                    f"Avaliação : {movie.rating:.0f} estrelas (0 a 5).\n"
                )

        print('*'*30, '\n')

def update():
    while True:
        print('Insira o ID do filme que deseja atualizar ou \'e\' para sair.')
        id_input = input('--> ')
        if id_input == 'e':
            break

        try: 
            id_input = int(id_input)
        except ValueError:
            continue

        if id_input < 0:
            continue

        movie = CRUD_proxy.read_movie(id_input)
        if len(movie) == 0:
            print('Não há filme com esse ID.')
            continue
        
        # There will be only one movie
        movie = movie[0]
        updated_movie = Movie.Movie(movie.id, movie.director_id, movie.title, 
                            movie.director_name, movie.length_minutes,
                            movie.gender, movie.rating
                        )
        
        update = False
        while True:
            print(
                "Você pode atualizar:\nNome do filme (n)\nNome do diretor (d)\nGênero do filme (g)\nAvaliação do filme (a)\nDuração do filme (l)."
            )

            if update:
                print("Digite 'e' para sair e salvar as alterações.")
            else:
                print("Digite 'e' para sair.")

            usr_input = input('--> ')

            match usr_input: 
                case "n":
                    print("Insira o novo nome do filme")
                    updated_movie.title = input('--> ')
                    update = True
                case "d":
                    print("Insira o nome do diretor do filme")
                    updated_movie.director_name = input('--> ')
                    update = True
                case "g":
                    print("Insira o novo gênero do filme")
                    updated_movie.gender = input('--> ')
                    update = True
                case "a":
                    print("Insira a nova avaliação do filme")
                    new_rating = -1
                    while new_rating > 5 or new_rating < 0:
                        new_rating = accept_only_int_input('--> ')
                    updated_movie.rating = new_rating
                    update = True
                case "l":
                    print("Insira a nova duração do filme")
                    updated_movie.length_min = accept_only_int_input('--> ')
                    update = True
                case "e":
                    break
                case _: 
                    continue

        if update == True:
            CRUD_proxy.update_movie(id_input, updated_movie)     

        break

def delete():
    print(f'Insira o ID do filme que deseja deletar, ou {d.WILDCARD_ID} para deletar' \
            'todos os filmes')
    id_input = d.WILDCARD_ID - 1 
    while id_input < d.WILDCARD_ID:
        id_input = accept_only_int_input('--> ')

    deleted_movies = CRUD_proxy.delete_movie(id_input)
    if len(deleted_movies) != 0:
        print('Filme(s) deletado(s) do banco de dados com sucesso!') 
        print('\nFilme(s) deletado(s):\n')
        for movie in deleted_movies:
            print(f"- {movie.title}\n")
        print('*'*30, '\n')
    else:
        print('Não há filme com esse ID.')

def usr_interaction():
    print("Banco de Dados de Filmes")

    while True:
        print(
            "Voce pode inserir (c), ler (r), atualizar (u), deletar registros (d)"
            " ou sair (e)"
        )

        usr_input = input('--> ')
        match usr_input:
            case 'c':
                create()
            case 'r':
                read()
            case 'u':
                update()
            case 'd':
                delete()
            case 'e':
                return 0
            case _: 
                continue
    

if __name__ == '__main__':
    CRUD_proxy = Pyro5.client.Proxy('PYRONAME:FabioRafael')

    # To aid in wireshark packet capture
    # input('*--> ')

    if not CRUD_proxy._pyroBind():
        print('LOG : falha no pyro_bind')
    # To aid in wireshark packet capture
    # input('*--> ')

    Pyro5.api.register_class_to_dict(Movie.Movie, Movie.Movie_to_dict)
    Pyro5.api.register_dict_to_class("Movie.Movie", Movie.dict_to_Movie)

    usr_interaction()
