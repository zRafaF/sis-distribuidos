from typing import Optional
import peewee
import sys, os
import datetime
import socket

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
sys.path.insert(0, project_root)

from atividadeSockets import defines as d
from atividadeSockets.server.database import core as db_core


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

                        db_core.handle_request(message_str)
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
