#! /usr/bin/python
# Threading section written by Dan Mandle http://dan.mandle.me September 2012
# modified by Bill Ballard January 2017 for GPS tracking files
# and to add Pimoroni Scroll pHAT display of speed May 2017
# License: GPL 2.0

# load all the modules we will need

from gps import *
import datetime
import time
import random
import threading
import scrollphat

# initialize some variables

gpsd = None                     # setting the global variable
first = True                    # first pass will set filenames
tzfix = time.altzone/3600       # time zone doesn't change
scrollphat.set_brightness(128)  # bright for daylight display

# initialize thread, we don't use all data

class GpsPoller(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        global gpsd                     # bring it in scope
        gpsd = gps(mode=WATCH_ENABLE)   # starting the stream of info
        self.current_value = None
        self.running = True             # setting the thread running to true

    def run(self):
        global gpsd
        # this will continue to loop and grab EACH set of 
        # gpsd info to clear the buffer and prevent overruns
        while gpsp.running:
            gpsd.next() 

# the real part of the program

if __name__ == '__main__':
    gpsp = GpsPoller()          # create the thread
    try:
        gpsp.start()            # start it up
        while True:             # infinite loop

# It may take a a while to get good data, ignore until a fix is present
# and mode > 1
 
            if (gpsd.fix.mode) > 1:
                utc = gpsd.utc  # load the utc time

# create and open track files for today, use utc date as we don't have
# internet available to set date, correct date for your time zone 

                if (first):     # first pass generate filenames

# correct date from UTC to local, grab correct characters from utc string

                    lclhrs = int(utc[11:13])-tzfix
                    lclday = int(utc[8:10])

                    if (lclhrs<0):      # might need to correct to yesterday
                        lclday=lclday-1
                    elif (lclhrs>23):   # or tomorrow
                        lclday=lclday+1

# now fix up local day string for filename

                    if (lclday<10): 
                        todayname=utc[0:8]+str(0)+str(lclday)
                    else: 
                        todayname=utc[0:8]+str(lclday)
# dat file for future uses has additional data
                    fname = ("/home/pi/"+todayname+"-track.dat")
# comma separated for Mathmatica or spreadsheet
                    fname2= ("/home/pi/"+todayname+"-latlon.csv")
# open as append in case we crashed and are restarting
                    trk = open(fname, 'a')
                    trk.write("date/time, latitude, longitude,"
                    " altitude, speed, track\n")
                    trk.close()
                    trk = open(fname2, 'a')
                    trk.write("latitude, longitude\n")
                    trk.close()
# done with first pass setup
                    first = False

# now load the data and convert some units

                lat = gpsd.fix.latitude
                lgt = gpsd.fix.longitude

# convert from meters to feet for this use

                alt = 3.281*gpsd.fix.altitude

# convert speed in m/s to knots as nautical use here

                speedkts = 1.944*gpsd.fix.speed

# display speed over ground on scroll pHAT fixed for speeds < 10 kts
# Speeds over 10 kts need to scroll the display. The initial offset of 10
# and extra 7 spaces in the string will allow a complete scroll.

                scrollphat.clear()
                kts = ("{0:0.1f}").format(speedkts)
                if (speedkts < 10.):
                    scrollphat.write_string(kts, 1)
                    scrollphat.update()
                    time.sleep(10)      # set to delta seconds between grabs
                else:
                    scrollphat.write_string(kts+"       ", 10)
                    len = scrollphat.buffer_len()
                    for i in range(len/2+1):
                        scrollphat.scroll()
                        time.sleep(0.3) #sets scrolling speed
                                        # no delay as scrolling takes the time
                track = gpsd.fix.track

# open in append mode and write data, then close files so a system
# crash won't prevent output

# but first correct time to right time zone

                lclhrs = int(utc[11:13])-tzfix
                if (lclhrs<0): lclhrs=lclhrs+24
                lcltm = str(lclhrs)+utc[13:19]

# build formatted output string
# for data file

                outs = ("{0:s}, {1:0.9f}, {2:0.9f}, {3:0.1f}, " 
                "{4:0.1f}, {5:0.0f}\n"
                ).format(lcltm, lat, lgt, alt, speedkts, track)
                trk = open(fname, 'a')
                trk.write(outs)
                trk.close()

# for comma separated file

                outs = ("{0:0.9f}, {1:0.9f}\n").format(lat, lgt)
                trk = open(fname2, 'a')
                trk.write(outs)
                trk.close()
            else:
                print "no fix"
                time.sleep(20)  # give it some time to acquire fix


    except (KeyboardInterrupt, SystemError, SystemExit): #reasons to stop
        gpsp.running = False
        gpsp.join()             # wait for the thread to finish
        scrollphat.clear()      # clear the display

# end of program
