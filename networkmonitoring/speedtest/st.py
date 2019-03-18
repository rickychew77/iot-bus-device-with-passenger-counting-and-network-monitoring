import os
import re
import subprocess
import time

response = subprocess.Popen('speedtest-cli --simple', shell=True, stdout=subprocess.PIPE).stdout.read()

ping = re.findall('Ping:\s(.*?)\s', response, re.MULTILINE)
download = re.findall('Download:\s(.*?)\s', response, re.MULTILINE)
upload = re.findall('Upload:\s(.*?)\s', response, re.MULTILINE)

ping[0] = ping[0].replace(',', '.')
download[0] = download[0].replace(',', '.')
upload[0] = upload[0].replace(',', '.')

speedtestcsv = '/home/pi/Desktop/networkmonitoring/speedtest/speedtest.csv'
    
with open (speedtestcsv, 'a') as a:
        if os.stat(speedtestcsv).st_size == 0:
            a.write('Date,Time,Ping (ms),Download (Mbit/s),Upload (Mbit/s)')
        
        a.write('\n{},{},{},{},{}'.format(time.strftime('%m/%d/%y'), time.strftime('%H:%M'), ping[0], download[0], upload[0]))

#print '\n{},{},{},{},{}'.format(time.strftime('%m/%d/%y'), time.strftime('%H:%M'), ping[0], download[0], upload[0])
