import datetime
import calendar
import logging
import random
import time

def log_gen(timestamp):
    connid = 0
    ts = timestamp
    tsnow = calendar.timegm(time.gmtime())
    while ts <= tsnow:
        tx = random.randint(0,10000)
        rx = random.randint(0,10000)
        connid+=1
        ts+=1
        yield "{\"level\":\"debug\",\"ts\":" + '{:d}'.format(ts) + ",\"conn_id\":" + '{:d}'.format(connid) + ",\"state\":\"closed\",\"Tx\":" + '{:d}'.format(tx) + ",\"Rx\":" + '{:d}'.format(rx) + "}"


start_time = time.time()

# Generates logs from specified date in epoch timestamp to current time.
values = log_gen(1582156799)

logging.basicConfig(filename='samples.log', filemode='w', format='%(message)s', level=logging.INFO)
logs = list()
cont = 0

for i in values:
    logs.append(i)
    cont+=1
    if cont == 86400:
        # logging in batches of 24 hrs
        logging.info("\n".join(logs))
        cont = 0
        logs = list()
if len(logs) > 0:
    logging.info("\n".join(logs))

# measuring execution time
print ("=======================================================================================")
print("--- Generation Completed in " +'{:f}'.format((time.time() - start_time)) + " seconds ---")
print ("=======================================================================================")
