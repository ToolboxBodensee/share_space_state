#! /usr/bin/python3
# -*- coding: utf-8 -*-

import socket
import urllib.request, json 

# development
debug = True

# define addresses
UDP_IP = "0.0.0.0" # Public IP Address from Toolbox
UDP_PORT = 5138 # used port for notification

# destinations:
UDP_DESTINATION = "info-display.tbbs.me"
UDP_DESTINATION_PORT = 5000

TCP_HOST = "treppeled.tbbs.me"
TCP_PORT = 5000

sock = socket.socket(socket.AF_INET, # Use Internet socket
                     socket.SOCK_DGRAM) # UDP
s = socket.socket(socket.AF_INET, # Use Internet socket
                     socket.SOCK_DGRAM) # UDP

# recieve udp packages 
sock.bind((UDP_IP, UDP_PORT))

while True:
    if debug: print("starting while True loop")
    data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
    if debug: print("received message:", data)

    # send udp
    sock.sendto(bytes("change", "utf-8"), (UDP_DESTINATION, UDP_DESTINATION_PORT))

    # read space state
    with urllib.request.urlopen("https://bodensee.space/spaceapi/toolboxbodenseeev.json") as url:
        data = json.loads(url.read().decode())

        # send udp packages
        s.connect((TCP_HOST, TCP_PORT))

        # try to get space state and send tcp
        try:
            if data['state']['open']:
                s.sendall(b'open')
                if debug: print("Toolbox is open")
            else:
                s.sendall(b'closed')
                if debug: print("Toolbox is closed")
            data = s.recv(1024)
            s.close()
        except: print("Failed to get space state or sending tcp")

