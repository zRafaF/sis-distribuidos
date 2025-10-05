import Pyro5.api
import Pyro5.client
import Movie 

CRUD_proxy = Pyro5.client.Proxy('PYRONAME:CRUD')

if not CRUD_proxy._pyro_bind():
    print('LOG : falha no pyro_bind')

Pyro5.api.register_class_to_dict(Movie.Movie, Movie.Movie_to_dict)

def accept_only_int_input(disp_str=''):
    while True:
        if disp_str != '':
            print(disp_str)
        try:
            num_input = input()
            num_input = int(num_input)
        except ValueError:
            continue

        return num_input

def create():
    new_movie = {}
    
    print('Insira o nome do filme: ')
    new_movie['name'] = input()

    print('Insira o nome do diretor: ')
    new_movie['director_name'] = input()

    print('Insira o gênero do filme: ')
    new_movie['gender'] = input()
    
    while True:
        num = accept_only_int_input("Insira a avaliação do filme (0 à 5): ")
        if num < 0 or num > 5:
            continue
        new_movie['rating'] = num
        break

    new_movie['length'] = accept_only_int_input('Insira a duração do filme em minutos; ')

    movie = Movie.Movie(new_movie['name'], new_movie['director_name'],
                        new_movie['length'], new_movie['gender'],
                        new_movie['rating']
                    )


def usr_interaction():
    print("Banco de Dados de Filmes")

    while True:
        print(
            "Voce pode inserir (c), ler (r), atualizar (u), deletar registros (d)"
            " ou sair (e)"
        )

        usr_input = input()
        match usr_input:
            case 'c':
                create()
            case 'r':
                pass
            case 'u':
                pass
            case 'd':
                pass
            case 'e':
                return 0
            case _: 
                continue
    

if __name__ == '__main__':

    usr_interaction()
