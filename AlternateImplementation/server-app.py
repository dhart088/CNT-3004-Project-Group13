import os
import socket
import threading
from pathlib import Path
import struct
import analytics as an

SIZE = 1024
FORMAT = "utf-8"
SERVER_PATH = "server"

# Client handler
def handle_client (conn,addr):
    basePath = Path.cwd() / "ServerResources"
    passPath = Path.cwd() / "AccountInfo"
    cur_dir = basePath

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
            if not (cur_dir / filename).is_file():
                an.startTime() # begin timer for recording transaction
                #full path of upload file
                # [***] cur_path
                create_path = cur_dir / filename

                # b"" is an empty bytes object
                raw_size = b""
                # get the first 8 bytes
                while len(raw_size) < 8:
                    raw_size += conn.recv(8 - len(raw_size))
                # unpack the first 8 bytes "raw_size" to find the total expected file size in bytes
                total_expected_size = struct.unpack("!Q", raw_size)[0]

                # get the file until the expected bytes are read
                an.responseTime() # record response time for recording transaction
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
                        an.updateChunk(chunk_size) # update chunk size for recording transaction
                        
                an.calculate(SERVER_PATH, "up") # calculate and record successful transaction
                conn.send(f"OK@{filename} uploaded successfully. ".encode(FORMAT))
            else:
                send_data = f"ERROR@{filename} already exists."
                conn.send(send_data.encode(FORMAT))


        elif cmd == "DOWNLOAD":
            filename = data[1]
            if (cur_dir / filename).is_file():
                an.startTime() # begin timer for recording transaction
                
                size_in_bytes = os.path.getsize(cur_dir / filename)
                conn.sendall(struct.pack("!Q", size_in_bytes))  # send 8 byte file size
                an.updateChunk(size_in_bytes) # updates expected file size for recording transaction
                
                with open(cur_dir / filename, "rb") as f:
                    an.responseTime() # record response time for recording transaction
                    conn.sendfile(f)
                an.calculate(SERVER_PATH, "down") # calculate and record successful transaction
                send_data += f"{filename} downloaded successfully."

            else:
                # send back 0 bytes because there is no file to send
                conn.sendall(struct.pack("!Q", 0))
                send_data = f"ERROR@{filename} Not found."

            conn.send(send_data.encode(FORMAT))


        elif cmd == "ERROR":
            send_data = f"ERROR@{data[1]}"
            conn.send(send_data.encode(FORMAT))


        elif cmd == "SUBFOLDER":

            if data[1] == "CREATE":
                if not (cur_dir / data[2]).is_dir():
                    Path(cur_dir / data[2]).mkdir()
                    conn.send(f"OK@{data[2]} created successfully.".encode(FORMAT))
                else:
                    conn.send(f"ERROR@{data[2]} already exists.".encode(FORMAT))
            elif data[1] == "DELETE":
                try:
                    if (cur_dir / data[2]).is_dir():
                        Path(cur_dir / data[2]).rmdir()
                        conn.send(f"OK@{data[2]} deleted successfully.".encode(FORMAT))
                    else:
                        conn.send(f"ERROR@{data[2]} does not exist.".encode(FORMAT))
                except OSError:
                    conn.send(f"ERROR@{data[2]} is not empty.".encode(FORMAT))


        elif cmd == "DELETE":
            if (cur_dir / data[1]).is_file():
                (cur_dir / data[1]).unlink(missing_ok=True)
                conn.send(f"OK@{data[1]} deleted successfully.".encode(FORMAT))
            else:
                conn.send(f"ERROR@{data[1]} does not exist.".encode(FORMAT))


        elif cmd == "DIR":

            # TO USE THIS THE CLIENT CURRENTLY NEEDS TO "SEND" THE MESSAGE IN FORMAT:
            # > "DIR@Text
            # > "DIR@UP"
            # > "DIR"
            send_data = "PASS@NONE"
            if data[1] == "UP":
                if cur_dir != basePath:
                    cur_dir = cur_dir.parent
                else:
                    send_data = f"ERROR@already at highest directory"
            elif data[1] != "NONE":

                # DIR@Text
                if (cur_dir / data[1]).is_dir():
                    cur_dir = cur_dir / data[1]
                    send_data = f"OK@current directory is now {data[1]}"
                else:
                    send_data = f"ERROR@{data[1]} does not exist."

            send_dir = "\nFolders:"
            send_item = "@Files:"
            for item in cur_dir.iterdir():
                if item.is_dir():
                    send_dir += f"@Folder: {item.name}"
                elif item.is_file():
                    send_item += f"@File: {item.name}"
            send_dir += send_item

            # send dir list
            conn.send(send_dir.encode(FORMAT))

            #then status message
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


