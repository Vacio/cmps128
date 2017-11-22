"""
    Author: Cristian Gonzales
    Created for UCSC undergrad course CMPS 128, Fall 2017
"""

import logging
import threading

from CMPS128HW3KVSReplica import CMPS128HW3KVSReplica
from CMPS128HW3KVSProxy import CMPS128HW3KVSProxy
from CMPS128HW3KVSNodeDetails import CMPS128HW3KVSNodeDetails
from CMPS128HW3KVSGetAllReplicas import CMPS128HW3KVSGetAllReplicas
from CMPS128HW3KVSUpdateView import CMPS128HW3KVSUpdateView
from CMPS128HW3Node import CMPS128HW3Node

import globals

from gevent.wsgi import WSGIServer

# To prevent any errors, quick fix to patch the thread
import gevent.monkey; gevent.monkey.patch_thread()

import sys
sys.path.append('src/')

import os

"""
    Assignment 3
    ---------------
    A REST API service that serves as a fault tolerant key-value store (KVS) that is eventually consistent and a bounded
    staleness of 10 seconds. The KVS uses a vector clock protocol.
    
    Initiate the application with the appropriate KVS resource, logic to see if this instance is the main instance or
    a forwarding instance.

    Global variables (as listed in the settings file)
    -----------------------------------------------------
    :var app: The Flask app to be run (e.g., app.run(...))
    :var api: The API to wire up different routes
    :var numOfReplicas: The number of K replicas, as indicated by the environment variable
    :var localIPPort: The localIPPort for this specific instance in the form of IP:PORT (an identifier to query for objects)
    :var KVSDict: The key-value store, global to all 
    :var viewList: The global view of all nodes
    :var live_servers: All the live servers, or servers that are "up"
    :var absent_servers: All the servers that are "down"
"""
class CMPS128HW3Main:

    def __init__(self):

        # Environment variables
        globals.localIPPort = os.getenv('IPPORT')
        logging.debug("Value of IP:PORT: " + str(globals.localIPPort))

        # Number of replicas determined by client
        globals.numOfReplicas = int(os.getenv('K'))
        logging.info("Number of replicas: " + str(globals.numOfReplicas))

        # The initial VIEW list
        initialView = os.getenv('VIEW').split(",")
        logging.debug("List of all IP:PORT values in the VIEW: " + str(initialView))

        # The local port for this instance
        localPort = os.getenv('IPPORT').split(":")[1]
        logging.debug("Value of local port: " + str(localPort))

        # Number of total nodes
        numOfNodes = len(os.getenv('VIEW').split(","))
        logging.debug("Number of nodes: " + str(numOfNodes))


        # Simple loop to assign IP:Port values to each of the nodes, and append the nodes to the global
        # nodesList
        for i in range(numOfNodes):
            # Declare a node "holder", pointing at a fresh node to be stored in the global replica list
            singleNode = CMPS128HW3Node()
            # Set the IPPORT from the initialView list
            singleNode.set_IPPort(initialView[i])
            # Append this node to the entire global list of nodes in the KVS
            globals.viewList.append(singleNode)


        # Pass the number of nodes and replicas to subroutine to determine replicas and proxies (if any)
        self.delegate_replicas_and_proxies(numOfNodes, globals.numOfReplicas)

        # Initiate the scheduler to gossip with other nodes
        # sched = BackgroundScheduler(daemon=True)
        # sched.add_job(gossip, 'interval', seconds=3)
        # sched.start()

        # Add the appropriate views and run the application
        globals.app.add_url_rule('/kv-store/get_node_details',
                                 view_func=CMPS128HW3KVSNodeDetails.as_view('get_node_details'))
        globals.app.add_url_rule('/kv-store/get_all_replicas',
                                 view_func=CMPS128HW3KVSGetAllReplicas.as_view('get_all_replicas'))
        globals.app.add_url_rule('/kv-store/update_view?type=<type>',
                                 view_func=CMPS128HW3KVSUpdateView.as_view('update_view'))

        # Looking for our node, iterate through the entire VIEW list and  if it is the node local to this instance,
        # see if it is a replica or proxy and add the appropriate URL rule. We can then break out of the entire loop
        # to spare us any more comparisons
        for i in range(len(globals.viewList)):
            singleNode = globals.viewList[i]
            if singleNode.get_IPPort() == globals.localIPPort:
                if singleNode.get_role() == "replica":
                    globals.app.add_url_rule('/kv-store/<key>',
                                             view_func=CMPS128HW3KVSReplica.as_view('kv-store-replica'))
                    break
                elif singleNode.get_role() == "proxy":
                    globals.app.add_url_rule('/kv-store/<key>',
                                             view_func=CMPS128HW3KVSProxy.as_view('kv-store-proxy'))
                    break

        globals.local_server = WSGIServer(("0.0.0.0", int(localPort)), globals.app)
        logging.info("* Running on " + str(globals.localIPPort) + " (Press CTRL+C to quit)")
        globals.local_server.serve_forever()

    """
        Should the number of nodes be greater than the number of replicas, we will assign roles to replicas
        & proxies (note that this is the initial initialization only).

        Here, if the number of nodes is greater than or equal to the number of replicas, then we delegate which
        nodes are proxies and which are replicas. In this instance, we will delegate the first k nodes as replicas,
        and the rest will be proxies.

        Though, if the number of nodes is less than the number of proxies, we assume all current nodes are replicas
        and we perform "degraded mode."
    """
    def delegate_replicas_and_proxies(self, numOfNodes, numOfReplicas):
        if numOfNodes >= numOfReplicas:
            # For the entire list, print out each node value and then assign the first k nodes as replicas in a
            # dictionary. The upper bound here will be number of replicas.
            for i in range(numOfReplicas):
                singleNode = globals.viewList[i]
                singleNode.set_replica()
                logging.debug("Role of " + str(singleNode.get_IPPort()) + ": " + singleNode.get_role())
            # For the entire list, print out each node value and then assign the first [k+1]...[number of nodes] as
            # replicas in a dictionary. The upper bound here will be number of total nodes, and the lower bound will be
            # the number of replicas.
            for i in range(numOfReplicas, numOfNodes):
                singleNode = globals.viewList[i]
                singleNode.set_proxy()
                logging.debug("Role of " + str(singleNode.get_IPPort()) + ": " + singleNode.get_role())
        else:
            # For the entire list, print out each node value and then assign all the nodes as replicas in a
            # dictionary. The upper bound here will be number of total nodes.
            for i in range(numOfNodes):
                singleNode = globals.viewList[i]
                singleNode.set_replica()
                logging.debug("Role of " + str(singleNode.get_IPPort()) + ": " + singleNode.get_role())


# Initiate a new thread for the method
if __name__ == '__main__':
    try:
        # Setting root logging level to DEBUG
        logging.getLogger().setLevel(logging.DEBUG)

        # Initiate the threads
        settings_thread = threading.Thread(target=globals.globals)
        settings_thread.start()
        main_thread = threading.Thread(target=CMPS128HW3Main)
        main_thread.start()

    except Exception as e:
        logging.error(str(e))