from typing import Optional
import schema
import defines as d
import Movie

def handle_create_movie(mov : Movie.Movie) -> d.ReturnCodes: 
    new_movie = schema.Movies(
        title=mov.title,
        director_id=mov.director_id,
        rating=mov.rating,
        duration_min=mov.length_minutes,
        gender=mov.gender
    )

    new_movie.save()

    print(f"Created new movie with ID {new_movie.id}")

    return d.ReturnCodes.SUCCESS.value

def handle_read_movie(record_id: int) -> list:
    print(f"Reading movie with ID: {record_id}")
    movie_id = record_id
    if movie_id == d.WILDCARD_ID:
        movies = schema.Movies.select()
    else:
        movies = schema.Movies.select().where(schema.Movies.id == movie_id)

    movies_list = [
        Movie.Movie( 
            movie.id,
            movie.director_id.id,
            movie.title,
            None,
            movie.duration_min,
            movie.gender,
            movie.rating,
        ) 
        for movie in movies
    ]

    if len(movies_list) == 0:
        print('Could not read movies from database')
        return [d.ReturnCodes.ERROR.value]

    print(f"Read {len(movies_list)} movies from database.")

    return [d.ReturnCodes.SUCCESS.value, movies_list]


def handle_delete_movie(record_id: int) -> d.ReturnCodes:
    print(f"Deleting movie with ID: {record_id}")
    movie = schema.Movies.get_by_id(record_id)
    if not movie:
        print(f"No movie with ID: {record_id}")
        return d.ReturnCodes.Error.value

    movie.delete_instance()
    print(f"Deleted movie with ID: {record_id}")

    return d.ReturnCodes.SUCCESS.value

def handle_update_movie(record_id: int, mov : Movie.Movie) -> d.ReturnCodes: 
    movie = schema.Movies.get_by_id(record_id)
    if not movie:
        print(f"No movie with ID: {record_id}")
        d.ReturnCodes.ERROR.value

    movie.director_id.id = mov.director_id 
    movie.title = mov.title
    movie.duration_min = mov.length_minutes
    movie.gender = mov.gender
    movie.rating = mov.rating

    movie.save()
    print(f"Updated movie with ID: {record_id}")
    
    return d.ReturnCodes.SUCCESS.value
