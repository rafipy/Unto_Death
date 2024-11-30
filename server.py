import socket
from _thread import *
import sys

server =  "192.168.100.189"
port = 5555 # Random Port, its a safe one because NO ONE uses it

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #TCP client, UDP's are very... very painful

try:
    s.bind((server, port))
    
except socket.error as e:
    str(e)
    
s.listen(2) # Check for 2 connections max
print("Waiting for connection, Server Started!")

def threaded_client(conn):
    conn.send(str.encode("Connected"))
    reply = ""
    
    while True:
        try:
            data = conn.recv(2048*2) #receives 4096 bits
            reply = data.decode("utf-8")
            
            if not data:
                print("Disconnected")
                break 
            else:
                print("Received: ", reply)
                print("Sending:", reply)
            
            conn.sendall(str.encode(reply))
        
        except:
            break
    print('Lost Connection')
    conn.close()
        
        

while True:
    conn, addr = s.accept() #accept any incoming connections and their address
    print("Connected to:", addr)
    
    start_new_thread(threaded_client, (conn,)) #creates a new thread, essentially adds another process to the background, for parallel running