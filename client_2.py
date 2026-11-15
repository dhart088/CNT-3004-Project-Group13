import os
import socket


IP = "localhost"
PORT = 4450
ADDR = (IP,PORT)
SIZE = 1024
FORMAT = "utf-8"
SERVER_DATA_PATH = "server_data"

#
FILENAME = "25MB_Sample.txt"
FILENAME2 = "sample_text.txt"

import os
import struct


def main():


    # connect to server
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)

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
            client.send(cmd.encode(FORMAT))
            break

        elif cmd == "UPLOADFILE":
            # send the UPLOADFILE command to server
            client.send("UPLOADFILE".encode(FORMAT))

            # prepare and send the byte header for placeholder file FILENAME2
            size_in_bytes = os.path.getsize(FILENAME2)
            client.sendall(struct.pack("!Q", size_in_bytes)) #send 8 byte file size header

            with open(FILENAME2, "rb") as f:
                client.sendfile(f)

            print("File sent successfully.")


    print("Disconnected from the server.")
    client.close() ## close the connection

if __name__ == "__main__":
    main()
