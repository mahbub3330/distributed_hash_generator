import socket
import threading
import json
import time
IP = socket.gethostbyname(socket.gethostname())
PORT = 5579
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8"
DISCONNECT_MSG = "!DISCONNECT"
# for block generate

T = "0421312027"
firstKey = 0
lastKey = 2**22 - 1
blockWiseKeySpace = []
blockNo = [0]
clientList = {}
outputList = []
startTime = [0]
for block in range(0, 1024):
    blockWiseKeySpace.append([firstKey, lastKey])
    firstKey += 2**22
    lastKey += 2**22



def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    
    connected = True
    while connected:
        msg = conn.recv(SIZE).decode(FORMAT)
        #print(msg)
        if msg == DISCONNECT_MSG:
            connected = False
        elif msg == "BLOCK_REQUEST":
            print(f"[{addr}] {msg}")
            # msg = f"Msg received: {msg}"
            if(int(blockNo[0]) < 1024):
                msg = json.dumps({
                   "client": clientList[addr],
                    "block_no" : blockNo[0],
                    "range" : blockWiseKeySpace[blockNo[0]],
                    "t" : T
                })
                blockNo[0] = blockNo[0]+1
            
                conn.send(msg.encode(FORMAT))
            
        elif (msg == "END_BLOCK" or msg == "END_BLOCKBLOCK_REQUEST"):
            f = open("client1.txt", "a")
            f.write("Number of client :" +  str(threading.activeCount() - 1))
	    
            print("number of client :", threading.activeCount() - 1)
            #print(f"[{addr}] {msg}")
            for output in outputList:
                f.write(f'\n{output}')
                print(output)
            print("Time = %s seconds" % (time.time() - startTime[0]))
            requiredTime = "Time :" + str(time.time() - startTime[0])
            f.write(f'\n{requiredTime}')
            
            f.close()
            connected = False
        else: 
            #print(f"[{addr}] {msg}")
            outputList.append(msg)

    conn.close()

def main():
    print("[STARTING] Server is starting...")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen()
    print(f"[LISTENING] Server is listening on {IP}:{PORT}")


    while True:
        conn, addr = server.accept()
        clientList[addr] = threading.activeCount()
        if(threading.activeCount() == 1):
            print('hitted')
            startTime[0] = time.time()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        clientNo = threading.activeCount() - 1
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")

if __name__ == "__main__":
    main()
