import peewee
import Pyro5.server
import Pyro5.api
import Pyro5.core

from server.database import core as db_core
from server.database import director
from server.database import movie

import Movie
import defines as d

@Pyro5.server.expose
class CRUD():

    def create_movie(self, mov : Movie.Movie):
        # Check if there is a director with his name
        result = director.handle_read_director_by_name(mov.director_name)
        if result[0] == d.ReturnCodes.ERROR.value:
            # Create director
            director.handle_create_director(mov.director_name)
            result = director.handle_read_director_by_name(mov.director_name)

        mov.director_id = result[1]['id']
        mov.director_name = result[1]['name']
        movie.handle_create_movie(mov)
        

        return d.ReturnCodes.SUCCESS

    def read_movie(self, movie_id : int):
        result = movie.handle_read_movie(movie_id)
        if result[0] == d.ReturnCodes.ERROR.value:
            return []

        movie_list = []
        for mov in result[1]:
            dir_read = director.handle_read_director_by_id(mov.director_id) 
            director_name = dir_read[1][0]['name']
            mov.director_name = director_name
            movie_list.append(mov)

        return movie_list 

    def update_movie(self, movie_id, upd_mov : Movie.Movie):
        return movie.handle_update_movie(movie_id, upd_mov)
    def delete_movie(self, movie_id):
        result = movie.handle_delete_movie(movie_id)
        if result[0] == d.ReturnCodes.ERROR:
            return []

        return result[1]

def main():
    db_core.initialize_db()
   
    daemon = Pyro5.server.Daemon()
    crud = CRUD()
    endereco = daemon.register(crud)

    Pyro5.api.register_class_to_dict(Movie.Movie, Movie.Movie_to_dict)
    Pyro5.api.register_dict_to_class("Movie.Movie", Movie.dict_to_Movie)

    ns = Pyro5.core.locate_ns()
    ns.register('FabioRafael', endereco)
    # To aid in wireshark packet capture
    #input('*-->')

    daemon.requestLoop()

if __name__ == "__main__":
    main()
