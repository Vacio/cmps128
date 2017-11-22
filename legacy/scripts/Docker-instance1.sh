#!/bin/sh
# Author: Cristian Gonzales
# CMPS 128, UCSC Fall 2017
# Emulate a Docker instance with 4 nodes and 3 replicas

cd ..
docker build -t cmps128hw3 .

docker run -p 8081:8080 --ip=10.0.0.21 --net=mynet -e K=3 -e VIEW="10.0.0.21:8080,10.0.0.22:8080,10.0.0.23:8080,10.0.0.24:8080" -e IPPORT="10.0.0.21:8080" cmps128hw3
