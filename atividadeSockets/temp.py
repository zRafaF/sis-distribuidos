import socket
import defines as d

s = socket.socket()

# Define the port on which you want to connect

# connect to the server on local computer
s.connect((d.HOST, d.PORT))

# receive data from the server and decoding to get the string.


message = d.create_message(
    d.CommandResponse.CREATE,
    d.Table.DIRECTOR,
    record_id=d.WILDCARD_ID,
    payload_dict={"name": "Jonas Brothers"},
)

d.send_message(s, message)


# Set a timeout of 1 second for the socket
s.settimeout(1.0)

# Get response from server
try:
    response = d.receive_message(s)
    if response:
        print("Received response from server:", response)
except socket.timeout:
    print("No response received within 1 second.")


parsed_msg = d.parse_message(response)

print(parsed_msg)

new_director_id = parsed_msg.record_id

print(f"New director ID: {new_director_id}")

# Inserts a new movie


message = d.create_message(
    d.CommandResponse.CREATE,
    d.Table.MOVIE,
    record_id=d.WILDCARD_ID,
    payload_dict={
        "title": "Inception",
        "director_id": new_director_id,
        "rating": 5,
        "gender": "Sci-Fi",
        "duration_min": 148,
    },
)

d.send_message(s, message)

try:
    response = d.receive_message(s)
    if response:
        print("Received response from server:", response)
except socket.timeout:
    print("No response received within 1 second.")


# Reads all directors


d.send_message(
    s,
    d.create_message(
        d.CommandResponse.READ,
        d.Table.DIRECTOR,
        record_id=d.WILDCARD_ID,
        payload_dict={},
    ),
)

try:
    response = d.receive_message(s)
    if response:
        print("Received response from server:", response)
except socket.timeout:
    print("No response received within 1 second.")


# close the connection
s.close()
