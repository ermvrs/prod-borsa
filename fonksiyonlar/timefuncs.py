from datetime import datetime
def timestamptodate(ts):
    return datetime.fromtimestamp(ts / 1e3)

def getcurrentdate():
    now = datetime.now()
    return now.strftime("%d/%m/%Y %H:%M:%S")