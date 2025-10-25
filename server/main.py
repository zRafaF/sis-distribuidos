import sys, os

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from query_schema import (
    Director,
    Movie,
    StandardMessage,
    DirectorListResponse,
    DirectorResponse,
    MovieResponse,
    MovieListResponse,
)
import db_core
from fastapi import FastAPI, HTTPException
from playhouse.shortcuts import model_to_dict
from pydantic import PositiveInt

app = FastAPI(
    title="Movie Director API",
    description="API para gerenciar diretores e seus filmes.",
    version="1.0.0",
    contact={
        "name": "Fábio Bays de Araujo & Rafael Farias Meneses",
    },
)
db_core.initialize_db()


@app.get(
    "/",
    summary="Endpoint Raiz",
    description="Retorna uma mensagem de boas-vindas da API.",
    tags=["Geral"],
    response_model=StandardMessage,
)
async def root():
    return {"message": "Bem-vindo à API de Filmes e Diretores!"}


# --- Endpoints de Diretores ---


@app.get(
    "/directors/{director_id}",
    summary="Buscar um diretor por ID",
    description="Obtém os detalhes de um diretor específico com base no seu ID.",
    tags=["Diretores"],
    responses={404: {"description": "Diretor não encontrado"}},
    response_model=DirectorResponse,
)
async def get_director(director_id: int) -> dict:
    try:
        director = db_core.Directors.get_by_id(director_id)
        return {
            "message": "Diretor recuperado com sucesso.",
            "data": model_to_dict(director),
        }
    except db_core.Directors.DoesNotExist:
        raise HTTPException(status_code=404, detail="Diretor não encontrado.")


@app.get(
    "/directors/",
    summary="Listar todos os diretores",
    description="Retorna uma lista paginada de diretores. Permite filtrar por nome (parcial) e idade (exata).",
    tags=["Diretores"],
    response_model=DirectorListResponse,
)
async def get_all_directors(
    page: PositiveInt = 1,
    size: PositiveInt = 10,
    name: str | None = None,
    age: PositiveInt | None = None,
) -> dict:
    query = db_core.Directors.select()
    if name:
        query = query.where(db_core.Directors.name.contains(name))
    if age:
        query = query.where(db_core.Directors.age == age)
    directors = query.paginate(page, size)
    return {
        "message": "Diretores recuperados com sucesso.",
        "data": [model_to_dict(director) for director in directors],
    }


@app.post(
    "/directors/",
    summary="Criar um novo diretor",
    description="Adiciona um novo diretor ao banco de dados.",
    tags=["Diretores"],
    status_code=201,
    response_model=DirectorResponse,
)
def create_director(director: Director) -> dict:
    new_director = db_core.Directors.create(name=director.name, age=director.age)
    new_director.save()
    return {
        "message": "Diretor criado com sucesso.",
        "data": model_to_dict(new_director),
    }


@app.delete(
    "/directors/{director_id}",
    summary="Deletar um diretor por ID",
    description="Remove um diretor e todos os seus filmes associados (exclusão em cascata) do banco de dados.",
    tags=["Diretores"],
    responses={404: {"description": "Diretor não encontrado"}},
    response_model=StandardMessage,
)
async def delete_director(director_id: int) -> dict:
    try:
        director = db_core.Directors.get_by_id(director_id)
        director.delete_instance(recursive=True)  # Exclusão em cascata
        return {"message": "Diretor e filmes associados deletados com sucesso."}
    except db_core.Directors.DoesNotExist:
        raise HTTPException(status_code=404, detail="Diretor não encontrado.")


@app.put(
    "/directors/{director_id}",
    summary="Atualizar um diretor por ID",
    description="Atualiza os dados (nome e idade) de um diretor existente.",
    tags=["Diretores"],
    responses={404: {"description": "Diretor não encontrado"}},
    response_model=DirectorResponse,
)
async def update_director(director_id: int, director: Director) -> dict:
    try:
        existing_director = db_core.Directors.get_by_id(director_id)
        existing_director.name = director.name
        existing_director.age = director.age
        existing_director.save()
        return {
            "message": "Diretor atualizado com sucesso.",
            "data": model_to_dict(existing_director),
        }
    except db_core.Directors.DoesNotExist:
        raise HTTPException(status_code=404, detail="Diretor não encontrado.")


