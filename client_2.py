import socket
import os
import struct
import time
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

        if cmd == "HELP":
            pass
        elif cmd == "LOGOUT":
            # to use:
            #> LOGOUT
            client.send(cmd.encode(FORMAT))
            break

        #  QUIT IS JUST FOR TESTING, FOR NOW IT CLEANLY SHUTS THE SERVER DOWN !!!! [***]
        elif cmd == "QUIT":
            # to use:
            #> QUIT

            #send logout
            client.send("QUIT".encode(FORMAT))
            client.close()

            # 0.5 second delay before reconnect
            time.sleep(0.5)

            # reconnect to server
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect(ADDR)

            # get welcome message
            data = client.recv(SIZE).decode(FORMAT)
            #logout again
            client.send("LOGOUT".encode(FORMAT))
            break


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
            # THIS NEEDS UPDATED, CAN TAKE ANY LEN THAT MATCHES ONE FROM THE SERVER, 3 is just easy testing
            if len(data) >= 3:
                cmd_full = cmd + "@" + data[1] + "@" + data[2]
                # Whatever changes above, THIS NEEDS TO BE FORMATED WITH @ between each input
                client.send(cmd_full.encode(FORMAT))

        else:
            # to use:
            #> literally anything not included above
            print("Command Not found: ", cmd)


    print("Disconnected from the server.")
    client.close() ## close the connection

if __name__ == "__main__":
    main()
