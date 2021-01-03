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

message = tcp.read_discrete_inputs(
    slave_id=1, starting_address=plant_id, quantity=1)
response = tcp.send_message(message, sock)

print(f'Supply to grid: {response}')

message = tcp.read_input_registers(
    slave_id=1, starting_address=plant_id, quantity=1)
response = tcp.send_message(message, sock)

print(f'LGC price: {response}')

message = tcp.read_input_registers(
    slave_id=1, starting_address=10 + plant_id, quantity=1)
response = tcp.send_message(message, sock)

print(f'Spot price: {response}')

sock.close()
