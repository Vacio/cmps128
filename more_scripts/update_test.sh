#!/bin/sh

PORT=5000
#send update view to localhost:5000

curl -X PUT localhost:$PORT/kv-store/update_view -d type=add -d ip_port='localhost:5001'
#curl -X PUT localhost:5000/kv-store/update_view -d type=add -d ip_port='localhost:5001'
curl -X PUT localhost:5002/kv-store/update_view -d type=remove -d ip_port=localhost:5004
#check view on localhost:5001

