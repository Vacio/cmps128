"""
    Author: Cristian Gonzales
    Created for UCSC undergrad course CMPS 128, Fall 2017
"""
from flask import Flask

"""
    Global variables for the entire codebase are initialized here.
    
    Global variables
    --------------------
    :var app: The Flask app to be run (e.g., app.run(...))
    :var local_server: The server for this instance, to be ran globally
    :var numOfReplicas: The number of K replicas, as indicated by the environment variable
    :var localIPPort: The localIPPort for this specific instance in the form of IP:PORT (an identifier to query for objects)
    :var KVSDict: The key-value store, global to all 
    :var viewList: The global view of all nodes
    :var live_servers: All the live servers, or servers that are "up"
    :var absent_servers: All the servers that are "down"
"""
class globals:
    def __init__(self):

        global app
        app = Flask(__name__)

        global local_server

        global numOfReplicas

        global localIPPort

        global KVSDict
        KVSDict = dict()

        global viewList
        viewList = []

        global live_servers
        live_servers = []

        global absent_servers
        absent_servers = []