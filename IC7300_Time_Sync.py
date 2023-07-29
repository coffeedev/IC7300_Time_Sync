#!/usr/bin/env python

import time
import os
import serial
import struct
import datetime
import signal
import sys
import datetime


baudrate = 115200  #change to match your radio
# Keep this at Zero always because we any get the localtime from the PI.
gmtoffset = 0  #change to a negative or positive offset from GMT if you
#               want to use local time.  i.e. -5 for EST
serialport = "/dev/ttyUSB0"  # Serial port of your radios serial interface.

# Defining the command to set the radios time in hex bytes.
preamble = ["0xFE", "0xFE", "0x94", "0xE0", "0x1A", "0x05", "0x00", "0x95"]
postamble = "0xfd"
timeServer = "in.pool.ntp.org"

logFile = open('/home/pi/code/IC7300_Time_Sync/time_sync.log', 'a')


#########################
# Log messages should be time stamped
def timeStamp():
    t = time.time()
    s = datetime.datetime.fromtimestamp(t).strftime('%Y/%m/%d %H:%M:%S - ')
    return s

# Write messages in a standard format

def printMsg(s):
    str = timeStamp() + s + "\n" ;
    print (str)
    logFile.write(str)
    logFile.flush()

#def printMsg(s):
    #print (s)
    #print (timeStamp() + s + "\n")
    # fileLog.write(timeStamp() + s + "\n")

#########################
class IC7300SyncTime(object):
    
    def __init__(self):
        printMsg("inside IC7300SyncTime")
    
    def syncTime(self):
         try:
            printMsg("Getting localtime") 
            
            t = time.localtime()
            hours = time.strftime("%H")
            hours = int(hours) + gmtoffset
            if hours < 0:
                hours = 23 + hours
            if hours > 23:
                hours = 23 - hours
            hours = str(hours)

            if (len(hours) < 2):
                hours = "0" + str(hours)
            
            hours = "0x" + hours
            preamble.append(hours)

            minutes = (int(time.strftime("%M")) + 1)
            minutes = str(minutes)
            if (len(minutes) < 2):
                minutes = "0" + minutes
            minutes = "0x" + minutes
            preamble.append(minutes)
            preamble.append('0xFD')

            # Now I get the current computer time in seconds.  Needed to set the time only
            # at the top of the minute.
            seconds = int(time.strftime("%S"))
            printMsg("Now waiting for 00 seconds")
            # Now we wait for the top of the minute.
            lastsec = 1
            while(seconds != 0):
               t = time.localtime()
               seconds = int(time.strftime("%S"))
               if(seconds != lastsec):
                    lastsec = seconds
               time.sleep(.01)


            printMsg("Set the time now")
            # Now that we've reached the top of the minute, set the radios time!
            ser = serial.Serial(serialport, baudrate)

            count = 0
            while(count < 11):
                senddata = int(bytes(preamble[count], 'UTF-8'), 16)
                ser.write(struct.pack('>B', senddata))
                count = count +1

            ser.close()
            # All done.  The radio is now in sync with the computer clock.
            printMsg("Time set done successfully")
             
             
             
         except Exception as e:
            printMsg(e)
            printMsg('Could not sync time with IC 7300')   
             
         

class NTPSyncTime(object):
    

    def __init__(self):
        printMsg("inside NTPSyncTime")

    def syncTime(self):
         try:
            import ntplib
            client = ntplib.NTPClient()
            response = client.request("in.pool.ntp.org")
            os.system('date ' + time.strftime('%m%d%H%M%Y.%S',
                        time.localtime(response.tx_time)))
            printMsg("Time sync done")

         except Exception as e:
            printMsg(e)
            printMsg('Could not sync with time server : in.pool.ntp.org')


if __name__ == '__main__':

    printMsg("Starting: TimeSync : NTPSyncTime")
    try:

        st = NTPSyncTime()
        st.syncTime()
        printMsg("NTPsync done.")

    except Exception as error:
        printMsg("ERROR: NTPSyncTime: " + error)


    printMsg("Starting: TimeSync : IC7300SyncTime")
    try:

        tx = IC7300SyncTime()
        tx.syncTime()
        printMsg("IC7300TimeSync done.")

    except Exception as error:
        printMsg("ERROR: IC7300SyncTime: " + error)

    finally:
        logFile.close()
