#!/usr/bin/env python
# scripts/examples/simple_tcp_client.py
import socket
import os

from umodbus import conf
from umodbus.client import tcp

# Enable values to be signed (default is False).
conf.SIGNED_VALUES = True

port = int(os.environ.get('SUNDIAL_MODBUS_PORT'))
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('localhost', port))

message = tcp.read_discrete_inputs(
    slave_id=1, starting_address=0, quantity=5)
response = tcp.send_message(message, sock)

print(f'Supply to grid: {response}')

message = tcp.read_discrete_inputs(
    slave_id=1, starting_address=10, quantity=5)
response = tcp.send_message(message, sock)

print(f'Recommendation valid: {response}')

message = tcp.read_input_registers(
    slave_id=1, starting_address=0, quantity=5)
response = tcp.send_message(message, sock)

print(f'Start timestamp: {response}')

message = tcp.read_input_registers(
    slave_id=1, starting_address=10, quantity=5)
response = tcp.send_message(message, sock)

print(f'End timestamp: {response}')

message = tcp.read_input_registers(
    slave_id=1, starting_address=20, quantity=5)
response = tcp.send_message(message, sock)

print(f'LGC price: {response}')

message = tcp.read_input_registers(
    slave_id=1, starting_address=30, quantity=5)
response = tcp.send_message(message, sock)

print(f'Spot price: {response}')

sock.close()
