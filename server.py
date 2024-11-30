import socket
import _thread
import sys

server = ""
port = 5555 # Random Port, its a safe one because NO ONE uses it

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)