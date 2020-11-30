#!/usr/bin/env python
# scripts/examples/simple_tcp_server.py
from __future__ import print_function
import logging
from socketserver import TCPServer
from collections import defaultdict
from datetime import datetime
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

# create an instance of the API class
api_instance = sundial.AdviceControllerApi(
    sundial.ApiClient(configuration, 'Authorization', f'Bearer {api_key}'))

# Add stream handler to logger 'uModbus'.
log_to_stream(level=logging.DEBUG)

# Enable values to be signed (default is False).
conf.SIGNED_VALUES = True

TCPServer.allow_reuse_address = True
app = get_server(TCPServer, ('localhost', port), RequestHandler)


@app.route(slave_ids=[1], function_codes=[2], addresses=list(range(10)))
def read_sundial_advice(slave_id, function_code, address):
    """"Return current Sundial generation recommendation"""
    now = datetime.utcnow().replace(tzinfo=pytz.utc)
    try:
        print(f'Read advice from plant {address}')
        api_response = api_instance.advice_controller_get_plant_advice(address)
        current_recommendations = filter(
            lambda r: r.start_at <= now and r.end_at >= now, api_response.recommendations)
        return list(current_recommendations)[0].supply_to_grid
    except ApiException as e:
        print("Exception when calling AdviceControllerApi->advice_controller_get_plant_advice: %s\n" % e)
    # Supply by default
    return True


if __name__ == '__main__':
    try:
        app.serve_forever()
    finally:
        app.shutdown()
        app.server_close()
