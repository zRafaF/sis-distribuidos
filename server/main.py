import sys, os

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from query_schema import Director
import db_core
from fastapi import FastAPI
from playhouse.shortcuts import model_to_dict
from pydantic import PositiveInt

app = FastAPI()
db_core.initialize_db()


@app.get("/")
async def root():
    return {"message": "Root"}


@app.post("/directors/")
def create_director(director: Director) -> dict:
    new_director = db_core.Directors.create(name=director.name, age=director.age)
    new_director.save()
    return {
        "message": "Director created successfully.",
        "data": model_to_dict(new_director),
    }


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
        return {"message": "Director not found."}


# Get all directors
@app.get("/directors/")
async def get_all_directors(page: PositiveInt = 1, size: PositiveInt = 10) -> dict:
    directors = db_core.Directors.select().paginate(page, size)
    return {
        "message": "Directors retrieved successfully.",
        "data": [model_to_dict(director) for director in directors],
    }

# Delete a director by ID
@app.delete("/directors/{director_id}")
async def delete_director(director_id: int) -> dict:
    try:
        director = db_core.Directors.get_by_id(director_id)
        director.delete_instance()
        return {"message": "Director deleted successfully."}
    except db_core.Directors.DoesNotExist:
        return {"message": "Director not found."}


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
        return {"message": "Director not found."}