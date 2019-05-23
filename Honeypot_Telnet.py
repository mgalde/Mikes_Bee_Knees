import os
import time
os.system('python telnet.py')
try:
    while True:
            print ("wait for 5 sec...")
            time.sleep(5)
            print ("Restarting...")
            os.system('python telnet.py')
except KeyboardInterrupt:
    print ("Quit")
except Exception as e:
    print ("Quit with error " + str(e))
