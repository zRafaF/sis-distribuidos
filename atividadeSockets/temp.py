import socket
from atividadeSockets import defines as d

s = socket.socket()         

# Define the port on which you want to connect 

# connect to the server on local computer 
s.connect((d.HOST, d.PORT)) 

# receive data from the server and decoding to get the string.


message = d.create_message(
    d.Command.CREATE,
    d.Table.DIRECTOR,
    record_id=d.WILDCARD_ID,
    payload_dict={
        "name": "João"
    }
)

d.send_message(s, message)

# close the connection 
s.close()