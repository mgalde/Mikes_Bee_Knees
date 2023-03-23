import sys
import argparse
import logging
import yagmail
import datetime
import time
from socket import socket, AF_INET, SOCK_STREAM

VERSION = '0.6 Mikes Fun Version'
welcome = b"Secret Server login: "

def send_email(src_address, email_account, email_password, email_recipient):
    """ This sends a email from a gmail account so I am alerted """
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    contents = ("Port 3389 RDP was accessed by: " + (src_address) + " at: " + (st))
    logging.info(contents)
    yagmail.SMTP(email_account, email_password).send(email_recipient, 'HONEYPOT ALERT! - RDP', contents)

def rdp(address,port):
    """ RDP Service create a listening port """
    try:
        ski=socket(AF_INET,SOCK_STREAM)
        ski.bind((address, port))
        ski.listen()
        conn,addr = ski.accept()
        logging.warning('ALERT! you have been visited by ' + addr[0])
        send_email(addr[0], args.email_account, args.email_password, args.email_recipient)
        conn.sendall(welcome)
        while True:
            data=conn.recv(1024)
            ski.close(2)
            sys.exit()
    except: 
        ski.close()
        sys.exit()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Create a honeypot for RDP services.')
    parser.add_argument('--address', type=str, default='localhost', help='IP address to listen on')
    parser.add_argument('--port', type=int, default=3389, help='Port number to listen on')
    parser.add_argument('--email_account', type=str, help='Email account for sending alerts')
    parser.add_argument('--email_password', type=str, help='Email account password for sending alerts')
    parser.add_argument('--email_recipient', type=str, help='Email recipient for sending alerts')
    args = parser.parse_args()

    logging.basicConfig(filename='rdp_honeypot.log', level=logging.WARNING, format='%(asctime)s %(levelname)s %(message)s')
    logging.warning('RDP monitor active')

    rdp(args.address, args.port)
