from typing import List
from pydantic import BaseModel, Field, PositiveInt, NonNegativeFloat


class Director(BaseModel):
    name: str = Field(..., example="Christopher Nolan")
    age: PositiveInt = Field(..., example=50)


class Movie(BaseModel):
    title: str = Field(..., example="Inception")
    director_id: PositiveInt = Field(..., example=1)
    rating: NonNegativeFloat = Field(0.0, example=8.8)
    duration_min: PositiveInt = Field(0, example=148)
    genre: str = Field("Unknown", example="Sci-Fi")

# 2. Modelos de Resposta (a estrutura JSON)
class StandardMessage(BaseModel):
    message: str

class DirectorResponse(StandardMessage):
    data: Director

class DirectorListResponse(StandardMessage):
    data: List[Director]

class MovieResponse(StandardMessage):
    data: Movie

class MovieListResponse(StandardMessage):
    data: List[Movie]