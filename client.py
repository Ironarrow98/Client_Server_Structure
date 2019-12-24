import sys
import socket


# References:
#     Piazza (including code provided on Piazza)
#     Course Slides
#     Textbook
#     Python Documentation



# Check if the number of parameter is corrrct
if not len(sys.argv) == 5:
  print("ERROR 1: five parameters was expected, {} was found".format(len(sys.argv) - 1))
  sys.exit(2)
  


# Make sure the port number and req_code are numbers
if not sys.argv[2].isdigit():
  print("ERROR 2: the Port Number must be number")
  sys.exit(2)  
if not sys.argv[3].isdigit():
  print("ERROR 3: the Request Code must be number")
  sys.exit(2)  
  


# Save server IP address, server port number, req_code and message from the command line
server_addr = sys.argv[1]
n_port = int(sys.argv[2])
req_code = sys.argv[3]
message = sys.argv[4]



# Create the TCP socket to connect to the server 
client_TCP_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)



# Save the socket port number
client_TCP_socket.connect((server_addr, n_port))



# Send the req_code to the server
client_TCP_socket.send(req_code.encode())



# Use try/except to prevent timeout or other ERRORs that may crash the client
try:
  msg_port = client_TCP_socket.recv(1024).decode()
  message_port = int(msg_port)
except:
  # Exit with a non-zero ERROR message code
  print(msg_port)
  sys.exit(1)



# Close the client TCP socket
client_TCP_socket.close()



# Initialize UDP socket to send message
client_UDP_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_UDP_socket.sendto(message.encode(), (server_addr, message_port))



# Set timeout to 30 to prevent timeout or connection lost
client_UDP_socket.settimeout(30)



# Get and display return messages
returned_message = ""
while returned_message != "NO MSG.\n": 
  returned_message, server_addr = client_UDP_socket.recvfrom(1024)
  print(returned_message.decode())



# Allow user to type any input and terminate the client
k = raw_input("Press any key to exit")
if(len(k) >= 0):
  client_UDP_socket.close()




