from typing import Optional
import schema
import defines as d


def handle_create_director(payload: dict) -> Optional[str]:
    if all((payload.get("name"),)) is False:
        return None

    new_director = schema.Directors(
        name=payload["name"],
    )

    new_director.save()

    print(f"Created new director with ID {new_director.id}")

    return d.create_message(
        d.CommandResponse.SUCCESS,
        d.Table.DIRECTOR,
        record_id=new_director.id,
        payload_dict={
            "id": new_director.id,
            "name": new_director.name,
        },
    )


def handle_read_director(payload: dict) -> Optional[str]:
    director_id = payload.get("id", d.WILDCARD_ID)
    if director_id == d.WILDCARD_ID:
        directors = schema.Directors.select()
    else:
        directors = schema.Directors.select().where(schema.Directors.id == director_id)

    directors_list = [
        {
            "id": director.id,
            "name": director.name,
        }
        for director in directors
    ]

    print(f"Read {len(directors_list)} directors from database.")

    payload_dict = {"directors": directors_list}

    return d.create_message(
        d.CommandResponse.SUCCESS,
        d.Table.DIRECTOR,
        record_id=d.WILDCARD_ID,
        payload_dict=payload_dict,
    )
