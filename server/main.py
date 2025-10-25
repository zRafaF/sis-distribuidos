import sys, os

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from query_schema import Director
import db_core
from fastapi import FastAPI
from playhouse.shortcuts import model_to_dict

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
