#!/usr/bin/env python
# scripts/examples/simple_tcp_client.py
import socket
import os

from umodbus import conf
from umodbus.client import tcp

# Enable values to be signed (default is False).
conf.SIGNED_VALUES = True

plant_id = int(os.environ.get('SUNDIAL_PLANT_ID'))
port = int(os.environ.get('SUNDIAL_MODBUS_PORT'))

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('localhost', port))

# Returns a message or Application Data Unit (ADU) specific for doing
# Modbus TCP/IP.
message = tcp.read_discrete_inputs(
    slave_id=1, starting_address=plant_id, quantity=1)

# Response depends on Modbus function code. This particular returns the
# amount of coils written, in this case it is.
response = tcp.send_message(message, sock)

print(response)

sock.close()
