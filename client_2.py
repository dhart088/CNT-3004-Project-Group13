import socket
import os
import struct
from pathlib import Path

IP = "localhost"
PORT = 4450
ADDR = (IP,PORT)
SIZE = 1024
FORMAT = "utf-8"
SERVER_DATA_PATH = "server_data"


def main():

    # connect to server
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)

    # base path or default folder for client
    base = Path.cwd() / "ClientResources"

    # get welcome message
    data = client.recv(SIZE).decode(FORMAT)
    cmd, msg = data.split("@")
    if cmd == "OK":
        print(f"{msg}")

    # command loop
    while True:

        # type client command
        data = input("> ")
        data = data.split(" ")
        cmd = data[0]

        # this was a default, nothing yet
        if cmd == "HELP":
            pass
        # close the connection from this client to the server
        elif cmd == "LOGOUT":
            # to use:
            #> LOGOUT
            client.send(cmd.encode(FORMAT))
            break

        # Shuts the server down and logs out
        elif cmd == "QUIT":
            # to use:
            #> QUIT
            client.send("QUIT".encode(FORMAT))
            break

        # Uploads a file to the server in the currently viewed directory
        elif cmd == "UPLOADFILE":
            # to use:
            #> UPLOAD name_of_file_i_want_to_upload.txt

            # send the command and filename to upload
            chosen_filename = data[1]

            # check if the file exists in ClientResources
            if (base / chosen_filename).is_file():
                cmd_full = cmd + "@" + chosen_filename
                client.send(cmd_full.encode(FORMAT))


                # prepare and send the byte header for placeholder file FILENAME2
                size_in_bytes = os.path.getsize(base / chosen_filename)
                client.sendall(struct.pack("!Q", size_in_bytes)) #send 8 byte file size header

                with open(base / chosen_filename, "rb") as f:
                    client.sendfile(f)

                print("File sent successfully.")
            else:
                print("File not found.")

        elif cmd == "DOWNLOADFILE":
            # to use:
            # client needs to send
            # > "DOWNLOAD@file_name_to_download.file_type_like_txt"

            # send the server the command and file to download
            create_path = base / data[1]
            client.send((cmd + "@" + data[1]).encode(FORMAT))

            # Read the 8-Byte file size header

            # b"" is an empty bytes object
            raw_size = b""
            # get the first 8 bytes
            while len(raw_size) < 8:
                raw_size += client.recv(8 - len(raw_size))
            # unpack the first 8 bytes "raw_size" to find the total expected file size in bytes
            total_expected_size = struct.unpack("!Q", raw_size)[0]

            # server returns 0 bytes if file not found
            if total_expected_size == 0:
                print("File not found.")
            else:
                # get the file until the expected bytes are read
                received_size = 0
                with open(create_path, "wb") as f:
                    while received_size < total_expected_size:
                        # cap the intake at the smaller of either the buffer size or the remaining bits to read
                        chunk_size = min(SIZE, total_expected_size - received_size)
                        # print(f"chunk_size = {chunk_size}\n received_size = {received_size}\n\n")
                        chunk = client.recv(chunk_size)
                        if not chunk:
                            break
                        f.write(chunk)
                        # update the received with each chunk
                        received_size += len(chunk)

                print("File Download complete")

        elif cmd == "DIR":
            # to use:
            #> DIR DOWN name_of_directory_i_want_to_go_down_into
            #> DIR UP NONE

            # This is the error check to ensure that every message is an appropriate length to send to the server
            # 1@2@3
            cmd_full = cmd
            for item in data[1:]:
                cmd_full += "@" + item
            for idx in range(3 - len(data)):
                cmd_full += "@NONE"

            client.send(cmd_full.encode(FORMAT))

        else:
            # to use:
            #> literally anything not included above
            print("Command Not found: ", cmd)


    print("Disconnected from the server.")
    client.close() ## close the connection

if __name__ == "__main__":
    main()
