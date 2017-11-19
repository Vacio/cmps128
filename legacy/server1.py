"""
    Author: Shane Dalton
    Created for UCSC undergrad course CMPS 128, Fall 2017
"""

import sys

import requests
from flask import Flask
from flask import abort
from flask import request
from flask import Response

from apscheduler.schedulers.background import BackgroundScheduler
import os
import json
import ast
import logging

import re
import time
from datetime import datetime
global this_server

global KVSDict
KVSDict = dict()

app = Flask(__name__)

def gossip():
    try:
        #print ("Gossiping: ", KVSDict)

        return
    except Exception as e:
        logging.error(e)
        abort(400, message=str(e))


sched = BackgroundScheduler(daemon=True)
sched.add_job(gossip,'interval',seconds=3)
sched.start()

def merge(dict1, dict2):
    #print("merging", dict1, dict2 )

    for key in dict1:
        #print(key)
        if key in dict2:
            #print(dict1[key], dict[key])
            winner = compare(dict1[key], dict2[key])
            #print("setting winner in dict1")
            dict1[key] = winner
        else:
            #print("in else")
            dict2[key] = dict1[key]
    for key in dict2:
        if key in dict1:
            winner = compare(dict1[key], dict2[key])
            dict2[key] = winner
        else:
            dict1[key] = dict2[key]
    return dict1

def compare(key1, key2):
    clock1 = int(key1['clock'])
    clock2 = int(key2['clock'])
    #print("comparing  c1 c2", clock1, clock2)
    if clock1 > clock2:
        return key1
    elif clock1 < clock2:
        return key2
    elif clock1 == clock2:
        # tie break timestamps
        if key1['timestamp'] > key2['timestamp']:
            print("tie breaker", key1['timestamp'], key2['timestamp'])
            return key1
        else:
            return key2


# state object for this_server's identifying information

"""
 CMPS128HW3Settings.localIPPort = os.getenv('IPPORT')
        logging.debug("Value of IP:PORT: " + str(CMPS128HW3Settings.localIPPort))

        localIP = os.getenv('IPPORT').split(":")[0]
        logging.debug("Value of local IP: " + str(localIP))

        my_port = os.getenv('IPPORT').split(":")[1]
        logging.debug("Value of local port: " + str(localPort))

        # Number of total nodes
        numOfNodes = len(os.getenv('VIEW').split(","))
        logging.debug("Number of nodes: " + str(numOfNodes))

        # Number of replicas determined by client
        numOfReplicas = int(os.getenv('K'))
        logging.info("Number of replicas: " + str(numOfReplicas))

        # All the nodes stored in the initial "VIEW" list
        viewList = os.getenv('VIEW').split(",")
        logging.debug("List of all IP:PORT values in the VIEW: " + str(viewList))
"""





#docker = 'loading from docker env variables
#docker = 'loading statically defined server'
docker = 'load state from command line'






# Like this: $python server1.py 3 "localhost:5000, localhost:5001, localhost:5002" "localhost:5000"
#  where 3 is the number of nodes and the string is the VIEW variable

