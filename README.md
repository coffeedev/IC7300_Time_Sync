# IC7300-Time-Sync
# Author : VU3GWN
# Date   : 10th March 2023

Features
 
1. Made the code modular to match Python coding standards
2. Added NTP time sync code before we sync time with 7300
3. Given steps in this file below to add the file in CRONTAB to run every 6 hours
4. Also provided are files that can be used to host this as a Linux service, but it won't run every 6 hours.
5. Super useful if you use RaspberryPI with your 7300 for DigiOps.
6. Requires Python 3.x +
7. Python script to sync the radio's clock with your computer via CAT commands.

Working description

Before we sync the localtime from Raspberrypi we will also attempt to sync the RaspberryPI time with the NTP pool.
That code is also integrated into the main python file.

To support that, you will need to run the following command

sudo pip install ntplib

At the top of the script (IC7300_Time_Sync.py) are a few variables you'll have to set.  

1. The serial device name your 7300 is at. Mine is set at 115200. Verify yours in the 7300 settings menu.
2. The rest of the script is commented and should be self-explainatory.  

Add this to crontab to run this script every 6 hours

run the following commands, one after the other

** sudo crontab -e **

once the editor opens, copy paste the below line, save and close

** 0 */6 * * * sudo python /home/pi/code/IC7300_Time_Sync/IC7300_Time_Sync.py **

once you exit, run this command to restart the cron service

** sudo service cron restart **


Thanks - vu3gwn@outlook.com
--------------------------------------------------------------------------
Original Code : https://github.com/loughkb/IC-7300-time-sync

