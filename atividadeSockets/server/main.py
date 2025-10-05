from typing import Optional
import peewee
import datetime
import threading

from server.database import core as db_core
from server.database import director
from server.database import movie

import Movie
import defines as d

class CRUD():

    def create_movie(mov : Movie.Movie):
         
    def read_movie(?):
        pass
    def update_movie(?):
        pass
    def delete_movie(?):
        pass


if __name__ == "__main__":
    db_core.initialize_db()
   
    print('primeira leitura: \n')
    l = movie.handle_read_movie(4)
 
    if not l[0]: 
        for mov in l[1]:
            dname = director.handle_read_director(mov.director_id)[1][0]
            print(f"{mov.title}\n{dname}\n{mov.length_minutes}\n" 
                    f"{mov.gender}\n{mov.rating}")
            print("*"*10)
   
