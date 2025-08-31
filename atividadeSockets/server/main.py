from typing import Optional
import peewee
import datetime
import socket
import threading

import defines as d
from server.database import core as db_core

tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)


def handle_client(connection, addr):
    print("Got connection from", addr)
    with connection:
        while True:
            message_str = d.receive_message(connection)
            if message_str is None:
                print("Connection closed by client.")
                break
            try:
                response_msg_str = db_core.handle_request(message_str)
            except Exception as e:
                print(f"Error handling request: {e}")
                response_msg_str = d.create_message(
                    d.CommandResponse.ERROR,
                    d.Table.NONE,
                    payload_dict={"error": str(e)},
                )

            if response_msg_str:
                print(f"msg string: {response_msg_str}")
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


def run_server():
    try:
        tcp.bind((d.HOST, d.PORT))
        print(f"Server listening on {d.HOST}:{d.PORT}")
        tcp.listen()

        while True:
            try:
                connection, addr = tcp.accept()
                client_thread = threading.Thread(
                    target=handle_client, args=(connection, addr), daemon=True
                )
                client_thread.start()
            except Exception as e:
                print(f"Error accepting connection: {e}")

    except KeyboardInterrupt:
        print("\nServer shutting down...")

    finally:
        tcp.close()
        print("Socket closed.")


if __name__ == "__main__":
    db_core.initialize_db()
    run_server()
