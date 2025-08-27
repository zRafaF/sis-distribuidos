import ast
from enum import Enum
from dataclasses import dataclass
import socket
from typing import Optional, Dict, Any
from urllib.parse import quote, unquote

# Configs
HOST: str = "127.0.0.1"
PORT: int = 60019
BUFFER_SIZE: int = 1024
MSG_SIZE_HEADER: int = 8


# Definição do protocolo
class CommandResponse(str, Enum):
    CREATE = "C"
    READ = "R"
    UPDATE = "U"
    DELETE = "D"

    SUCCESS = "SUCCESS"
    ERROR = "ERROR"


class Table(str, Enum):
    DIRECTOR = "DIR"
    MOVIE = "MOV"
    NONE = "NONE"


# Estrutura da mensagem
MESSAGE_DELIMITER: str = "@"
PAYLOAD_DELIMITER: str = "|"
PAYLOAD_ASSIGNER: str = "="
WILDCARD_ID: int = -1


# Data Structure
@dataclass
class Message:
    command: CommandResponse
    table: Table
    record_id: int
    payload: Dict[str, Any]


# Helpers
def format_payload(data: Dict[str, Any]) -> str:
    """
    Formats a dictionary into a 'key=value|key=value' string.
    Each value is converted to its standard string representation.

    WARNING: This protocol is not robust. Keys or string values containing
    '=' or '|' will break the parsing.
    """
    if not isinstance(data, dict) or not data:
        return ""

    # For a list of dicts, str() will create a string like "[{'id': 1}, {'id': 2}]"
    parts = [f"{str(key)}{PAYLOAD_ASSIGNER}{str(value)}" for key, value in data.items()]
    return PAYLOAD_DELIMITER.join(parts)


def parse_payload(payload_str: str) -> Dict[str, Any]:
    """
    Parses a 'key=value|key=value' string into a dictionary.
    It safely evaluates values from strings back into Python objects
    (e.g., lists, dicts, numbers) where possible.
    """
    if not payload_str:
        return {}

    result: Dict[str, Any] = {}
    try:
        for pair in payload_str.split(PAYLOAD_DELIMITER):
            if PAYLOAD_ASSIGNER not in pair:
                continue

            key, value_str = pair.split(PAYLOAD_ASSIGNER, 1)

            try:
                # ast.literal_eval safely parses string representations of
                # Python data structures like lists, dicts, numbers, and booleans.
                result[key] = ast.literal_eval(value_str)
            except (ValueError, SyntaxError):
                # If the string is not a valid literal (e.g., a simple
                # message like "SUCCESS"), keep it as a string.
                result[key] = value_str
        return result
    except ValueError:
        return {}


def create_message(
    command_response: CommandResponse,
    table: Table,
    record_id: int = WILDCARD_ID,
    payload_dict: Optional[Dict[str, Any]] = None,
) -> str:
    payload_str = format_payload(payload_dict) if payload_dict else ""
    return MESSAGE_DELIMITER.join(
        [command_response.value, table.value, str(record_id), payload_str]
    )


def parse_message(message_str: str) -> Optional[Message]:
    try:
        parts = message_str.split(MESSAGE_DELIMITER, 3)
        if len(parts) != 4:
            return None

        cmd_response_str, table_str, record_id_str, payload_str = parts

        command = CommandResponse(cmd_response_str)

        table = Table(table_str)
        record_id = int(record_id_str)
        payload = parse_payload(payload_str)

        return Message(
            command=command, table=table, record_id=record_id, payload=payload
        )
    except (ValueError, KeyError):
        return None


def send_message(sock: socket.socket, message: str) -> None:
    encoded_message = message.encode("utf-8")

    header = len(encoded_message).to_bytes(MSG_SIZE_HEADER, "big")
    sock.sendall(header + encoded_message)


def receive_message(sock: socket.socket) -> Optional[str]:
    try:
        # Lê o header e tenta encontrar o tamanho da mensagem
        header = sock.recv(MSG_SIZE_HEADER)
        if not header:
            return None
        msg_len = int.from_bytes(header, "big")

        chunks = []
        bytes_received = 0
        while bytes_received < msg_len:
            chunk = sock.recv(min(BUFFER_SIZE, msg_len - bytes_received))
            if not chunk:
                raise RuntimeError("Socket connection closed prematurely.")
            chunks.append(chunk)
            bytes_received += len(chunk)

        return b"".join(chunks).decode("utf-8")
    except Exception as e:
        print(f"Error receiving message: {e}")
        return None
