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


def handle_read_director(record_id: int) -> Optional[str]:
    director_id = record_id
    print(f"Reading director with ID: {director_id}")
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


def handle_delete_director(record_id: int) -> Optional[str]:
    print(f"Deleting director with ID: {record_id}")
    director = schema.Directors.get_by_id(record_id)
    if not director:
        return d.create_message(
            d.CommandResponse.ERROR,
            d.Table.DIRECTOR,
            record_id=record_id,
            payload_dict={"error": "Director not found"},
        )

    director.delete_instance()
    print(f"Deleted director with ID: {record_id}")

    return d.create_message(
        d.CommandResponse.SUCCESS,
        d.Table.DIRECTOR,
        record_id=record_id,
        payload_dict={"id": record_id},
    )


def handle_update_director(record_id: int, payload: dict) -> Optional[str]:
    if not payload.get("name"):
        return None

    director = schema.Directors.get_by_id(record_id)
    if not director:
        return d.create_message(
            d.CommandResponse.ERROR,
            d.Table.DIRECTOR,
            record_id=record_id,
            payload_dict={"error": "Director not found"},
        )

    director.name = payload["name"]
    director.save()

    return d.create_message(
        d.CommandResponse.SUCCESS,
        d.Table.DIRECTOR,
        record_id=record_id,
        payload_dict={
            "id": director.id,
            "name": director.name,
        },
    )
