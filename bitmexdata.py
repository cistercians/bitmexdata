import os
import csv
import datetime
import time
import requests

field_names = ['timestamp', 'Open', 'High', 'Low', 'Close', 'Trades', 'Volume', 'VTR', 'VWAP', 'Distance']
csv_file = open('data.csv', 'w')

writer = csv.DictWriter(csv_file, fieldnames=field_names)
writer.writeheader()

while True:

    bitmex = requests.get('https://www.bitmex.com/api/v1/trade/bucketed?binSize=1m&partial=false&symbol=XBTUSD&count=1&reverse=true').json()

    timestamp = datetime.datetime.now()
    open = bitmex[0]["open"]
    high = bitmex[0]["high"]
    low = bitmex[0]["low"]
    close = bitmex[0]["close"]
    trades = bitmex[0]["trades"]
    volume = bitmex[0]["volume"]
    vtr = volume / trades
    vwap = bitmex[0]["vwap"]
    distance = close - vwap

    writer.writerow({'timestamp' : timestamp,
                     'Open': open,
                     'High': high,
                     'Low': low,
                     'Close': close,
                     'Trades': trades,
                     'Volume': volume,
                     'VTR': vtr,
                     'VWAP': vwap,
                     'Distance': distance})

    csv_file.flush()
    os.fsync(csv_file.fileno())

    # this line is optional, you can delete it.
    print('')
    print(str(timestamp))
    print('')
    print('VWAP: ' + str(vwap))
    print('Distance: ' + str(distance))
    print('VTR: ' + str(vtr))
    print('')

    time.sleep(60)
