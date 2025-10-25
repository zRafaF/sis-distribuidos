from pydantic import BaseModel, Field, PositiveInt


class Director(BaseModel):
    name: str = Field(..., example="Christopher Nolan")
    age: PositiveInt = Field(..., example=50)
