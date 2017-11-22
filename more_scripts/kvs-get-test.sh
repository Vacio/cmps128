#!/bin/sh

PORT=5000
./killservers.sh

python server1.py 3 "localhost:5000, localhost:5001, localhost:5002" localhost:5000


#put a value and then get it back
curl -X PUT 127.0.0.1:$PORT/gossip -d dict={val1:val2,val2:val3,}
echo "\n"


#
#curl -X GET 127.0.0.1:$PORT/kv-store/test
#echo "\n"
#
##put the value again and check to see if the clock increments
#echo "Clock should increment here \n"

#
#curl -X PUT 127.0.0.1:$PORT/kv-store/test -d val=cheese1 -d causal_payload="1"

