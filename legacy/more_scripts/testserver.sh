#!/bin/bash

# Author: Shane Dalton
# Created for UCSC undergrad course CMPS128, Fall 2017

# Initializes all servers listed in the ports list

cd ../src
echo "test"
echo "From server:"
num_servers=$1
echo $num_servers
K=4
VIEW="10.0.0.21:8080,10.0.0.22:8080,10.0.0.23:8080,10.0.0.24:8080"

# Starting port range
port=5000
echo putting foo:add on server
curl -X PUT localhost:5000/kv-store/foo -d val=add
echo getting foo:add from server
curl -X GET localhost:5000/kv-store/foo 
#This is how you can iterate test over multiple servers
#for i in $(seq 1 $num_servers)		#"${ports[@]}"
#do
	
#	echo "Raising server at localhost:$port"
#	python3 server1.py $K $VIEW localhost:$port &
#	let "port=port+1"
#done 
