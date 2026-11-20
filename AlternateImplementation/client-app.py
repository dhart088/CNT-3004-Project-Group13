import os
import socket
import struct
from pathlib import Path
from getpass import getpass
import hashlib
import analytics as an

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
        elif cmd == "PASS":
            #DO NOT REMOVE
            pass
        
        # Console input
        send_data = ""
        data = input("> ")
        data = data.split(" ")
        cmd = data[0].upper()
        send_data += cmd

        # # input checking
        #
        # cmd_full = ["@NONE", "@NONE", "@NONE"]
        # for idx, item in enumerate(data):
        #         cmd_full[idx] = "@" + item

        # Upload command
        if cmd == "UPLOAD":
            try:
                filename = data[1]
                if (basePath / filename).is_file():
                    an.startTime() # start timer for recording transaction
                    send_data += f"@{filename}"
                    client.send(send_data.encode(FORMAT))

                    #now send the file size
                    size_in_bytes = os.path.getsize(basePath / filename)
                    client.sendall(struct.pack("!Q", size_in_bytes))  # send 8 byte file size header
                    an.updateChunk(size_in_bytes) # updates the expected file size for recording the transaction
                    
                    # open and send the file
                    with open(basePath / filename, "rb") as f:
                        an.responseTime() # record response time for recording transaction
                        client.sendfile(f)
                    an.calculate("client", "up") # calculate and record successful transaction
                else:
                    send_data = f"ERROR@File {filename} does not exist."
                    client.send(send_data.encode(FORMAT))
            except IndexError:
                send_data = "ERROR@No file name was included."
                client.send(send_data.encode(FORMAT))

        # Download command
        elif cmd == "DOWNLOAD":
            try:
                filename = data[1]
                if (basePath / filename).is_file():
                    send_data = f"ERROR@File {filename} already exists."
                    client.send(send_data.encode(FORMAT))
                else:
                    an.startTime() # start timer for recording transaction
                    # send server download command
                    send_data += f"@{filename}"
                    client.send(send_data.encode(FORMAT))

                    # b"" is an empty bytes object
                    raw_size = b""
                    # get the first 8 bytes
                    while len(raw_size) < 8:
                        raw_size += client.recv(8 - len(raw_size))
                    # unpack the first 8 bytes "raw_size" to find the total expected file size in bytes
                    total_expected_size = struct.unpack("!Q", raw_size)[0]

                    # server returns 0 bytes if file not found
                    if total_expected_size == 0:
                        # file not found, server is already sending its error message
                        pass
                    else:
                        # get the file until the expected bytes are read
                        an.responseTime() # record response time for recording transaction
                        received_size = 0
                        with open(basePath / filename, "wb") as f:
                            while received_size < total_expected_size:
                                # cap the intake at the smaller of either the buffer size or the remaining bits to read
                                chunk_size = min(SIZE, total_expected_size - received_size)
                                chunk = client.recv(chunk_size)
                                if not chunk:
                                    break
                                f.write(chunk)
                                # update the received with each chunk
                                received_size += len(chunk)
                                an.updateChunk(chunk_size) # update file size for recording transaction
                    an.calculate("client", "down") # calculate and record successful transaction
            except IndexError:
                send_data = "ERROR@No file name was included."
                client.send(send_data.encode(FORMAT))

        # Delete command
        elif cmd == "DELETE":
            try:
                filename = data[1]
                send_data += f"@{filename}"
                client.send(send_data.encode(FORMAT))
            except IndexError:
                send_data = "ERROR@No file name was included."
                client.send(send_data.encode(FORMAT))

        # Directory command
        elif cmd == "DIR":

            try:
                send_data += "@" + data[1]
            except IndexError:
                send_data = "DIR@NONE"

            client.send(send_data.encode(FORMAT))

            dir_items = client.recv(SIZE).decode(FORMAT)
            dir_items = dir_items.split("@")

            for item in dir_items:
                print(item)

        # Subfolder commands
        elif cmd == "SUBFOLDER":
            try:
                if data[1] == "CREATE" or data[1] == "DELETE":
                    try:
                        send_data += f"@{data[1].upper()}"
                        send_data += f"@{data[2]}"
                        client.send(send_data.encode(FORMAT))
                    except IndexError:
                        send_data = "ERROR@No directory name was included."
                        client.send(send_data.encode(FORMAT))
                else:
                    send_data = f"ERROR@Invalid subfolder action {data[1]}."
                    client.send(send_data.encode(FORMAT))
            except IndexError:
                send_data = "ERROR@No action was included."
                client.send(send_data.encode(FORMAT))


        elif cmd == "DELETE":
            send_data = "DELETE@" + data[1]
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
