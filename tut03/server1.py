import socket

def calculate(expression):
    """Evaluates a simple arithmetic expression"""
    try:
        result = eval(expression)
        return str(result)
    except:
        return "Invalid expression"

socky = -1
def handle_client(client_socket):
    """Handles a single client connection"""
    print("Connected with client socket number", client_socket.fileno())
    global socky
    while True:
        try:
            # Receive data from the client
            data = client_socket.recv(1024).decode().strip()

            # If no data received, client has terminated
            if not data:
                print("Client disconnected")
                break
            print("Client socket ",client_socket.fileno(),"sent message: " + data)
            # Evaluate the expression and send back the result
            # if socky == -1 or socky == client_socket.fileno(): socky = client_socket.fileno()
            # else:
            #      result = -1000
            #      print("Sending reply: " + result)
            #      client_socket.sendall(result.encode())
                
            result = calculate(data)
            print("Sending reply: " + result)
            client_socket.sendall(result.encode())

        except Exception as e:
            print("Error: ", e)
            break

    client_socket.close()

if __name__ == "__main__":
    # Parse command-line arguments
    import argparse
    parser = argparse.ArgumentParser(description="Simple calculator server")
    parser.add_argument("ip", help="Server IP address")
    parser.add_argument("port", type=int, help="Server port number")
    args = parser.parse_args()

    # Create the server socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((args.ip, args.port))
    server_socket.listen(1)
    print("Listening on", args.ip, ":", args.port)

    # Wait for client connections
    while True:
        client_socket, client_address = server_socket.accept()
        handle_client(client_socket)

