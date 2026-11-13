import os
import socket

SIZE = 1024
FORMAT = "utf-8"
SERVER_DATA_PATH = "server_data"

def main():
    # User configurable connection
    IP = input("Server IP: ")
    PORT = int(input("Server Port: "))
    ADDR = (IP,PORT)
    
    print(f"\nConnecting to {IP}:{PORT}...\n")
    client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    client.connect(ADDR)
    
    print("\nConnected to server.\n")
    
    while True:
        data = client.recv(SIZE).decode(FORMAT)
        cmd, msg = data.split("@")
      
        if cmd == "OK":
            print(f"{msg}")
        elif cmd == "DISCONNECTED":
            print(f"{msg}")
            break
        
        data = input("> ")
        data = data.split(" ")
        cmd = data[0]

        if cmd == "TASK":
            client.send(cmd.encode(FORMAT))
            
        elif cmd == "HELP":
            # Should this be handled client-side or server-side?
            continue

        elif cmd == "LOGOUT":
            client.send(cmd.encode(FORMAT))
            break
        
        else:
            print("Invalid command, please try again.")
            continue

    # Close the connection when loop broken
    print("Disconnected from server.")
    client.close()

if __name__ == "__main__":
    # Main function execution
    main()
