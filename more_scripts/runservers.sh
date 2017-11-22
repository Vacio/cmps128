#!/bin/bash
# Author: Shane Dalton
# Created for UCSC undergrad course CMPS128, Fall 2017

# Initializes all servers listed in the ports list

echo "test"
echo "From server:"
num_servers=$1
echo $num_servers
K=4
VIEW1="10.0.0.21:8080,10.0.0.22:8080,10.0.0.23:8080,10.0.0.24:8080"
#fill in this list with the addresses of all servers you want to spawn
VIEW="localhost:5000,localhost:5001,localhost:5002,localhost:5003"
#starting port range
port=5000
for i in $(seq 1 $num_servers)		#"${ports[@]}"
do
	
	echo "Raising server at localhost:$port"
	python server1.py $K $VIEW localhost:$port &
	let "port=port+1"

done 



    # d1 = json.loads(d) string->dictionary  d - > d1
    # d2 = json.dumps(d)  dictionary -> string     d2 - > d
    # d3 = json.dumps(json.loads(d))  # 'dumps' gets the dict from 'loads' this time