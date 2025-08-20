from typing import Optional
import peewee
import sys, os
import datetime
import socket

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
sys.path.insert(0, project_root)

from atividadeSockets import defines as d
from atividadeSockets import schema

db = peewee.SqliteDatabase(os.path.join(current_dir, "database.db"))


def initialize_db() -> None:
    db.bind([schema.Directors, schema.Movies])
    db.connect()
    db.create_tables([schema.Directors, schema.Movies], safe=True)
    print("Database initialized with Director and Movie tables.")


def handle_create_director(payload: dict) -> Optional[int]:
    if payload.get("name") is None:
        return None

    new_director = schema.Directors.create(name=payload["name"])

    print(f"Created new director with ID {new_director.id}")
    return new_director.id


def handle_request(message_str: str) -> Optional[d.Message]:
    try:
        message = d.parse_message(message_str)
    except Exception as e:
        print(f"Error parsing message: {e}")
        return None

    if message.command == d.Command.CREATE:
        print(
            f"Handling CREATE command for {message.table.value} with payload: {message.payload}"
        )
        match message.table:
            case d.Table.DIRECTOR:
                return handle_create_director(message.payload)
    return None
