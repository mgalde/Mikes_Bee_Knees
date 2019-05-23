import os
import time
os.system('python rdp.py')
try:
    while True:
            print ("wait for 5 sec...")
            time.sleep(5)
            print ("Restarting...")
            os.system('python rdp.py')
except KeyboardInterrupt:
    print ("Quit")
except Exception as e:
    print ("Quit with error " + str(e))
