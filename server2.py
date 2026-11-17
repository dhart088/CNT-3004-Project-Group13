import socket
import threading

IP = "localhost"
PORT = 4450
ADDR = (IP,PORT)
SIZE = 1024
FORMAT = "utf-8"
SERVER_PATH = "server"
KEEP_ALIVE = True

#
import struct
from pathlib import Path

### to handle the clients
def handle_client (conn,addr):

    print(f"[NEW CONNECTION] {addr} connected.")
    conn.send("OK@Welcome to the server".encode(FORMAT))

    # Directory setup ==================================================================================================
    # base path or default folder, shouldn't go any higher than this only lower into subfolders
    base = Path.cwd() / "ServerResources"
    cur_dir = base
    # Directory setup ==================================================================================================

    while True:
        # get client messages
        data =  conn.recv(SIZE).decode(FORMAT)
        data = data.split("@")
        cmd = data[0]

        send_data = "OK@"

        # client initiated logout
        if cmd == "LOGOUT":
            break
        elif cmd == "QUIT":
            global KEEP_ALIVE
            KEEP_ALIVE = False
            break
        # Client initialed a file upload ===============================================================================
        elif cmd == "UPLOADFILE":
            #currently just downloads the file into the received_file bin.

            #now that directories are "Functioning" (barebones), client can now navigate to the directory and give the file name when calling "UPLOAD FILE"

            #if upload file, now extract filename and type
            # cmd = data[0]
            # file_name_to_upload = data[1]
            # ex: UPLOADFILE@quizanswers.txt

            #once ready ill update to new file with name update instead of just recieved_file.bin

            create_path = cur_dir / data[1]

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
            with open(create_path, "wb") as f:
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
        #  =============================================================================================================
        elif cmd == "DIR":

            # TO USE THIS THE CLIENT CURRENTLY NEEDS TO "SEND" THE MESSAGE IN FORMAT:
            #> "DIR@DOWN@Text"
            #> "DIR@UP@NONE"
            #> "DIR@LIST@NONE"
            # NONE is just a placeholder NEEDED until input checks are in place so 3 inputs are currently required, for commands that want 2
            # the sever then splits and does what it needs to
            # The client can type the message with " " spaces or anything BUT MUST SEND it in this format with @ between command words to the server

            if data[1] == "DOWN":
                # how to Navigate DOWN using the / operator
                # destination_dir = base / "Video" / "Text"
                # puts you in the "Text" subfolder following the path of /

                # OR

                # using a dictionary of subfolder paths as the key pair is an easy way to navigate [***]
                # subfolders = ["Video", "Text"]
                # destination_dir = base.joinpath(*subfolders)
                # put you in subfolders in the order of the array, ending in "Text"

                # DIR@DOWN@Text
                cur_dir = cur_dir / data[2]

            elif data[1] == "UP":
                print("UP command")
                # Up doesn't need additional info from client, just get the parent dir
                # Navigate UP using .parent

                # check before it gets higher than base/ServerResources
                cur_dir = cur_dir.parent

            #elif data[1] == "LIST":
            # List immediate files and folders [***]
            #if they use dir, display the new cur_dir
            for item in cur_dir.iterdir():
                if item.is_dir():
                    print(f"Folder: {item.name}")
                elif item.is_file():
                    print(f"File: {item.name}")


    # final statement before client thread dies
    print(f"{addr} disconnected")
    conn.close()


def main():
    print("Starting the server")
    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM) ## used IPV4 and TCP connection
    server.bind(ADDR) # bind the address
    server.listen() ## start listening
    print(f"server is listening on {IP}: {PORT}")
    global KEEP_ALIVE
    while KEEP_ALIVE:
        conn, addr = server.accept() ### accept a connection from a client
        thread = threading.Thread(target = handle_client, args = (conn, addr)) ## assigning a thread for each client
        thread.start()


if __name__ == "__main__":
    main()

