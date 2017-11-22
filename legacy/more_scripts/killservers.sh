#!/bin/bash
#Shane Dalton CMPS128
#Kills all servers via shutdown route
cd ..
echo "test"
echo "From server:"
ports=(5000 5001 5002 5003 5004 8080)
for port in "${ports[@]}"
do
	echo "Killing $port"
curl -X POST localhost:$port/shutdown
done