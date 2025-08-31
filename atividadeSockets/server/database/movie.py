from typing import Optional
import schema
import defines as d


def handle_create_movie(payload: dict) -> Optional[str]:
    if (
        all(
            (
                payload.get("title"),
                payload.get("director_id"),
                payload.get("rating"),
                payload.get("duration_min"),
                payload.get("gender"),
            )
        )
        is False
    ):
        return None

    new_movie = schema.Movies(
        title=payload["title"],
        director_id=payload["director_id"],
        rating=payload["rating"],
        duration_min=payload["duration_min"],
        gender=payload["gender"],
    )

    new_movie.save()

    print(f"Created new movie with ID {new_movie.id}")

    return d.create_message(
        d.CommandResponse.SUCCESS,
        d.Table.MOVIE,
        record_id=new_movie.id,
        payload_dict={
            "id": new_movie.id,
            "title": new_movie.title,
            "director_id": new_movie.director_id,
            "rating": new_movie.rating,
            "duration_min": new_movie.duration_min,
            "gender": new_movie.gender,
        },
    )


def handle_read_movie(record_id: int) -> Optional[str]:
    movie_id = record_id
    if movie_id == d.WILDCARD_ID:
        movies = schema.Movies.select()
    else:
        movies = schema.Movies.select().where(schema.Movies.id == movie_id)

    movies_list = [
        {
            "id": movie.id,
            "title": movie.title,
            "director_id": movie.director_id.id,
            "rating": movie.rating,
            "duration_min": movie.duration_min,
            "gender": movie.gender,
        }
        for movie in movies
    ]

    print(f"Read {len(movies_list)} movies from database.")

    payload_dict = {"movies": movies_list}

    return d.create_message(
        d.CommandResponse.SUCCESS,
        d.Table.MOVIE,
        record_id=d.WILDCARD_ID,
        payload_dict=payload_dict,
    )