class Node(object):
    number_of_replicas = 0
    view_node_list = []
    my_ip = ''
    my_port = ''
    my_role = ''
    causal_payload = {}
    live_servers = []
    replicas = []
    view_clock = 0

    def __init__(self, env_vars):

        if docker == 'loading statically defined server':
            print(env_vars)
            self.number_of_replicas = 1
            self.view_node_list = ["1"]
            self.my_ip_port = "127.0.0.1:8080"
            self.my_ip = "127.0.0.1"
            self.my_port = "8080"
            self.my_role = 'replica'  # to start

        if docker == 'loading from docker env variables':
            self.view_node_list = os.getenv('VIEW').split(",")
            self.my_ip_port = os.getenv('IPPORT')
            self.my_ip = self.my_ip_port.split(":")[0]
            self.my_port = self.my_ip_port.split(':')[1]
            self.view_node_list = os.getenv('VIEW').split(",")
            self.number_of_replicas =  len(self.view_node_list)

        elif docker == 'load state from command line':
            # env_vars is sys.argv
            print(env_vars)
            self.number_of_replicas = env_vars[1]
            # list of all ip:port in the view ['ip1:port1', 'ip2:port2',... etc]
            self.view_node_list = env_vars[2].split(',')
            self.my_ip_port = env_vars[3]
            self.my_ip = env_vars[3].split(':')[0]
            self.my_port = env_vars[3].split(':')[1]
            self.my_role = 'replica'  # to start

    def my_identity(self):
        return self.my_ip_port


    def update_view(self):
        for node in self.view_node_list:
            if node != self.my_ip_port:
                print("\n\nsending request to http://localhost:5001 \n\n")
                r = requests.put('http://localhost:5001' + '/secondary_update',
                                json={
                    'val':'test',
                    'result':'it made it',
                    'type':'add',
                },
                                headers={'content-type':'application/json'},
                                timeout=2,
                                )
                print(r)
            else:
                continue
            # set up the network trafficking portion here
        # for ip_port in self.view_node_list:


    def determine_replicas(self):
        # sort to order in precedence
        self.view_node_list = self.view_node_list.sort()

        # determine the live servers
        self.live_servers = []
        # pick the first K ip's from view that ARE LIVE and make them replicas

        for ip in self.view_node_list:
            if ping(ip) == 'up':
                self.live_servers.append((ip, 'up'))
            else:
                self.live_Servers.append((ip, 'down'))
        number_replicas = int(self.number_of_replicas)


# state object for this node
this_server = Node(sys.argv)


# for recieving updates from a node that recieved the initial update
@app.route('/secondary_update', methods=['PUT'])
def secondary_update():

    #Get a python dict with the data here

    print("\nSERVER: "+ this_server.my_ip_port+ "reporting secondary update view")
    print("\nNEW VIEW IS: "+str(this_server.view_node_list))
    if request.form['type'] == 'add':
        # update the view list with a new server identity
        print("second server add working")
        this_server.view_node_list.append(request.form['ip_port'])
        # this_server.update_state() #update state will
        json_resp = json.dumps({
            "msg": "success",
            "node_id": this_server.my_identity(),
            "number_of_nodes": len(this_server.view_node_list),
            "all servers": this_server.view_node_list,
        })
        return Response(
            json_resp,
            status=200,
            mimetype='application/json'
        )
    elif request.form['type'] == 'remove':
        this_server.view_node_list.remove(request.form['ip_port'])
        json_resp = json.dumps({
            "msg": "success",
            "node_id": this_server.my_identity(),
            "number_of_nodes": len(this_server.view_node_list),
            "all servers": this_server.view_node_list,
        })
        return Response(
            json_resp,
            status=200,
            mimetype='application/json'
        )
    else:
        return Response(
            json.dumps({'update_view': 'fall through no match'})
        )


def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()


@app.route('/kv-store/get_node_details', methods=['GET'])
def get_node_details():
    if this_server.my_role == 'replica':
        result = 'Yes'
    elif this_server.my_role == 'forwarding':
        result = 'No'
    else:
        result = 'get_node_details did not determine a role'
    json_resp = json.dumps({
        'result': 'success',
        "replica": result,
    })
    return Response(
        json_resp,
        status=403,
        mimetype='application/json'
    )


# necessary for remote start/stop
@app.route('/shutdown', methods=['POST'])
def shutdown():
    shutdown_server()
    return 'Server shutting down \n'


