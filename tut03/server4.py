import socket
import select
import sys

# Define the server IP and port
SERVER_IP = sys.argv[1]
SERVER_PORT = int(sys.argv[2])

# Create the server socket and bind it to the IP and port
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((SERVER_IP, SERVER_PORT))

# Listen for incoming client connections
server_socket.listen()

# Set up a list of sockets to be monitored for incoming data
sockets_list = [server_socket]

# Set up a dictionary to keep track of client sockets and their associated data
clients = {}

print(f"Echo server started on {SERVER_IP}:{SERVER_PORT}")

while True:
    # Use the select method to monitor the sockets for incoming data
    read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)

    # Process the incoming data from the readable sockets
    for socket in read_sockets:
        # If the incoming data is from the server socket, accept the connection and add the client socket to the list
        if socket == server_socket:
            client_socket, client_address = server_socket.accept()
            sockets_list.append(client_socket)
            print(f"New client connected: {client_address}")
            clients[client_socket] = ''

        # If the incoming data is from a client socket, receive the message and send it back to the client
        else:
            data = socket.recv(1024).decode()
            print("Client socket ",client_socket.fileno(),"sent message: " + data)
            if data:
                # If the client socket has not sent any previous data, save the data in the dictionary
                if not clients[socket]:
                    clients[socket] = data
                # If the client socket has sent previous data, append the new data to the previous data and send it back
                else:
                    clients[socket] = data
                socket.sendall(clients[socket].encode())
                print("Sending reply: " + clients[socket]) 
            # If there is no incoming data, remove the socket from the list and close the connection
            else:
                sockets_list.remove(socket)
                del clients[socket]
                socket.close()

    # Handle any exception sockets
    for socket in exception_sockets:
        sockets_list.remove(socket)
        del clients[socket]
        socket.close()
