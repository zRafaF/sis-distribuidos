from typing import Optional
import peewee
import datetime
import socket

import defines as d
from server.database import core as db_core


tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)


def run_server():
    try:
        tcp.bind((d.HOST, d.PORT))
        print(f"Server listening on {d.HOST}:{d.PORT}")
        tcp.listen()

        while True:
            try:
                connection, addr = tcp.accept()

                with connection:
                    print("Got connection from", addr)
                    while True:
                        message_str = d.receive_message(connection)

                        if message_str is None:
                            print("Connection closed by client.")
                            break

                        response_msg_str = db_core.handle_request(message_str)

                        if response_msg_str:
                            d.send_message(connection, response_msg_str)

                        else:
                            d.send_message(
                                connection,
                                d.create_message(
                                    d.CommandResponse.ERROR,
                                    d.Table.NONE,
                                    payload_dict={"error": "Invalid request"},
                                ),
                            )

            finally:
                # Close client socket after handling
                if connection:
                    connection.close()

    except KeyboardInterrupt:
        print("\nServer shutting down...")

    finally:
        tcp.close()
        print("Socket closed.")


if __name__ == "__main__":
    db_core.initialize_db()
    run_server()
