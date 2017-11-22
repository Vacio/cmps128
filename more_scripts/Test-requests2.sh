#!/bin/sh
# Author: Cristian Gonzales
# CMPS 128

# Port number
PORT=8084

# Tests the PUT functionality by storing and changing the value of the key foo
curl -X PUT localhost:$PORT/kv-store/foo -d val=bart
curl -X GET localhost:$PORT/kv-store/foo
