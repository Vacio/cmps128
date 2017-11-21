#!/bin/bash
#Shane Dalton CMPS128
#Initializes all servers
#listed in the ports list

#first positional argument is the number of servers to start, progressing from 1 to 5
runservers.sh 5
./killservers.sh