@app.route('/kv-store/<key>', methods=['PUT', 'GET'])
def put_in_kvs(key):

    # kvs_dict = this_server.kvs
    if request.method == 'PUT':
       # print('got a put request')

        #try:
        logging.debug(key)

        # Conditional to check if the input value is nothing or if there are just no arguments
        if request.form['val'] == '' or len(request.form['val']) == 0:
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



        if key in KVSDict:

            print("Key already exists", KVSDict)
            KVSDict[key]['val'] = request.form['val']
            KVSDict[key]['clock'] = KVSDict[key]['clock'] + 1
            KVSDict[key]['timestamp'] = str(time.time())

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

        elif key not in KVSDict:

            newVal = {
                'val': request.form['val'],
                'clock': 0,
                'timestamp': str(time.time())
            }

            KVSDict[key] = newVal
            print("----->", KVSDict[key])
            #KVSDict[key] = request.form['val'] old way


            json_resp = json.dumps(
                {
                    'replaced': 'False',
                    'msg': 'New key created'
                }
            )
            # logging.debug("Value in dict: " + KVSDict[key])
            # Return the response
            return Response(
                json_resp,
                status=201,
                mimetype='application/json'
            )

        #
        # except Exception as e:
        #     logging.error(e)
        #     abort(400, message=str(e))

    elif request.method == 'GET':
        try:
            # If the requested argument is in the dictionary,
            # then return a sucessful message with the last stored
            # value. If not, then return a 404 error message
            logging.info("Value of key: " + str(KVSDict.get(key)))

            if key in KVSDict:
                logging.debug(key)
                json_resp = json.dumps(
                    {
                        'result': 'Success',
                        'value': KVSDict[key]['val'],
                        'node_id': str(this_server.my_identity()),
                        'causal_payload': KVSDict[key]['clock'],
                        'timestamp': KVSDict[key]['timestamp']
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
            abort(400, message=str(e))

    else:
        return 'fall through error kv-store/<key>'




@app.route('/kv-store/update_view', methods=['PUT'])
def update_view():
    #print(request.form)
    if request.form['type'] == 'add':
        # update the view list with a new server identity
        this_server.view_node_list.append(request.form['ip_port'])
        print('appended'+request.form['ip_port'])
        this_server.update_view()

        json_resp = json.dumps({
            "msg": "success",
            "node_id": this_server.my_identity(),
            "number_of_nodes": len(this_server.view_node_list),
            "all servers": this_server.view_node_list,
        })
        return Response(
            json_resp,
            status=200,
            mimetype='application/json'
        )
    elif request.form['type'] == 'remove':
        this_server.view_node_list.remove(request.form['ip_port'])
        json_resp = json.dumps({
            "msg": "success",
            "node_id": this_server.my_identity(),
            "number_of_nodes": len(this_server.view_node_list),
            "all servers": this_server.view_node_list,
        })
        return Response(
            json_resp,
            status=200,
            mimetype='application/json'
        )
    else:
        return Response(
            json.dumps({'update_view': 'fall through no match'})
        )


@app.route('/server_name', methods=['GET'])
def server_name():
    try:
        json_resp = json.dumps(
            {
                'result': 'Success',
                'value': 'Server1',
                'ip:port': this_server.my_ip + ':' + this_server.my_port,
                'View': this_server.view_node_list
            }
        )
        return Response(
            json_resp,
            status=200,
            mimetype='application/json'
        )
    except Exception as e:
        logging.error(e)
        abort(400, message=str(e))

@app.route('/gossip', methods=['PUT'])
def gossip():
    DictA = ast.literal_eval(request.form['dict'])
    newDict = dict()
    newDict = merge(KVSDict, DictA)
    print("----->",newDict)
    json_resp = json.dumps({
        "msg": "success",
        "dict": newDict,
        "kvsdict": KVSDict,
    })
    return Response(
        json_resp,
        status=200,
        mimetype='application/json'
    )

@app.route('/print_kvs', methods=['GET'])
def print_kvs():
    json_resp = json.dumps({
        'dict':KVSDict,
    })
    return Response(
        json_resp,
        status=200,
        mimetype='application/json',
    )

if __name__ == '__main__':
    app.run(host=this_server.my_ip, port=this_server.my_port)
