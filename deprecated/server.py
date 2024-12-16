import socket
from _thread import *
import pickle
import sys
from objects import *
from sprites import *


server = "172.16.100.80"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)
print("Waiting for a connection, Server Started")


players = [
    {"x" : 200,
     "y" : 401,
     "hit" : False,
     "stun" : False,
     "health" : 100,
},
           ]

def threaded_client(conn, player):
    conn.send(pickle.dumps(players[player]))
    reply = ""
    while True:
        try:
            data = pickle.loads(conn.recv(2048*2))
            players[player] = data

            if not data:
                print("Disconnected")
                break
            else:
                if player == 1:
                    reply = players[0]
                else:
                    reply = players[1]

                print("Received: ", data)
                print("Sending : ", reply)

            conn.sendall(pickle.dumps(reply))
        except:
            break

    print("Lost connection")

    conn.close()

def threadedWaiting(conn, player):
    while True:
        try:
            conn.sendall(str.encode("Please wait, searching for player."))

        except:
            pass




connectedPlayers = 0
currentPlayer = 0
while True:
    conn, addr = s.accept()

    print("Connected to:", addr)

    if connectedPlayers == 2:
        start_new_thread(threaded_client, (conn, 0))
        start_new_thread(threaded_client, (conn, 1))
    elif connectedPlayers == 1:
        start_new_thread(threadedWaiting, (conn, currentPlayer))



    connectedPlayers += 1
    currentPlayer += 1


