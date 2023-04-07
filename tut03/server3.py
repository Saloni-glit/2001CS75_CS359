import socket
import select
import sys

# Function to handle client requests
def handle_client(client_socket):
    # Receive the client request
    request = client_socket.recv(1024).decode()
    if not request:
        sockets_list.remove(client_socket)
        del clients[client_socket]
        client_socket.close()
        return
    print("Client socket ",client_socket.fileno(),"sent message: " + str(request))
    try:
        # Evaluate the expression
        result = eval(request)
        # Send the result back to the client
    except:
        # If the expression is invalid, send an error message back to the client
        result = "Invalid input" 
    client_socket.send(str(result).encode())
    print("Sending reply: " + str(result))  
# Main function
if __name__ == "__main__":
    # Get the server IP and port number from the command line
    server_ip = sys.argv[1]
    server_port = int(sys.argv[2])
    
    # Create a TCP/IP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    # Bind the socket to the server address and port
    server_socket.bind((server_ip, server_port))
    
    # Listen for incoming connections
    server_socket.listen(5)
    print("Listening on {}:{}".format(server_ip, server_port))
    
    # List of sockets for select.select()
    sockets_list = [server_socket]
    
    # Clients dictionary, maps socket to client details
    clients = {}
    
    while True:
        # Get the list of sockets ready to be read
        read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)
        
        # Iterate over the sockets ready to be read
        for read_socket in read_sockets:
            # If it's the server socket, accept a new connection
            if read_socket == server_socket:
                client_socket, client_address = server_socket.accept()
                print(f"Connected with {client_address[0]}:{client_address[1]}")
                # client_socket.sendall('Welcome to the server!'.encode())
                print("Connected with client socket number ", client_socket.fileno())
                # Add the new client socket to the list of sockets
                sockets_list.append(client_socket)
                # Add the new client to the clients dictionary
                clients[client_socket] = client_address
            # Otherwise, handle the client request
            else:
                handle_client(read_socket)
                # Remove the socket from the list of sockets if the client has disconnected
                # sockets_list.remove(read_socket)
                # del clients[read_socket]
                # print("Client disconnected")
        for exception_socket in exception_sockets:
            sockets_list.remove(exception_socket)
            del clients[exception_socket]
            exception_socket.close()
    # Close the server socket
    
    server_socket.close()