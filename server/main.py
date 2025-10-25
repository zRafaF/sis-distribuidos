import sys, os

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from query_schema import Director, Movie
import db_core
from fastapi import FastAPI, HTTPException
from playhouse.shortcuts import model_to_dict
from pydantic import PositiveInt

app = FastAPI()
db_core.initialize_db()


@app.get("/")
async def root():
    return {"message": "Root"}

# Get one director by ID
@app.get("/directors/{director_id}")
async def get_director(director_id: int) -> dict:
    try:
        director = db_core.Directors.get_by_id(director_id)
        return {
            "message": "Director retrieved successfully.",
            "data": model_to_dict(director),
        }
    except db_core.Directors.DoesNotExist:
        raise HTTPException(status_code=404, detail="Director not found.")

# Get directors by name
@app.get("/directors/name/{name}")
async def get_directors_by_name(name: str, page: PositiveInt = 1,
                                size: PositiveInt = 10) -> dict:
    directors = db_core.Directors.select().where(
        db_core.Directors.name.contains(name)
    ).paginate(page, size)
    return {
        "message": "Directors retrieved successfully.",
        "data": [model_to_dict(director) for director in directors],
    }

# Get all directors
@app.get("/directors/")
async def get_all_directors(page: PositiveInt = 1, size: PositiveInt = 10) -> dict:
    directors = db_core.Directors.select().paginate(page, size)
    return {
        "message": "Directors retrieved successfully.",
        "data": [model_to_dict(director) for director in directors],
    }

@app.post("/directors/")
def create_director(director: Director) -> dict:
    new_director = db_core.Directors.create(name=director.name, age=director.age)
    new_director.save()
    return {
        "message": "Director created successfully.",
        "data": model_to_dict(new_director),
    }



# Delete a director by ID (with cascade delete for movies)
@app.delete("/directors/{director_id}")
async def delete_director(director_id: int) -> dict:
    try:
        director = db_core.Directors.get_by_id(director_id)
        director.delete_instance(recursive=True)  # Cascade delete movies
        return {"message": "Director and associated movies deleted successfully."}
    except db_core.Directors.DoesNotExist:
        raise HTTPException(status_code=404, detail="Director not found.")


# Update a director by ID
@app.put("/directors/{director_id}")
async def update_director(director_id: int, director: Director) -> dict:
    try:
        existing_director = db_core.Directors.get_by_id(director_id)
        existing_director.name = director.name
        existing_director.age = director.age
        existing_director.save()
        return {
            "message": "Director updated successfully.",
            "data": model_to_dict(existing_director),
        }
    except db_core.Directors.DoesNotExist:
        raise HTTPException(status_code=404, detail="Director not found.")
    

# Get one movie by ID
@app.get("/movies/{movie_id}")
async def get_movie(movie_id: int) -> dict:
    try:
        movie = db_core.Movies.get_by_id(movie_id)
        return {
            "message": "Movie retrieved successfully.",
            "data": model_to_dict(movie),
        }
    except db_core.Movies.DoesNotExist:
        raise HTTPException(status_code=404, detail="Movie not found.")

# Get all movies
@app.get("/movies/")
async def get_all_movies(page: PositiveInt = 1, size: PositiveInt = 10) -> dict:
    movies = db_core.Movies.select().paginate(page, size)
    return {
        "message": "Movies retrieved successfully.",
        "data": [model_to_dict(movie) for movie in movies],
    }

# Create a new movie
@app.post("/movies/")
def create_movie(movie: Movie) -> dict:
    try:
        director = db_core.Directors.get_by_id(movie.director_id)
    except db_core.Directors.DoesNotExist:
        raise HTTPException(status_code=404, detail="Director not found.")
    new_movie = db_core.Movies.create(
        title=movie.title,
        director_id=director,
        rating=movie.rating,
        duration_min=movie.duration_min
    )
    new_movie.save()
    return {
        "message": "Movie created successfully.",
        "data": model_to_dict(new_movie),
    }

# Delete a movie by ID (will delete the director if no movies left)
@app.delete("/movies/{movie_id}")
async def delete_movie(movie_id: int) -> dict:
    try:
        movie = db_core.Movies.get_by_id(movie_id)
        director = movie.director_id
        movie.delete_instance()
        # Check if the director has any other movies
        if director.movies.count() == 0:
            director.delete_instance()
            return {
                "message": "Movie and director deleted successfully."
            }
        return {"message": "Movie deleted successfully."}
    except db_core.Movies.DoesNotExist:
        raise HTTPException(status_code=404, detail="Movie not found.")
    
    
# Update a movie by ID
@app.put("/movies/{movie_id}")
async def update_movie(movie_id: int, movie: Movie) -> dict:
    try:
        existing_movie = db_core.Movies.get_by_id(movie_id)
        existing_movie.title = movie.title
        existing_movie.director_id = movie.director_id
        existing_movie.rating = movie.rating
        existing_movie.duration_min = movie.duration_min
        existing_movie.save()
        return {
            "message": "Movie updated successfully.",
            "data": model_to_dict(existing_movie),
        }
    except db_core.Movies.DoesNotExist:
        raise HTTPException(status_code=404, detail="Movie not found.")