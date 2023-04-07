import socket
import sys

def client_program():
    host = sys.argv[1]
    port = int(sys.argv[2])
    
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
   
    try:
        client_socket.connect((host, port))
   

        print("Connected to server")
   
        while True:
            message = input("Please enter the message to the server: ")
           # print(message.encode())
            client_socket.send(message.encode())
            #print(message.encode())
            if message == "exit":
                break
            data = client_socket.recv(1024).decode()
            
            
            print("Server replied: " + data)
        
        client_socket.close()
    except socket.error as e:
      print("Client is already connected, please try after sometime")
      client_socket.close()

if __name__ == '__main__':
    client_program()