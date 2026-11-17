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
