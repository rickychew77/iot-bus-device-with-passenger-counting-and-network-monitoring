import os
from gps import *
from time import *
import time
import threading
 
gpsd = None #seting the global variable
 
#os.system('clear') #clear the terminal (optional)
 
class GpsPoller():
  def __init__(self):
    #threading.Thread.__init__(self)
    global gpsd #bring it in scope
    gpsd = gps(mode=WATCH_ENABLE) #starting the stream of info
    self.current_value = None
    #self.running = True #setting the thread running to true
 
  def run(self):
    global gpsd
    while gpsp.running:
      gpsd.next() #this will continue to loop and grab EACH set of gpsd info to clear the buffer

class extract():
    def longitude(self):
        return gpsd.fix.longitude

    def latitude(self):
        return gpsd.fix.latitude

if __name__ == '__main__':
  gpsp = GpsPoller() # create the thread
  try:
    #gpsp.start() # start it up
    while True:
      #It may take a second or two to get good data
      #print gpsd.fix.latitude,', ',gpsd.fix.longitude,'  Time: ',gpsd.utc
      speedtestcsv = '/home/pi/Desktop/networkmonitoring/speedtest/speedtest.csv'
      
      print ' GPS reading'
      print '----------------------------------------'
      print 'latitude    ' , gpsd.fix.latitude
      print 'longitude   ' , gpsd.fix.longitude
      print 'time utc    ' , gpsd.utc,' + ', gpsd.fix.time
      print 'altitude (m)' , gpsd.fix.altitude
      print 'eps         ' , gpsd.fix.eps
      print 'epx         ' , gpsd.fix.epx
      print 'epv         ' , gpsd.fix.epv
      print 'ept         ' , gpsd.fix.ept
      print 'speed (m/s) ' , gpsd.fix.speed
      print 'climb       ' , gpsd.fix.climb
      print 'track       ' , gpsd.fix.track
      print 'mode        ' , gpsd.fix.mode
      print 'sats        ' , gpsd.satellites
      
      et = extract()
      #longi = gpsd.fix.longitude
      #lati = gpsd.fix.latitude
      #text = '{} {}'.format(et.longitude(longi), extract.latitude(lati))
      time = str(gpsd.utc) + ' + ' + str(gpsd.fix.time)
      print (time)
      print ('longitude: ' + str(et.longitude()))
      print ('latitude: ' + str(et.latitude()))
      with open (speedtestcsv , 'a') as n:
          if os.stat(speedtestcsv).st_size == 0:
                n.write('Date,Time,Ping (ms),Download (Mbit/s),Upload (Mbit/s)')
                
          n.write ('\n' + time  + ',' + str(et.longitude()) + ',' + str(et.latitude())) 

      gpsd.close()
      #time.sleep(5) #set to whatever
      exit()

  except (KeyboardInterrupt, SystemExit): #when you press ctrl+c
    #print "\nKilling Thread..."
    gpsp.running = False
    #gpsp.join() # wait for the thread to finish what it's doing
  print "Done.\nExiting."
 
