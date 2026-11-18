import os
import socket
import threading
from pathlib import Path

SIZE = 1024
FORMAT = "utf-8"
SERVER_PATH = "server"

# Client handler
def handle_client (conn,addr):
    basePath = Path.cwd() / "ServerResources"
    passPath = Path.cwd() / "AccountInfo"

    print(f"[NEW CONNECTION] {addr} connected.")
    conn.send("OK@Welcome to the server!".encode(FORMAT))

    while True:
        try:
            data = conn.recv(SIZE).decode(FORMAT)
            data = data.split("@")
            cmd = data[0]
        except:
            break
       
        send_data = "OK@"

        if cmd == "LOGIN":
            userfile = data[1] + ".txt"
            passhash = data[2]
            if (passPath / userfile).is_file():
                userdir = passPath / userfile
                hashfile = open(userdir, "r")
                serverhash = hashfile.read()
                hashfile.close()
                if serverhash == passhash:
                    conn.send("LOGGEDIN@Authentication verified.".encode(FORMAT))
                else:
                    conn.send("ERROR@Incorrect password.".encode(FORMAT))
            else:
                conn.send("ERROR@Invalid username.".encode(FORMAT))

        elif cmd == "LOGOUT":
            break
        
        elif cmd == "UPLOAD":
            filename = data[1]
            if not (basePath / filename).is_file():
                send_data += f"File {filename} available."
            else:
                send_data = f"ERROR@{filename} already exists."

            conn.send(send_data.encode(FORMAT))

        elif cmd == "DOWNLOAD":
            filename = data[1]
            if (basePath / filename).is_file():
                send_data += f"File {filename} available."
            else:
                send_data = f"ERROR@{filename} does not exist."

            conn.send(send_data.encode(FORMAT))

        elif cmd == "ERROR":
            send_data = f"ERROR@{data[1]}"
            conn.send(send_data.encode(FORMAT))

        # Generic error
        else:
            conn.send("ERROR@An error occurred.".encode(FORMAT))



    print(f"{addr} disconnected.")
    conn.close()


def main():
    IP = input("Enter an IP to listen on: ")
    PORT = int(input("Enter a port to listen on: "))
    ADDR = (IP,PORT)
    print("Starting the server...")
    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM) ## used IPV4 and TCP connection
    server.bind(ADDR) # bind the address
    server.listen() ## start listening
    print(f"Server is listening on {IP}:{PORT}")
    while True:
        conn, addr = server.accept() ### accept a connection from a client
        thread = threading.Thread(target = handle_client, args = (conn, addr)) ## assigning a thread for each client
        thread.start()


if __name__ == "__main__":
    main()


