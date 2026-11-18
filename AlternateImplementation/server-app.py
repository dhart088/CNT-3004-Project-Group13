import os
import socket
import threading
from pathlib import Path
import struct


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

            # check if the file exist and can be uploaded
            filename = data[1]
            if not (basePath / filename).is_file():

                #full path of upload file
                # [***] cur_path
                create_path = basePath / filename

                # b"" is an empty bytes object
                raw_size = b""
                # get the first 8 bytes
                while len(raw_size) < 8:
                    raw_size += conn.recv(8 - len(raw_size))
                # unpack the first 8 bytes "raw_size" to find the total expected file size in bytes
                total_expected_size = struct.unpack("!Q", raw_size)[0]

                # get the file until the expected bytes are read
                received_size = 0
                with open(create_path, "wb") as f:
                    while received_size < total_expected_size:
                        # cap the intake at the smaller of either the buffer size or the remaining bits to read
                        chunk_size = min(SIZE, total_expected_size - received_size)
                        chunk = conn.recv(chunk_size)
                        if not chunk:
                            break
                        f.write(chunk)
                        # update the received with each chunk
                        received_size += len(chunk)

                # print("File transfer complete")
                conn.send(f"OK@{filename} uploaded successfully. ".encode(FORMAT))
            else:
                send_data = f"ERROR@{filename} already exists."
                conn.send(send_data.encode(FORMAT))



        elif cmd == "DOWNLOAD":
            filename = data[1]
            if (basePath / filename).is_file():

                size_in_bytes = os.path.getsize(basePath / filename)
                conn.sendall(struct.pack("!Q", size_in_bytes))  # send 8 byte file size header

                with open(basePath / filename, "rb") as f:
                    conn.sendfile(f)
                send_data += f"{filename} downloaded successfully."

            else:
                # send back 0 bytes because there is no file to send
                conn.sendall(struct.pack("!Q", 0))
                send_data = f"ERROR@{filename} Not found."

            conn.send(send_data.encode(FORMAT))



        elif cmd == "ERROR":
            # Why does the client need to send error to server, for server to send back the same error message?
            # conn.send("PASS@CONTINUE".encode(FORMAT))

            send_data = f"ERROR@{data[1]}"
            conn.send(send_data.encode(FORMAT))


        # Generic error
        else:
            conn.send("ERROR@An error occurred.".encode(FORMAT))



    print(f"{addr} disconnected.")
    conn.close()


def main():
    # IP = input("Enter an IP to listen on: ")
    # PORT = int(input("Enter a port to listen on: "))
    IP = "localhost"
    PORT = 4450
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


