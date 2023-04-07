import socket
import threading
import sys

def handle_client(client_socket):
    print("Connected with client socket number", client_socket.fileno())
    while True:
        try:
            # Receive the client's message
            request = client_socket.recv(1024).decode()
            if not request:
                print("Client ", client_socket.fileno()," disconnected")
                break
            print("Client socket ",client_socket.fileno(),"sent message: " + request)    
            # Evaluate the expression
            try:
                result = eval(request) 
            except:
                result = "Invalid input"            
            # Send the result back to the client
            client_socket.send(str(result).encode())
            print("Sending reply: " + str(result))
        except:
            # If there's an error, close the socket and exit the loop
            client_socket.close()
            return

def start_server():
    # Get the server's IP and port from the command line arguments
    ip_address = sys.argv[1]
    port = int(sys.argv[2])

    # Create a TCP socket and bind it to the IP and port
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((ip_address, port))
    server_socket.listen(5)
    print(f"Listening on {ip_address}:{port}")

    # Handle client connections in a separate thread
    while True:
        try:
            # Wait for a client to connect
            client_socket, address = server_socket.accept()
            print(f"Connected with {address[0]}:{address[1]}")

            # Start a new thread to handle the client
            thread = threading.Thread(target=handle_client, args=(client_socket,))
            thread.start()

        except:
            # If there's an error, close the socket and exit the loop
            server_socket.close()
            return

if __name__ == "__main__":
    start_server()
