# Sundial Modbus Server

This is a Modbus server, connected to a Sundial client.

## Mappings

Digital inputs on the server are mapped to plant IDs on Sundial

Reading a digital input, will get advice from the corresponding plant
in Sundial, and return the current recommendation to supply to grid.

## Requirements

You need Python 3.x and `pipenv`

## Preparing

- Navigate to the source folder
- Run `pipenv shell`
- Run `pipenv install`

## Running

To run the server:

```
SUNDIAL_API_KEY=<my sundial API key> SUNDIAL_URL=https://api.sundial.energy SUNDIAL_MODBUS_PORT=<some port> python server.py
```

This repository also includes a test client. To run it:

```
SUNDIAL_PLANT_ID=5 SUNDIAL_MODBUS_PORT=<some port> python ./client.py
```
