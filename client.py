import socket
import json
import hashlib
import time
start_time = time.time()


IP = socket.gethostbyname(socket.gethostname())
PORT = 5579
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8"
DISCONNECT_MSG = "!DISCONNECT"

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)
    print(f"[CONNECTED] Client connected to server at {IP}:{PORT}")

    connected = True
    while connected:
       # msg = input("> ")
        msg = "BLOCK_REQUEST"

        client.send(msg.encode(FORMAT))

        if msg == DISCONNECT_MSG:
            connected = False
        else:
            # msg = client.recv(SIZE).decode(FORMAT)
            msg = client.recv(SIZE)
            data = json.loads(msg.decode(FORMAT))
            print(f"[SERVER] {data}")
            T=data.get('t')
            blockRange = data.get('range')
            lastThreeDigitOfT = T[-3:]
            S = '00' + lastThreeDigitOfT
            clientNo = data.get('client')
            blockNo = data.get('block_no')
            matchedString = []

            for key in range(blockRange[0], blockRange[1]):
                nonce = str(key)
                V = str(T) + str(nonce)
                M = hashlib.md5(V.encode("utf-8")).hexdigest()
                firstFiveOfM = str(M)[:5]

                if(str(S) == str(firstFiveOfM)):
                    clientName = "[client-" + str(clientNo) + "]" + str(M)
                    sendToServer = str(clientName)
                    client.send(sendToServer.encode(FORMAT))
                    matchedString.append(M)
                
            print(matchedString)   
            print("--- %s seconds ---" % (time.time() - start_time))
            if(blockNo == 1023):
                print("yes hitted")
                endMsg = "END_BLOCK"
                client.send(endMsg.encode(FORMAT))




if __name__ == "__main__":
    main()
