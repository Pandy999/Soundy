import glob
import schedule
import time
import os

def deleterecs():
    files = glob.glob('./Recordings/*')
    for f in files:
        os.remove(f)

schedule.every(30).minutes.do(deleterecs)
    
while True:
    schedule.run_pending()
    time.sleep(1)