#!/bin/bash

# Bash Script for CS456/656 Assignment 1
# Initialize Client Port (Please make sure to initialize the Server Port first)
# Parameters:
#    $1: <server_address>  (Please use command like "curl ifconfig.me" to check your Server's IP Address first)
#    $2: <n_port>          (Please make sure to initialize the Server Port first and get the Port Number from the Server)
#    $3: <req_code>        (Please make sure to use the exact same req_code that used in Server Port)
#    $4: message           (Please make sure to type "" in the message)
# Example Command;
#    ./client.sh 129.97.167.47 62358 253 "Hello World"
#    ./client.sh 129.97.167.47 62358 253 "TERMINATE"

python client.py $1 $2 $3 "$4"
