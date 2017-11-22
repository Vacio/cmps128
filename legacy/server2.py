"""
    Author: Shane Dalton
    Created for UCSC undergrad course CMPS 128, Fall 2017
"""

import sys

from flask import Flask
from flask import abort
from flask import request
from flask import Response
from apscheduler.schedulers.background import BackgroundScheduler

import json
import ast
import logging
import requests

import re
import time
from datetime import datetime
global this_server

global KVSDict
KVSDict = dict()

app = Flask(__name__)

def sendGossip():
    try:
        # print ("Gossiping: ", KVSDict)
        # return requests.get('localhost:8080/gossip').content
        return
    except Exception as e:
        logging.error(e)
        abort(400, message=str(e))


sched = BackgroundScheduler(daemon=True)
sched.add_job(sendGossip,'interval',seconds=3)
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


# from kvs_api import kvs_api

# state object for this_server's identifying information


class Node(object):
    number_of_replicas = 0
    view_node_list = []
    my_ip = ''
    my_port = ''
    my_role = ''
    kvs = {}
    causal_payload = {}
    live_servers = []
    replicas = []

    def __init__(self, env_vars):
        env_vars is sys.argv
        self.number_of_replicas = 1
        # list of all ip:port in the view ['ip1:port1', 'ip2:port2',... etc]
        self.view_node_list = ["1"]
        self.my_ip_port = "127.0.0.1:8081"
        self.my_ip = "127.0.0.1"
        self.my_port = "8081"
        self.my_role = 'replica'  # to start

    def my_identity(self):
        return self.my_ip_port

    # check for the case where it pings itself in iteration

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


def ping():
    # make a get request and send it to the target IP, set timeout for 1s, test and possibly reset it to 2s
    return 'up'

#  The ping route returns this server's IP and

@app.route('/ping', methods=['GET'])
def ping():
    json_resp = json.dumps({
        'result': 'success',
        'time': time.time(),
        'remote_server_ip': this_server.my_ip,
    })
    return Response(
        json_resp,
        status=403,
        mimetype='application/json'
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
        print('got a put request')

        try:
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

            # If the value is in the dictionary, then replace the value of the existing key with a new value
            # Else, make a new key-val pair in the dict if the key does not exist
            if key in KVSDict:
                # Replace the key-val pair in the dict with the new requested value
                # Precondition: the key must already exist in the dict
                print("Key already exists", KVSDict)
                logging.debug(key)

                KVSDict[key]['val'] = request.form['val']
                KVSDict[key]['clock'] = KVSDict[key]['clock'] + 1
                KVSDict[key]['timestamp'] = str(datetime.now())
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
                    'timestamp': str(datetime.now())
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
                #logging.debug("Value in dict: " + KVSDict[key])
                # Return the response
                return Response(
                    json_resp,
                    status=201,
                    mimetype='application/json'
                )


        except Exception as e:
            logging.error(e)
            abort(400, message=str(e))

    elif request.method == 'GET':
        try:
            # If the requested argument is in the dictionary, then return a sucessful message with the last stored
            # value. If not, then return a 404 error message
            logging.info("Value of key: " + str(KVSDict.get(key)))

            if key in KVSDict:
                logging.debug(key)
                json_resp = json.dumps(
                    {
                        'result': 'Success',
                        'value': KVSDict[key]
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
    # print(request.form)
    if request.form['type'] == 'add':
        # update the view list with a new server identity
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
    DictA = json.loads(request.data)
    newDict = dict()
    newDict = merge(KVSDict, DictA)

    json_resp = json.dumps({
        "msg": "success",
        "dict": KVSDict
    })
    return Response(
        json_resp,
        status=200,
        mimetype='application/json'
    )


if __name__ == '__main__':
    app.run(host=this_server.my_ip, port=this_server.my_port)
