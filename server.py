import sys
import socket
from contextlib import closing


# References:
#     Piazza (including code provided on Piazza)
#     Course Slides
#     Textbook
#     Python Documentation


# Global variable that saves all the income messages
msg_buffer = []


# Class that saves income message and the client port number
class Message:
  # Constructor
  def __init__(self, server_port, msg):
    self.server_port = server_port
    self.msg = msg
  # Displayer
  def __repr__(self):
    return "[" + str(self.server_port) + "]: " + self.msg
  # Presentor
  def __str__(self):
    return "[" + str(self.server_port) + "]: " + self.msg
    

# Function for negotiating with the client
def Server_Client_Negotiation(req_code):
  
  # Check if request code is a number
  if not req_code.isdigit():
    print("ERROR 2: Invalid req_code, req_code must be a number.")
    sys.exit(2)

  # Initialize TCP socket and bind to a randomly assigned avalible port
  server_TCP_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  server_TCP_socket.bind(('', 0))
  server_addr, server_port = server_TCP_socket.getsockname()
  print("SERVER_PORT={}".format(server_port))

  # Waiting for connections from clients
  server_TCP_socket.listen(1)
  while True:
  
    # Get client socket and client's IP address
    client_TCP_socket, client_TCP_addr = server_TCP_socket.accept()

    # Set the timeout to be 30 seconds to prevent case like infinite loop
    client_TCP_socket.settimeout(30)

    # Use try/except to prevent server crashing
    try:
      client_req_code = client_TCP_socket.recv(1024).decode()
    except socket.timeout:
      # Close the connection, throw Error Code 3 after timeout, and wait for new connection
      client_TCP_socket.send("ERROR 3: connection timeout, connection closed".encode())
      client_TCP_socket.close()
      continue
      
    if not client_req_code:
      # Prevent client sends invalid req_code
      continue
    elif not client_req_code == req_code:
      # Close the connection, throw Error Code 0 after timeout, and terminate the server
      client_TCP_socket.send("ERROR 0: Invalid req_code.".encode())
      client_TCP_socket.close()
      return
    else:
      # Request code is successfully matched, and create new UDP socket
      client_TCP_socket.settimeout(None)
      # Create new UDP socket and bind to a randomly assigned avaliable port
      client_UDP_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
      client_UDP_socket.bind(('', 0))
      t_addr, t_port = client_UDP_socket.getsockname()

      # Send the UDP port number to the client and close the TCP socket
      client_TCP_socket.send(str(t_port).encode())
      client_TCP_socket.close()
      # Set UDP socket timeout to 30 seconds
      client_UDP_socket.settimeout(30)

      # Start waiting for UDP message
      # Use try/except to prevent timeout or other ERRORs that may crash the server
      try:
        client_message, client_UDP_addr = client_UDP_socket.recvfrom(1024)
      except:
        # ERROR case, terminate the server
        return
        
      # Analyze the message
      if client_message == "TERMINATE":
        # If the message is "TERMINATE"
        if msg_buffer == []:
          # There are no stored messages, send "NO MSG" to the client and terminate the server
          end_message = "NO MSG.\n"
          client_UDP_socket.sendto(end_message.encode(), client_UDP_addr)
        else:
          # Send all stored message to the client and terminate the server
          for mc in msg_buffer:
            client_UDP_socket.sendto(str(mc).encode(), client_UDP_addr)
          end_message = "NO MSG.\n"
          client_UDP_socket.sendto(end_message.encode(), client_UDP_addr)
        client_UDP_socket.close()
        return
      else:
        # Other messages
        if msg_buffer == []:
          # There are no stored messages, send "NO MSG" to the client and save the current message to the buffer
          end_message = "NO MSG.\n"
          client_UDP_socket.sendto(end_message.encode(), client_UDP_addr)
        else:
          # Send all stored message to the client and save the current message to the buffer
          for mc in msg_buffer:
            client_UDP_socket.sendto(str(mc).encode(), client_UDP_addr)
          end_message = "NO MSG.\n"
          client_UDP_socket.sendto(end_message.encode(), client_UDP_addr)
        client_UDP_socket.close()
        message_class = Message(client_UDP_addr[1], client_message)
        msg_buffer.append(message_class)



# Check if the number of arguments is correct
if not len(sys.argv) == 2:
  print("ERROR 1: two parameters was expected, {} was found".format(len(sys.argv) - 1))
  sys.exit(2)


# Initialize the server
req_code = sys.argv[1]
Server_Client_Negotiation(req_code)




  
