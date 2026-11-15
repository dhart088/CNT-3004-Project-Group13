import os
import socket
import threading

IP = "localhost"
PORT = 4450
ADDR = (IP,PORT)
SIZE = 1024
FORMAT = "utf-8"
SERVER_PATH = "server"

#
import struct

# 4096 is test, 1024 is default autofill
# BUFFER_SIZE = 1024

### to handle the clients
def handle_client (conn,addr):

    print(f"[NEW CONNECTION] {addr} connected.")
    conn.send("OK@Welcome to the server".encode(FORMAT))




    while True:
        # get client messages
        data =  conn.recv(SIZE).decode(FORMAT)
        data = data.split("@")
        cmd = data[0]

        send_data = "OK@"

        # client initiated logout
        if cmd == "LOGOUT":
            break

#  ====================================================================================================================
        # Client initialed a file upload
        elif cmd == "UPLOADFILE":
            #currently just downloads the file into the received_file bin.
            #will soon make it create/update client defined files with names


            # Read the 8-Byte file size header

            # b"" is an empty bytes object
            raw_size = b""
            # get the first 8 bytes
            while len(raw_size) < 8:
                raw_size += conn.recv(8 - len(raw_size))
            # unpack the first 8 bytes "raw_size" to find the total expected file size in bytes
            total_expected_size = struct.unpack("!Q", raw_size)[0]

            # get the file until the expected bytes are read
            received_size = 0
            with open("received_file.bin", "wb") as f:
                while received_size < total_expected_size:
                    # cap the intake at the smaller of either the buffer size or the remaining bits to read
                    chunk_size = min(SIZE, total_expected_size - received_size)
                    # print(f"chunk_size = {chunk_size}\n received_size = {received_size}\n\n")
                    chunk = conn.recv(chunk_size)
                    if not chunk:
                        break
                    f.write(chunk)
                    # update the received with each chunk
                    received_size += len(chunk)

            print("File transfer complete")
#  ====================================================================================================================


    # final statement before client thread dies
    print(f"{addr} disconnected")
    conn.close()


def main():
    print("Starting the server")
    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM) ## used IPV4 and TCP connection
    server.bind(ADDR) # bind the address
    server.listen() ## start listening
    print(f"server is listening on {IP}: {PORT}")
    while True:
        conn, addr = server.accept() ### accept a connection from a client
        thread = threading.Thread(target = handle_client, args = (conn, addr)) ## assigning a thread for each client
        thread.start()


if __name__ == "__main__":
    main()

