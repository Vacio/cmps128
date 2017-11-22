"""
    Author: Cristian Gonzales
    Created for UCSC undergrad course CMPS 128, Fall 2017
"""

from flask.views import MethodView
from flask import Response
from flask import request

import requests

import json

import logging

from CMPS128HW3Node import CMPS128HW3Node

from gevent.wsgi import WSGIServer
import gevent

import globals

"""
    In this file, this is a resource to perform a PUT request to update the view (add or remove nodes).
    
    :return: An HTTP response
"""
class CMPS128HW3KVSUpdateView(MethodView):

    """
        PUT request to add or delete a node to the network, and reconfigure the replicas and proxies such that we
        account for the new node, if it is to stay a replica or be a proxy based on the prerequisite for degraded mode
    """
    def put(self, type):
        try:
            # The new node as an IP:PORT value
            new_node_value = request.form['ip_port']
            # The PUT type (presumably, 'add' or 'remove')
            PUT_type = str(type)

            logging.debug("Type of view update: "  + PUT_type)
            logging.debug("IP:PORT value to " + PUT_type + ": " + str(new_node_value))

            # Determine if the request is to add a node. Any request that deviates from this is invalid.
            if PUT_type == "add":
                # Create a new node and set its IPPORT value
                new_node = CMPS128HW3Node()
                new_node.set_IPPort(str(new_node_value))
                # If the total number of nodes after the add is greater than the number of replicas K, then
                # set it to be a proxy. If not, then set it to be a replica.
                if (len(globals.viewList) + 1) > globals.numOfReplicas:
                    new_node.set_proxy()
                else:
                    new_node.set_replica()
                # Add the new node to this globals list
                globals.viewList.append(new_node)
                # At the very end, make forward whatever request it may have been to all other instances. Should it be
                # the case that an instance does not exist, it will be appended to a global absent_servers list
                self.forward_request(PUT_type, new_node_value)
                # Forming the JSON request and returning the appropriate message
                json_resp = json.dumps(
                    {
                        "msg":"success",
                        "node_id":str(new_node_value),
                        "number_of_nodes":len(globals.viewList)
                    }
                )
                return Response(
                    json_resp,
                    status=200,
                    mimetype='application/json'
                )
            # Determine if the request is to remove a node. Any request that deviates from this is invalid.
            elif PUT_type == "remove":
                # If the total number of nodes after the delete is still greater than the number of replicas K, then
                # delete it and that's it. If not, then we need to change all proxies to be replicas.
                if (len(globals.viewList) - 1) > globals.numOfReplicas:
                    # Here, we will append each IPPort value of all existing nodes to a list. Then, we will compare
                    # the requested value to the list of IPPort values. If it is not in the list, we will return an
                    # error to the client saying that the value does not exist.
                    listOfIPPorts = []
                    # Here, we iterate through the global viewList and if we find the node to be deleted
                    for node in globals.viewList:
                        # Append all node's IPPort values to the local list of IPPort values that we initialized outside
                        # of the loop
                        listOfIPPorts.append(node.get_IPPort())
                        # If we have a IPPort value that is equal to the requested value to be deleted, then we remove
                        # it from the list and then proceed to error check if we did not remove a node.
                        if node.get_IPPort() == new_node_value:
                            globals.viewList.remove(node)
                    # Here the error checking occurs for an invalid request to delete a node that doesn't exist
                    if new_node_value not in listOfIPPorts:
                        json_resp = json.dumps(
                            {
                                "result": "error",
                                "msg": "invalid ip_port value (does not exist)"
                            }
                        )
                        return Response(
                            json_resp,
                            status=404,
                            mimetype='application/json'
                        )
                    # Here, we will do another loop executed in the count_replicas() method. The justification for
                    # running another loop with the same bounds as the prior loop is that if the node is DID exist
                    # and was successfully removed, we want to correctly count the number of replicas in the global
                    # view. Thus, this comparison says that if the current replica count is not equal to K (or the
                    # required number of replicas), then take the difference between K and the replica count. Also
                    # note here that we do not need an else statement because should it be the case that the replica
                    # count is equal to the number of replicas, then we do not need to do anything...
                    current_replica_count = self.replica_count()
                    if current_replica_count != globals.numOfReplicas:
                        # This determines the number of replicas need to become proxies...
                        numOfReplicasToProxies = globals.numOfReplicas - current_replica_count
                        self.set_replica_to_proxy(numOfReplicasToProxies)
                # This is the case that the number of nodes in the view is less than the number of replicas K. Here,
                # we simply need to turn any current proxies into replicas...
                else:
                    # TODO: Implement the logic and make sure that we reconfigure the replicas and proxies
                    pass
                # At the very end, make forward whatever request it may have been to all other instances. Should it be
                # the case that an instance does not exist, it will be appended to a global absent_servers list
                self.forward_request(PUT_type, new_node_value)

                # Forming the JSON request and returning the appropriate message
                json_resp = json.dumps(
                    {
                        "result":"success",
                        "number_of_nodes":len(globals.viewList)
                    }
                )
                return Response(
                    json_resp,
                    status=200,
                    mimetype='application/json'
                )
            # The request did not specify add or remove, and therefore, it is invalid
            else:
                json_resp = json.dumps(
                    {
                        "result":"error",
                        "msg":"Invalid request"
                    }
                )
                return Response(
                    json_resp,
                    status=404,
                    mimetype='application/json'
                )
        # Miscellaneous exception handling in case anything breaks
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

    """
        Here, we forward the request with all the fields given to us to all the IPs that aren't this instance
        :param type: The type of request ("add" or "remove") that is being made to the other nodes
        :param IPPort: The IPPort value that was given to us to forward to the other nodes.
    """
    def forward_request(self, type, new_node_value):
        # For each node in the global VIEW list
        for node in globals.viewList:
            # If this node's IPPORT is not equal to this instance's IPPORT value, forward the request (we do this so
            # that we don't forward a request to ourselves). In the try-catch, if it throws an error, then we will
            # log the error and then add the node to the global list of absent servers
            if node.get_IPPort() != globals.localIPPort:
                try:
                    logging.info("* Forwarding request to " + str(node.get_IPPort()) + " to update the view")
                    # PUT forwarding request
                    requests.put(
                        "http://" + str(node.get_IPPort()) + "/kv-store/update_view?type=" + type,
                        data={'ip_port': new_node_value},
                        timeout=1
                    )
                    # Acknowledgement for the PUT request
                    logging.info("* ACK from " + str(globals.localIPPort)
                                 + "for /update_view fowarded PUT request to "
                                 + str(node.get_IPPort()))
                except Exception as e:
                    logging.info(e)
                    logging.info("* Address at " + node.get_IPPort() + " unreachable")
                    self.absent_servers.append(node)

    """
        Here, we are simply count the number of replicas for the global view list and return it to the caller.
        :var count: the replica counter to be used and returned to the caller
        :return: an integer for the amount of replicas present in the global view list
    """
    def replica_count(self):
        # The replica_count is the counter we will use to calculate the total number of replicas in the global view.
        # We will return this count to the caller as the count of all the replicas in the global VIEW list.
        count = 0;
        # For all nodes in the global view list, if its role is a replica, add one to the count
        for node in globals.viewList:
            if node.get_role() == "replica":
                count = count + 1
        return count

    """
        Here, we will loop through the global view list and set a proxy to a replica. We only use this for the case
        that the length of the view list is greater than k after removing a node.
        :return: void
    """
    def set_replica_to_proxy(self, bound):
        # Our counter to count how many replicas we are setting to proxies.
        count = 0
        # Iterate through the nodes and for each replica we encounter, we will set it to a proxy. We do this for
        # x number of nodes, or the bound requested by the client
        for node in globals.viewList:
            if node.get_role() == "replica":
                # Set this node to a proxy and increment the count
                node.set_proxy()
                count = count + 1
                # Check the count to the bound requested by the caller. If they were equal, break out of this loop
                # and exit the method
                if count == bound:
                    break

    """
        This method, specific to the case where we need to delete the nodes, will be called to reconfigure proxies and
        replicas
    """
    def reconfigure_nodes(self, currentReplicaCount):
        pass