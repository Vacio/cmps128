#!/bin/sh
# Author: Cristian Gonzales
# CMPS 128

# Port number
PORT=8081

# Block comment
# if [ 1 -eq 0 ]; then
# Tests the PUT functionality by storing and changing the value of the key foo
curl -X PUT localhost:$PORT/kv-store/foo -d val=bart
echo "\n"

curl -X GET localhost:$PORT/kv-store/foo -d
echo "\n"

curl -X PUT localhost:$PORT/kv-store/foo -d val=bert
echo "\n"

curl -X GET localhost:$PORT/kv-store/foo
echo "\n"

# Tests the PUT functionality of a different key, making a single call
curl -X PUT localhost:$PORT/kv-store/ping -d val=else
echo "\n"

curl -X GET localhost:$PORT/kv-store/ping
echo "\n"


# Tests an invalid key (should return an error code)
curl -X GET localhost:$PORT/kv-store/invalidkey
echo "\n"

# Deletes existing keys 
curl -X DELETE localhost:$PORT/kv-store/foo
echo "\n"

curl -X DELETE localhost:$PORT/kv-store/ping
echo "\n"

# Deleting a key that does not exist (should return an error)
curl -X DELETE localhost:$PORT/kv-store/invalidkey
echo "\n"

# This should return an error, as these keys have already been deleted
curl -X GET localhost:$PORT/kv-store/foo
echo "\n"

curl -X GET localhost:$PORT/kv-store/ping
echo "\n"

# End block comment
# fi

# This should return an error, as one query is more than 1MB, the second query has invalid characters, and the third one is a request with no value
curl -X PUT localhost:$PORT/kv-store/foo -d val=s#*@!
echo "\n"

curl -X PUT localhost:$PORT/kv-store/foo -d val=
echo "\n"
