import socket

IP = socket.gethostbyname("")
PORT = 4456 #port no should be same
ADDR = (IP, PORT)
FORMAT = "utf-8"
SIZE = 1024

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  #creating client server
    client.connect(ADDR)

    while True:
        data = client.recv(SIZE).decode(FORMAT) #data received from the server is decoded
        cmd, msg = data.split("@")              # because @ is used to spilt into command and message

        if cmd == "DISCONNECTED":
            print(f"[SERVER]: {msg}")
            break
        elif cmd == "OK":
            print(f"{msg}")                       #prints the msg received

        data = input("> ")
        data = data.split(" ") #data is split using " " i.e space
        cmd = data[0]

        if cmd == "HELP":
            client.send(cmd.encode(FORMAT))
        elif cmd == "LOGOUT":
            client.send(cmd.encode(FORMAT))
            break

        elif cmd == "LIST":
            client.send(cmd.encode(FORMAT))

        elif cmd == "DELETE":
            client.send(f"{cmd}@{data[1]}".encode(FORMAT))   #data[1] has the path of the file

        elif cmd == "UPLOAD":  #UPLOAD@filename@text
            path = data[1]

            with open(f"{path}", "r") as f:  #opening the file in read(r) mode as f and reading it in text variable
                text = f.read()
                                             #client_data/data.txt splits as [client_data,data.txt]
            filename = path.split("/")[-1]
            send_data = f"{cmd}@{filename}@{text}"
            client.send(send_data.encode(FORMAT))

    print("Disconnected from the server.")
    client.close()

if __name__ == "__main__":
    main()
