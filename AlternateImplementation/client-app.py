import os
import socket
import struct
from pathlib import Path
from getpass import getpass
import hashlib

SIZE = 1024
FORMAT = "utf-8"
SERVER_DATA_PATH = "server_data"

def main():
    # User configurable connection
    IP = input("Server IP: ")
    PORT = int(input("Server Port: "))
    ADDR = (IP,PORT)
    basePath = Path.cwd() / "ClientResources"
    isAuthenticated = False

    print(f"\nConnecting to {IP}:{PORT}...")
    try:
        client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        client.connect(ADDR)
    except:
        print(f"Connection error. Unable to connect to {IP}:{PORT}\n")
        quit()

    print("\n=====LIST OF COMMANDS=====")
    print("UPLOAD")
    print("DOWNLOAD")
    print("DELETE")
    print("DIR")
    print("SUBFOLDER (CREATE/DELETE)")
    print("LOGOUT")
    print("==========================\n")

    while True:
        data = client.recv(SIZE).decode(FORMAT)
        cmd, msg = data.split("@")
        
        if cmd == "OK":
            print(f"[OK] {msg}")
        elif cmd == "ERROR":
            print(f"[ERROR] {msg}")
        elif cmd == "LOGGEDIN":
            print(f"[OK] {msg}")
            isAuthenticated = True
        elif cmd == "DISCONNECTED":
            print(f"[DISCONNECT] {msg}")
            break
        
        # Console input
        send_data = ""
        data = input("> ")
        data = data.split(" ")
        cmd = data[0].upper()
        send_data += cmd

        # Upload command
        if cmd == "UPLOAD":
            try:
                filename = data[1]
                print(f"Filename: {filename}")
                if (basePath / filename).is_file():
                    print(f"File {filename} exists.")
                    send_data += f"@{filename}"
                    client.send(send_data.encode(FORMAT))
                else:
                    send_data = "ERROR@File {filename} does not exist."
                    client.send(send_data.encode(FORMAT))
            except IndexError:
                send_data = "ERROR@No file name was included."
                client.send(send_data.encode(FORMAT))

        # Download command
        elif cmd == "DOWNLOAD":
            try:
                filename = data[1]
                print(f"Filename: {filename}")
                if (basePath / filename).is_file():
                    send_data = "ERROR@File {filename} already exists."
                    client.send(send_data.encode(FORMAT))
                else:
                    send_data += f"@{filename}"
                    client.send(send_data.encode(FORMAT))
            except IndexError:
                send_data = "ERROR@No file name was included."
                client.send(send_data.encode(FORMAT))

        # Delete command
        elif cmd == "DELETE":
            try:
                filename = data[1]
                print(f"Filename: {filename}")
                send_data += f"@{filename}"
                client.send(send_data.encode(FORMAT))
            except IndexError:
                send_data = "ERROR@No file name was included."
                client.send(send_data.encode(FORMAT))

        # Directory command
        elif cmd == "DIR":
            client.send(send_data.encode(FORMAT))

        # Subfolder commands
        elif cmd == "SUBFOLDER":
            try:
                action = data[1].upper()
                if action == "CREATE" or action == "DELETE":
                    try:
                        dirname = data[2]
                        send_data += f"@{action}"
                        send_data += f"@{dirname}"
                        print(f"Action: {action}")
                        print(f"Directory: {dirname}")
                        client.send(send_data.encode(FORMAT))
                    except IndexError:
                        send_data = "ERROR@No directory name was included."
                        client.send(send_data.encode(FORMAT))
                else:
                    send_data = f"ERROR@Invalid subfolder action {action}."
                    client.send(send_data.encode(FORMAT))
            except IndexError:
                send_data = "ERROR@No action was included."
                client.send(send_data.encode(FORMAT))
        
        # Logout command
        elif cmd == "LOGOUT":
            client.send(send_data.encode(FORMAT))
            break

        else:
            send_data = f"ERROR@Invalid command {cmd}."
            client.send(send_data.encode(FORMAT))

    # Close the connection when loop broken
    print("Disconnected from server.")
    client.close()

if __name__ == "__main__":
    # Main function execution
    main()
