#!/usr/bin/env python
# scripts/examples/simple_tcp_server.py
from __future__ import print_function
import logging
from socketserver import TCPServer, ThreadingMixIn
from collections import defaultdict
from cachetools import cached, TTLCache
from datetime import datetime
import dateutil.parser
from threading import Lock
import time
import os
import sundial
import pytz
from sundial.rest import ApiException
from sundial.configuration import Configuration
from pprint import pprint

from umodbus import conf
from umodbus.server.tcp import RequestHandler, get_server
from umodbus.utils import log_to_stream

utc = pytz.UTC

configuration = Configuration()
configuration.host = os.environ.get('SUNDIAL_URL')
api_key = os.environ.get('SUNDIAL_API_KEY')
port = int(os.environ.get('SUNDIAL_MODBUS_PORT'))
SLAVE_ID = 1
PLANT_ID = 5

# create an instance of the API class
api_instance = sundial.AdviceControllerApi(
    sundial.ApiClient(configuration, 'Authorization', f'Bearer {api_key}'))

# Add stream handler to logger 'uModbus'.
log_to_stream(level=logging.DEBUG)

# Enable values to be signed (default is False).
conf.SIGNED_VALUES = True


class ThreadingServer(ThreadingMixIn, TCPServer):
    pass


ThreadingServer.allow_reuse_address = True
app = get_server(ThreadingServer, ('', port), RequestHandler)
lock = Lock()


@cached(cache=TTLCache(maxsize=1024, ttl=600), lock=lock)
def get_plant_recommendations():
    datetime.utcnow().replace(tzinfo=pytz.utc)
    api_response = api_instance.advice_controller_get_plant_advice(
        PLANT_ID)
    return api_response.recommendations


@app.route(slave_ids=[SLAVE_ID], function_codes=[2], addresses=list(range(5)))
def read_sundial_supply_to_grid(slave_id, function_code, address):
    """"Return Sundial generation recommendation supply_to_grid"""
    recommendation_index = address
    try:
        recommendations = get_plant_recommendations()
        return recommendations[recommendation_index].supply_to_grid
    except IndexError as e:
        print("Exception when getting current supply_to_grid %s\n" % e)
    # False by default
    return False


@app.route(slave_ids=[SLAVE_ID], function_codes=[2], addresses=list(range(10, 15)))
def read_sundial_recommendation_valid(slave_id, function_code, address):
    """"Return Sundial generation recommendation validity"""
    recommendation_index = address - 10
    recommendations = get_plant_recommendations()
    return len(recommendations) > recommendation_index


@app.route(slave_ids=[SLAVE_ID], function_codes=[4], addresses=list(range(5)))
def read_sundial_start_timestamp(slave_id, function_code, address):
    """"Return Sundial recommendation start timestamp"""
    recommendation_index = address
    try:
        recommendations = get_plant_recommendations()
        recommendation = recommendations[recommendation_index]
        start_time = int(recommendation.start_at.timestamp())
        return start_time & 0x7fff
    except IndexError as e:
        print("Exception when getting start timestamp %s\n" % e)
    return 0


@app.route(slave_ids=[SLAVE_ID], function_codes=[4], addresses=list(range(10, 15)))
def read_sundial_end_timestamp(slave_id, function_code, address):
    """"Return Sundial recommendation end timestamp"""
    recommendation_index = address - 10
    try:
        recommendations = get_plant_recommendations()
        recommendation = recommendations[recommendation_index]
        end_time = int(recommendation.end_at.timestamp())
        return end_time & 0x7fff
    except IndexError as e:
        print("Exception when getting end timestamp %s\n" % e)
    return 0


@app.route(slave_ids=[SLAVE_ID], function_codes=[4], addresses=list(range(20, 25)))
def read_sundial_lgc_price(slave_id, function_code, address):
    """"Return Sundial recommendation lgc price"""
    recommendation_index = address - 20
    try:
        recommendations = get_plant_recommendations()
        recommendation = recommendations[recommendation_index]
        ret = int(recommendation.lgc_price * 100)
        print(f'Returning LGC price {ret}')
        return ret
    except IndexError as e:
        print("Exception when getting lgc_price %s\n" % e)
    # Zero by default
    return 0


@app.route(slave_ids=[SLAVE_ID], function_codes=[4], addresses=list(range(30, 35)))
def read_sundial_spot_price(slave_id, function_code, address):
    """"Return Sundial recommendation spot price"""
    recommendation_index = address - 30
    try:
        recommendations = get_plant_recommendations()
        recommendation = recommendations[recommendation_index]
        ret = int(recommendation.energy_price * 100)
        print(f'Returning spot price {ret}')
        return ret
    except IndexError as e:
        print("Exception when getting spot_price %s\n" % e)
    # Zero by default
    return 0


if __name__ == '__main__':
    try:
        app.serve_forever()
    finally:
        app.shutdown()
        app.server_close()
