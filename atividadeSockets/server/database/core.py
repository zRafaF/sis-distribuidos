from typing import Optional
import peewee
import os
import datetime
import socket
import server.database.director as db_director
import server.database.movie as db_movie

current_dir = os.path.dirname(os.path.abspath(__file__))

import defines as d
import schema

db = peewee.SqliteDatabase(os.path.join(current_dir, "database.db"))


def initialize_db() -> None:
    db.bind([schema.Directors, schema.Movies])
    db.connect()
    db.create_tables([schema.Directors, schema.Movies], safe=True)
    print("Database initialized with Director and Movie tables.")


def handle_request(message_str: str) -> Optional[str]:
    """
    Handle incoming messages from clients.

    Will return a response message string if the request is valid.
    Else will return None
    """

    try:
        message = d.parse_message(message_str)
    except Exception as e:
        print(f"Error parsing message: {e}")
        return None

    if message.command == d.CommandResponse.CREATE:
        print(
            f"Handling CREATE command for {message.table.value} with payload: {message.payload}"
        )
        match message.table:
            case d.Table.DIRECTOR:
                return db_director.handle_create_director(message.payload)
            case d.Table.MOVIE:
                return db_movie.handle_create_movie(message.payload)

    if message.command == d.CommandResponse.READ:
        print(
            f"Handling READ command for {message.table.value} with payload: {message.payload}"
        )
        match message.table:
            case d.Table.DIRECTOR:
                return db_director.handle_read_director(message.payload)
            case d.Table.MOVIE:
                return db_movie.handle_read_movie(message.payload)

    return None
