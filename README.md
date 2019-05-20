# Mikes Quick Honeypot
A quick and simple honeypot that also allows you to be notified of a intrusion on your network 

So check it out, you want a honeypot and you want it quick and you want it simple

BAM here you go, check it out. I borrowed heavely from https://mindchasers.com/dev/net-python-socket and I encurage you to read that blog to get a stronger understanding of what this is doing. 

Ok so first off here is what you want to import
```python
import sys
import argparse
import yagmail
import datetime
import time
from socket import socket, AF_INET, SOCK_STREAM
```

you may need to pip install yagmail to send emails. It is really easy and I encurage you to do so


```python
VERSION = '0.5 Mikes Fun Version'
welcome = b"Secret Server login: "
```

These are setting some global objects, when you run the command it says what version it is. Simple self promotion and the welcome line is what the Telnet client will see

```python
def send_email(src_address):
    """ This sends a email from a gmail account so I am alerted """
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    contents = ("Port 23 was accessed by: " + (src_address) + " at: " + (st))
    print (contents)
    yagmail.SMTP('insertemailhere@gmail.com').send('insertemailhere@gmail.com', 'HONEYPOT ALERT!', contents)
    pass
```
This is setting up a email message that will send once it is called. It will be passed the address from the telnet definition. 

The email will need to be set up in your own keyring. You can set the username and password up but that is a little crazy. Add it to your keyring. 

you may need to run the following as well

```cmd
pip install keyring
```

then do the following commands

```python
python
>>> import yagmail
>>> yagmail.register('mygmailusername', 'mygmailpassword')
>>> exit()
```

Insert your gmail username and password here and add them to your keyring. 

Please do not use your password in your script. Take the extra steps.


Next we define the Telnet Honeypot

```python
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
```
This opens a connection socket and waits for a connection

Once a connection is made it sends a welcome message

The connection then waits for a interaction from the connecting client 


Now we gring it together into main

```python
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Mikes Quick Honeypot',
                                 epilog='Version: ' + str(VERSION))
    parser.add_argument('-a','--address',help='Use your IP address, the one you want to scan',action='store', required=True)   
    args = parser.parse_args()
    print ("Ready...")
    telnet(args.address)
    
```


So any questions??