# --- Endpoints de Filmes ---


@app.get(
    "/movies/{movie_id}",
    summary="Buscar um filme por ID",
    description="Obtém os detalhes de um filme específico com base no seu ID.",
    tags=["Filmes"],
    responses={404: {"description": "Filme não encontrado"}},
    response_model=MovieResponse,
)
async def get_movie(movie_id: int) -> dict:
    try:
        movie = db_core.Movies.get_by_id(movie_id)
        return {
            "message": "Filme recuperado com sucesso.",
            "data": model_to_dict(movie),
        }
    except db_core.Movies.DoesNotExist:
        raise HTTPException(status_code=404, detail="Filme não encontrado.")


@app.get(
    "/movies/",
    summary="Listar todos os filmes",
    description="Retorna uma lista paginada de todos os filmes no banco de dados.",
    tags=["Filmes"],
    response_model=MovieListResponse,
)
async def get_all_movies(page: PositiveInt = 1, size: PositiveInt = 10) -> dict:
    movies = db_core.Movies.select().paginate(page, size)
    return {
        "message": "Filmes recuperados com sucesso.",
        "data": [model_to_dict(movie) for movie in movies],
    }


@app.post(
    "/movies/",
    summary="Criar um novo filme",
    description="Adiciona um novo filme ao banco de dados, associando-o a um diretor existente.",
    tags=["Filmes"],
    status_code=201,
    responses={404: {"description": "Diretor (associado) não encontrado"}},
    response_model=MovieResponse,
)
def create_movie(movie: Movie) -> dict:
    try:
        director = db_core.Directors.get_by_id(movie.director_id)
    except db_core.Directors.DoesNotExist:
        raise HTTPException(
            status_code=404, detail="Diretor (associado) não encontrado."
        )

    new_movie = db_core.Movies.create(
        title=movie.title,
        director_id=director,
        rating=movie.rating,
        duration_min=movie.duration_min,
    )
    new_movie.save()
    return {
        "message": "Filme criado com sucesso.",
        "data": model_to_dict(new_movie),
    }


@app.delete(
    "/movies/{movie_id}",
    summary="Deletar um filme por ID",
    description="Remove um filme do banco de dados. Se este for o último filme do diretor, o diretor também será removido.",
    tags=["Filmes"],
    responses={404: {"description": "Filme não encontrado"}},
    response_model=StandardMessage,
)
async def delete_movie(movie_id: int) -> dict:
    try:
        movie = db_core.Movies.get_by_id(movie_id)
        director = movie.director_id
        movie.delete_instance()

        # Verifica se o diretor ficou sem filmes
        if director.movies.count() == 0:
            director.delete_instance()
            return {"message": "Filme e diretor (órfão) deletados com sucesso."}

        return {"message": "Filme deletado com sucesso."}
    except db_core.Movies.DoesNotExist:
        raise HTTPException(status_code=404, detail="Filme não encontrado.")


@app.put(
    "/movies/{movie_id}",
    summary="Atualizar um filme por ID",
    description="Atualiza os dados de um filme existente.",
    tags=["Filmes"],
    responses={404: {"description": "Filme não encontrado"}},
    response_model=MovieResponse,
)
async def update_movie(movie_id: int, movie: Movie) -> dict:
    try:
        # Validação extra: verificar se o novo ID de diretor existe
        try:
            db_core.Directors.get_by_id(movie.director_id)
        except db_core.Directors.DoesNotExist:
            raise HTTPException(
                status_code=404, detail="Diretor (associado) não encontrado."
            )

        existing_movie = db_core.Movies.get_by_id(movie_id)
        existing_movie.title = movie.title
        existing_movie.director_id = movie.director_id
        existing_movie.rating = movie.rating
        existing_movie.duration_min = movie.duration_min
        existing_movie.save()

        return {
            "message": "Filme atualizado com sucesso.",
            "data": model_to_dict(existing_movie),
        }
    except db_core.Movies.DoesNotExist:
        raise HTTPException(status_code=404, detail="Filme não encontrado.")
