""" 
Copyright 2019 Michael Galde,
file: honeypot.py
So this is used to monitor the network and look for conenctions on Port 23
"""
import sys
import argparse
import yagmail
import datetime
import time
from socket import socket, AF_INET, SOCK_STREAM

VERSION = '0.5 Mikes Fun Version'
welcome = b"Secret Server login: "

def send_email(src_address):
    """ This sends a email from a gmail account so I am alerted """
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    contents = ("Port 23 was accessed by: " + (src_address) + " at: " + (st))
    print (contents)
    yagmail.SMTP('insertemailhere@gmail.com').send('insertemailhere@gmail.com', 'HONEYPOT ALERT!', contents)
    pass

def telnet(address,port=23):
    """ create a listening port """
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
            if data == b'\r\n':
                pass
                ski.close(2)
                sys.exit()
    except: 
        ski.close()
        sys.exit()
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Mikes Quick Honeypot',
                                 epilog='Version: ' + str(VERSION))
    parser.add_argument('-a','--address',help='Use your IP address, the one you want to scan',action='store', required=True)   
    args = parser.parse_args()
    print ("Ready...")
    telnet(args.address)
        
