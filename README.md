# Sundial Modbus Server

This is a Modbus server, connected to a Sundial client.

## Mappings

The server is configured to retrieve Sundial advice for a single plant.

Incoming recommendations are mapped to different Modbus addresses:

### Discrete Inputs

| Address | Value                                     |
| ------- | ----------------------------------------- |
| 0       | “supply to grid” flag of recommendation 0 |
| 1       | “supply to grid” flag of recommendation 1 |
| 2       | “supply to grid” flag of recommendation 2 |
| 3       | “supply to grid” flag of recommendation 3 |
| 4       | “supply to grid” flag of recommendation 4 |

| Address | Value                  |
| ------- | ---------------------- |
| 10      | Recommendation 0 valid |
| 11      | Recommendation 1 valid |
| 12      | Recommendation 2 valid |
| 13      | Recommendation 3 valid |
| 14      | Recommendation 4 valid |

### Input Registers

| Address | Value                                                            |
| ------- | ---------------------------------------------------------------- |
| 0       | Least significant 15 bits of start timestamp of recommendation 0 |
| 1       | Least significant 15 bits of start timestamp of recommendation 1 |
| 2       | Least significant 15 bits of start timestamp of recommendation 2 |
| 3       | Least significant 15 bits of start timestamp of recommendation 3 |
| 4       | Least significant 15 bits of start timestamp of recommendation 4 |

| Address | Value                                                          |
| ------- | -------------------------------------------------------------- |
| 0       | Least significant 15 bits of end timestamp of recommendation 0 |
| 1       | Least significant 15 bits of end timestamp of recommendation 1 |
| 2       | Least significant 15 bits of end timestamp of recommendation 2 |
| 3       | Least significant 15 bits of end timestamp of recommendation 3 |
| 4       | Least significant 15 bits of end timestamp of recommendation 4 |

| Address | Value                         |
| ------- | ----------------------------- |
| 20      | LGC price of recommendation 0 |
| 21      | LGC price of recommendation 1 |
| 22      | LGC price of recommendation 2 |
| 23      | LGC price of recommendation 3 |
| 24      | LGC price of recommendation 4 |

| Address | Value                          |
| ------- | ------------------------------ |
| 30      | Spot price of recommendation 0 |
| 31      | Spot price of recommendation 1 |
| 32      | Spot price of recommendation 2 |
| 33      | Spot price of recommendation 3 |
| 34      | Spot price of recommendation 4 |

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
