"""
    Author: Cristian Gonzales
    Created for UCSC undergrad course CMPS 128, Fall 2017
"""
from flask.views import MethodView
from flask import Response

import json

import logging

import globals

"""
    In this file, this is a resource that will check if this instance is a forwarding instance or a replica.
    :var localIPPort: This instance's local IP and port, to be checked against the dictionary with all the IP:PORT
        keys and their associated statuses. This is global, as declared in CMPS128HW3Main
    :var nodeStatus: The dictionary that contains all the IP:PORT values and their associated statuses (either 
        they are replicas, or they are proxies).
    :return: An HTTP response
"""
class CMPS128HW3KVSNodeDetails(MethodView):

    # Get method to see if current instance is a replica or not
    def get(self):
        try:
            # For each node in the list, if the IP:Port value of the local state is equal to an IP Port of
            # a node, and if it's role is replica, then return a JSON response that indicates that it is
            # a replica. If that node's role isn't a replica, then return a JSON response that indicates
            # that it isn't a replica.
            for node in globals.viewList:
                if str(node.get_IPPort()) == str(globals.localIPPort):
                    if str(node.get_role()) == "replica":
                        json_resp = json.dumps({
                            "result": "success",
                            "replica": "Yes"
                        })
                    else:
                        json_resp = json.dumps({
                            "result": "success",
                            "replica": "No"
                        })
                    # Return the response as JSON
                    return Response(
                        json_resp,
                        status=200,
                        mimetype='application/json'
                    )
                
        except Exception as e:
            logging.error(e)
            json_resp = json.dumps(
                {
                    "result":"error",
                    "msg": str(e)
                }
            )
            return Response(
                json_resp,
                status=404,
                mimetype='application/json'
            )