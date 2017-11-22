"""
    Author: Cristian Gonzales
    Created for UCSC undergrad course CMPS 128, Fall 2017
"""

from flask.views import MethodView
from flask import request
from flask import Response

import time
import json
import logging
import re

import globals


"""
    Initialize an empty dictionary.
    :var globals.KVSDict: The global dictionary that will serve as our KVS
"""
        
"""
    Class that implements the KVS. Refer to the README for specifications and functional guarantees.
"""
class CMPS128HW3KVSReplica(MethodView):
    """
       GET request
       :return: HTTP response
    """
    def get(self, key):
        try:
            # If the requested argument is in the dictionary, then return a sucessful message with the last stored
            # value. If not, then return a 404 error message
            logging.info("Value of key: " + str(globals.KVSDict.get(key)))
            logging.info("Type: " + type(globals.KVSDict[key]))

            if key in globals.KVSDict:
                logging.debug(key)
                json_resp = json.dumps(
                    {
                        'result':'Success',
                        'value': globals.KVSDict[key]['val'],
                        'node_id': str(globals.localIPPort),
                        'causal_payload': globals.KVSDict[key]['clock'],
                        'timestamp': globals.KVSDict[key]['timestamp']
                    }
                )
                # Return the response
                return Response(
                    json_resp,
                    status=200,
                    mimetype='application/json'
                )
            else:
                json_resp = json.dumps(
                    {
                        'result': 'Error',
                        'msg': 'Key does not exist'
                    }
                )
                # Return the response
                return Response(
                    json_resp,
                    status=404,
                    mimetype='application/json'
                )
        except Exception as e:
            logging.error(e)
            json_resp = json.dumps(
                {
                    'result': 'Error',
                    'msg': str(e)
                }
            )
            # Return the response
            return Response(
                json_resp,
                status=404,
                mimetype='application/json'
            )

    """
        PUT request
        :return: HTTP response
    """
    def put(self, key):
        try:

            logging.debug(key)
            # Conditional to check if the input value is nothing or if there are just no arguments
            if request.form['val'] == '' or len(request.form['val']) == None:
                json_resp = json.dumps(
                    {
                        'result': 'Error',
                        'msg': 'No value provided'
                    }
                )
                return Response(
                    json_resp,
                    status=403,
                    mimetype='application/json'
                )

            # Conditional to check if the key is too long (> 200 chars)
            logging.debug("Size of key: " + str(len(key)))
            if len(key) > 200:
                json_resp = json.dumps(
                    {
                        'result': 'Error',
                        'msg': 'Key not valid'
                    }
                )
                return Response(
                    json_resp,
                    status=403,
                    mimetype='application/json'
                )

            # Conditional to check if input is greater than 1MB
            logging.debug("Size of val: " + str(len(request.form['val'])))

            if len(request.form['val']) > 1000000:
                json_resp = json.dumps(
                    {
                        'result': 'Error',
                        'msg': 'Object too large'
                    }
                )
                return Response(
                    json_resp,
                    status=404,
                    mimetype='application/json'
                )
            # Conditional to check if the input contains invalid characters outside of [a-zA-Z0-9_]
            if not re.compile('[A-Za-z0-9_]').findall(key):
                json_resp = json.dumps(
                    {
                        'result': 'Error',
                        'msg': 'Key not valid'
                    }
                )
                return Response(
                    json_resp,
                    status=404,
                    mimetype='application/json'
                )

            # If the value is in the dictionary, then replace the value of the existing key with a new value
            # Else, make a new key-val pair in the dict if the key does not exist
            if key in globals.KVSDict:
                # Replace the key-val pair in the dict with the new requested value
                # Precondition: the key must already exist in the dict
                logging.debug(request.form['val'])
                globals.KVSDict[key]['val'] = request.form['val']
                globals.KVSDict[key]['clock'] = globals.KVSDict[key]['clock'] + 1
                globals.KVSDict[key]['timestamp'] = str(time.time())
                json_resp = json.dumps(
                    {
                        'replaced': 'True',
                        'msg': 'Value of existing key replaced'
                    }
                )
                # Return the response
                return Response(
                    json_resp,
                    status=200,
                    mimetype='application/json'
                )
            elif key not in globals.KVSDict:
                logging.debug(request.form['val'])
                # Add the key-val pair to the dictionary
                newVal = {
                    'val': request.form['val'],
                    'clock': 0,
                    'timestamp': str(time.time())
                }
                globals.KVSDict[key] = newVal
                # globals.KVSDict[key] = request.form['val']
                json_resp = json.dumps(
                    {
                        'replaced': 'False',
                        'msg': 'New key created'
                    }
                )
                #logging.debug("Value in dict: " + globals.KVSDict[key])
                # Return the response
                return Response(
                    json_resp,
                    status=201,
                    mimetype='application/json'
                )
        except Exception as e:
            logging.error(e)
            json_resp = json.dumps(
                {
                    'result': 'Error',
                    'msg': str(e)
                }
            )
            # Return the response
            return Response(
                json_resp,
                status=404,
                mimetype='application/json'
            )