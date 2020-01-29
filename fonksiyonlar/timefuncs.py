from datetime import datetime
import time
def timestamptodate(ts):
    return datetime.fromtimestamp(ts / 1e3)

def getcurrentdate():
    now = datetime.now()
    return now.strftime("%d/%m/%Y %H:%M:%S")
def getcurrentts():
    return time.time() * 1000