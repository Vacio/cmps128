"""
    Author: Cristian Gonzales
    Created for UCSC undergrad course CMPS 128, Fall 2017
"""


from flask import Response
from flask.views import MethodView

import json
import logging

import globals

"""
    In this file, we will return the number of replicas that are currently available in the key-value store.
    :var nodesList: The global list of nodes from CMPS128HW3 to extrapolate data from
    :return: A HTTP response with the list of replicas
"""
class CMPS128HW3KVSGetAllReplicas(MethodView):

    # GET method to get the list of replicas
    def get(self):
        try:
            # For each node in the global nodesList (in CMPS128HW3Main), turn each item in the list into a string
            # and append it to the local replicaList, to be turned into JSON in json_resp
            json_resp = json.dumps({
                "result":"success",
                "replicas": self.get_replicas()
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

    # Method to iterate through the list and check if each node is a replica. If so, it will get
    # that node's IP and store it in a list to be returned to the caller
    def get_replicas(self):

        # Initially empty replica list to be returned to the caller
        replicaList = []

        # iterate through the list and if a node is a replica, append the IP:Port value to the replicaList
        for node in globals.viewList:
            if node.get_role() == "replica":
                replicaList.append(node.get_IPPort())

        # Return the replicaList
        return replicaList
