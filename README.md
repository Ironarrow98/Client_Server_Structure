Name: Chenxi Zhang
Student ID: 20671033
Quest ID: c462zhan

Tested on Student environment in 2 different machines with Python

1) Check the server's IP address
   Example: curl ifconfig.me

2) Start the server with req_code first, make sure req_code is a positive integer
   Example: ./server.sh 143

3) Get the port number from the server
   
4) Start the client with server's IP address, port number, req_code and message (Make sure to use the exact req_code, server address and port number)
   Example: ./client.sh 129.97.167.47 62358 143 "Hello World!" 