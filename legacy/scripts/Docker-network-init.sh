#!/bin/sh
# Author: Cristian Gonzales
# CMPS 128, UCSC Fall 2017
# Create a Docker network called 'mynet' and build Docker container

docker network create --subnet 10.0.0.0/16 mynet
