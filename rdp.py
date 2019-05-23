""" 
Copyright 2019 Michael Galde,
file: rdp.py
So this is used to monitor the network and look for conenctions on RDP port 3389
"""
import sys
import argparse
import yagmail
import datetime
import time
from socket import socket, AF_INET, SOCK_STREAM

VERSION = '0.5 Mikes Fun Version'
welcome = b"NARI Server login: "
address = "localhost" #Change to your IP address 

def send_email(src_address):
    """ This sends a email from a gmail account so I am alerted """
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    contents = ("Port 3389 RDP was accessed by: " + (src_address) + " at: " + (st))
    print (contents)
    yagmail.SMTP('Your yagmail account').send('your email', 'HONEYPOT ALERT! - RDP', contents)
    pass

def rdp(address,port=3389):
    """ RDP Service create a listening port """
    try:
        ski=socket(AF_INET,SOCK_STREAM)
        ski.bind((address, port))
        ski.listen()
        conn,addr = ski.accept()
        print('ALERT! you have been visited by ' + addr[0])
        send_email(addr[0])
        """Send Alert Email"""
        conn.sendall(welcome)
        while True:
            data=conn.recv(1024)
            ski.close(2)
            sys.exit()
    except: 
        ski.close()
        sys.exit()

print("RDP monitor active")
rdp(address)
        
