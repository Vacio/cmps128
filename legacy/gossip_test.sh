#!/bin/sh


#put some test values into the server's KVS's
# clock increment tests
curl -X PUT localhost:5000/kv-store/key1 -d val="shld be replaced"

curl -X PUT localhost:5000/kv-store/key3 -d val="shld be replaced"

curl -X PUT localhost:5000/kv-store/key3 -d val="shld win"

curl -X PUT localhost:5000/kv-store/key1 -d val="shld win"
curl -X PUT localhost:5001/kv-store/key3 -d val="not final"
curl -X PUT localhost:5001/kv-store/key1 -d val="vc 1"
curl -X
#timestamp tests

#merge em
curl -X GET localhost:5000/test_gossip
#check to see that the two