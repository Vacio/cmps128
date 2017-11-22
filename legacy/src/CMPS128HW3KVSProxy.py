"""
    Author: Shane Dalton
    Created for UCSC undergrad course CMPS 128, Fall 2017
"""

from flask.views import MethodView
from flask import Response
from flask import request

import requests

import json

import logging

import os

"""
    Class that will redirect to the KVS. Refer to the README for specifications and functional guarantees.
"""
# TODO: Clean up this *entire* class/logic
class CMPS128HW3KVSProxy(MethodView):
    """
        MAINIP initialization
    """
    def __init__(self):
        self.mainIP = os.getenv('MAINIP')
        logging.debug("Value of MAINIP: " + str(self.mainIP))

    """
       GET request
       :return: HTTP response
    """
    def get(self, val):
        try:
            logging.debug("String: http://" + str(self.mainIP) + "/kv-store/" + val)
            # Forward GET request to the main instance
            r = requests.get(
                "http://" + str(self.mainIP) + "/kv-store/" + val,
                timeout=1
            )
            logging.info("Status code: " + str(r.status_code))
            logging.info("JSON: " + str(r.json()))

            # Replicate the response and return it
            return Response(
                json.dumps(r.json()),
                status=int(r.status_code),
                mimetype='application/json'
            )
        # Exception in the case that the request cannot be forwarded
        except Exception as e:
            logging.error(e)
            json_resp = json.dumps(
                {
                    'result': 'Error',
                    'msg': 'Server unavailable'
                }
            )
            return Response(
                json_resp,
                status=500,
                mimetype='application/json'
            )

    """
       DELETE request
       :return: HTTP response 
    """
    def delete(self, val):
        try:
            logging.debug("String: http://" + str(self.mainIP) + "/kv-store/" + val)
            # Forward DELETE request to the main instance
            r = requests.delete(
                "http://" + str(self.mainIP) + "/kv-store/" + val,
                timeout=1
            )
            logging.info("Status code: " + str(r.status_code))
            logging.info("JSON: " + str(r.json()))

            # Replicate the response and return it
            return Response(
                json.dumps(r.json()),
                status=int(r.status_code),
                mimetype='application/json'
            )
        # Exception in the case that the request cannot be forwarded
        except Exception as e:
            logging.error(e)
            json_resp = json.dumps(
                {
                    'result': 'Error',
                    'msg': 'Server unavailable'
                }
            )
            return Response(
                json_resp,
                status=500,
                mimetype='application/json'
            )

    """
        PUT request
        :return: HTTP response
    """
    def put(self, val):
        try:
            logging.debug("String: http://" + str(self.mainIP) + "/kv-store/" + val)
            # Forward PUT request to the main instance
            r = requests.put(
                "http://" + str(self.mainIP) + "/kv-store/" + val,
                data={'val': request.form['val']},
                timeout=1
            )
            logging.info("Status code: " + str(r.status_code))
            logging.info("JSON: " + str(r.json()))

            # Replicate the response and return it
            return Response(
                json.dumps(r.json()),
                status=int(r.status_code),
                mimetype='application/json'
            )
        # Exception in the case that the request cannot be forwarded
        except Exception as e:
            logging.error(e)
            json_resp = json.dumps(
                {
                    'result': 'Error',
                    'msg': 'Server unavailable'
                }
            )
            return Response(
                json_resp,
                status=500,
                mimetype='application/json'
            )