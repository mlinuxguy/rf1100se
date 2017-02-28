# rf1100se
Arduino code and Odroid-C1 (or Raspberry PI) python code to control TI cc1100 and cc1101 transceivers.  Also known as: RF1100SE and RF1101SE

Many of the cheap cc1101 modules available online only work at 433mhz due to missing inductors and resistors on the board, make sure if you want frequencies other than 433Mhz that you see more than just 4 inductors near the antenna (that's 433mhz, it takes 6-8 for 915mhz).

I wrote both the arduino and Odroid python code for several reasons
For the Arduino:
   I couldn't find any CC1100 libraries for Arduino that were lean enough to use an OLED + their library on a Pro MINI
For the Odroid-C1 (or Raspberry PI)
   No python libraries were easily found, so I wrote my own.
   
The python code is setup to use a Odroid-C1 as a base-station and transmit a beacon at 433mhz.
The Arduino Pro Mini code is setup to receive the beacon and print to a tiny OLED the RSSI (signal strength) and the beacon number.
Using a battery on the Pro MINI you can then walk around to measure the distance you still receive the base station beacon.

Notes:   The python code has support for 915mhz and 433mhz, the Arduino code I only put constants in for 433mhz.  You can use the TI
RF studio to add your own frequencies.   However note that many of the cheap RF1100se boards available online do not have all the 
resistors to support frequencies other than 433mhz.

Notes:  The python code appears to be sensitive to timing around changing TI CC1100 modes, I put code in to try and deal with it.
Some further work around that area may be needed.
