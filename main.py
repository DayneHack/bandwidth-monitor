import psutil as ps
import pandas as pd
from datetime import datetime
import time
import os.path


if not os.path.exists('bandwidth.csv'):
    attributes = ['date', 'MB_sent', 'MB_received', 'MB_total']
    df = pd.DataFrame(columns=attributes)
    df.to_csv('bandwidth.csv', index=False)

else:
    df = pd.read_csv('bandwidth.csv', index_col=[0])


bytesSent_init = ps.net_io_counters().bytes_sent
bytesReceived_init = ps.net_io_counters().bytes_recv
bytesTotal_init = bytesSent_init + bytesReceived_init

while True:

    bytesSent = ps.net_io_counters().bytes_sent
    bytesReceived = ps.net_io_counters().bytes_recv
    bytesTotal = bytesSent_init + bytesReceived_init

    bytesSent_diff = bytesSent - bytesSent_init
    bytesReceived_diff = bytesReceived - bytesReceived_init
    bytesTotal_diff = bytesSent_diff + bytesReceived_diff

    MBSent = bytesSent_diff / 1024 / 1024
    MBReceived = bytesReceived_diff / 1024 / 1024
    MBTotal = bytesTotal_diff / 1024 / 1024

    currTime = str(datetime.today())[11:16]
    currDate = str(datetime.today())[0:10]


    if currTime == '00:00':

        data = {'date': currDate, 'MB_sent': MBSent, 'MB_received': MBReceived, 'MB_total': MBTotal}
        
        new = pd.DataFrame([data])
        df = pd.concat([df, new], ignore_index=True)
        df.to_csv('bandwidth.csv')
        time.sleep(120)
      
