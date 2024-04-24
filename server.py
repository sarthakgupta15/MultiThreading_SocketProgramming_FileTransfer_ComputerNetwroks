import os
import socket         #to create a tcp socket connenction
import threading      #to create thread for each individual client to make the server concurrent

IP = socket.gethostbyname("")
PORT = 4456      #can use any port no. after 1024
ADDR = (IP, PORT) #tupple having 2 vslues
SIZE = 1024
FORMAT = "utf-8"  #to encode and decode the data that is send acroos the server
SERVER_DATA_PATH = "server_data"

"""
format of msg for client and server
CMD@msg
"""


def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    #send a msg to cleint using conn variable
    conn.send("OK@Welcome to the File Server".encode(FORMAT)) #encoding every text info using utf-8

    while True:
        data = conn.recv(SIZE).decode(FORMAT) #data received from the client
        data = data.split("@")
        cmd = data[0]

        if cmd == "LIST":
            files = os.listdir(SERVER_DATA_PATH)             #gives list of all the files inside the server data
            send_data = "OK@"    #to send msg to the client

            if len(files) == 0:
                send_data += "The server directory is empty"
            else:
                send_data += "\n".join(f for f in files)     #gives the names of the files present in the server in new line
            conn.send(send_data.encode(FORMAT))

        elif cmd == "UPLOAD":
            name, text = data[1], data[2]
            filepath = os.path.join(SERVER_DATA_PATH, name) #define the path where  the file will be uploaded
            with open(filepath, "w") as f:  # open the file in write mode to
                f.write(text)

            send_data = "OK@File uploaded successfully."
            conn.send(send_data.encode(FORMAT))

        elif cmd == "DELETE":
            files = os.listdir(SERVER_DATA_PATH)
            send_data = "OK@"
            filename = data[1]

            if len(files) == 0:
                send_data += "The server directory is empty"
            else:
                if filename in files:
                    os.system(f"rm {SERVER_DATA_PATH}/{filename}") #remove the file from the directory requested from the client
                    send_data += "File deleted successfully."
                else:
                    send_data += "File not found."

            conn.send(send_data.encode(FORMAT))

        elif cmd == "LOGOUT":
            break
        elif cmd == "HELP":
            data = "OK@"
            data += "LIST: List all the files from the server.\n"
            data += "UPLOAD <path>: Upload a file to the server.\n"
            data += "DELETE <filename>: Delete a file from the server.\n"
            data += "LOGOUT: Disconnect from the server.\n"
            data += "HELP: List all the commands."

            conn.send(data.encode(FORMAT))

    print(f"[DISCONNECTED] {addr} disconnected")
    conn.close()

def main():
    print("[STARTING] Server is starting")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  #creating the server AF_NET uses internet version 4 and
                                                                #SOCK_STREAM to establish a tcp connenction so that it is connenction oriented
    server.bind(ADDR)                                           #for binding the hostname(having IP and PORT)
    server.listen()
    print(f"[LISTENING] Server is listening on {IP}:{PORT}.")

    while True:
        conn, addr = server.accept()                        #server will accept the connention from client
        thread = threading.Thread(target=handle_client, args=(conn, addr)) #creating a seprate thread for each individual client
        # arg which the func handle_client takes are conn and addr . conn helps us to receive and send the data and addr is tupple having addr of the cliant on the network
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

if __name__ == "__main__":
    main()
