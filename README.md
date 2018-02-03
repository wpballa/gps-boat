# gps-boat
GPS tracking and mapping of sailing routes

Read the pdf for full instructions for both hardware and software

boat-gpsd.py works for the Pimoroni Scroll pHAT, now obsolete but still available

boat-gpsdhd.py works for the Pimoroni Scroll pHAT HD
Hardware assembly is identical
The only other changes needed, are to load the scrollphatHD library from Pimoroni and
sudo apt-get install python3-pip
pip3 install flake 
and to change the /etc/rc.local startup to point to the hd version of the program
