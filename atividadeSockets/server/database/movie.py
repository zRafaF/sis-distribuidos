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
        },
    )


def handle_read_movie(payload: dict) -> Optional[str]:
    movie_id = payload.get("id", d.WILDCARD_ID)
    if movie_id == d.WILDCARD_ID:
        movies = schema.Movies.select()
    else:
        movies = schema.Movies.select().where(schema.Movies.id == movie_id)

    movies_list = [
        {
            "id": movie.id,
            "title": movie.title,
            "director_id": movie.director_id,
            "rating": movie.rating,
            "duration_min": movie.duration_min,
        }
        for movie in movies
    ]

    return d.create_message(
        d.CommandResponse.SUCCESS,
        d.Table.MOVIE,
        record_id=d.WILDCARD_ID,
        payload_dict={"movies": movies_list},
    )
