PiLCD v1.0
=======

Python scripts for interfacing with the [Adafruit 16x2 LCD + Keypad Kit](http://learn.adafruit.com/adafruit-16x2-character-lcd-plus-keypad-for-raspberry-pi/overview) for Raspberry Pi.

Adafruit invests time and resources providing this open source code, please support Adafruit and open-source hardware by purchasing products from Adafruit!

Written by Dennis Mojado and based on code by Collin Cunningham for Adafruit Industries. BSD license, all text above must be included in any redistribution

This project depends on [configuring your Pi for i2c](http://learn.adafruit.com/adafruits-raspberry-pi-lesson-4-gpio-setup/configuring-i2c) and having installed the [Adafruit Raspberry Pi Python Code](https://github.com/adafruit/Adafruit-Raspberry-Pi-Python-Code) in the pi user home directory (See line 5 of PiLCD.py to change Adafruit path).

Oh yeah, this code also displays secondary screen info (down button) of Bitstamp's bitcoin price ticker. This refreshes every 60 seconds. I left this in here because I find it personally useful, but can also be a template for accessing other JSON-based API data.

To download this project, log into your Pi with Internet accessibility and type: git clone https://github.com/denmojo/PiLCD.git


Configure Auto-start
-------------
In order for this code to be helpful on startup, it should run when the Pi is powered on.

To do this, you must add the following lines ABOVE "exit 0" in the Pi's /etc/rc.local

`cd /home/pi/PiLCD`
`python PiLCD.py &`

So for example the /etc/rc.local will look like this:

    #!/bin/sh -e
    #
    # rc.local
    #
    # This script is executed at the end of each multiuser runlevel.
    # Make sure that the script will "exit 0" on success or any other
    # value on error.
    #
    # In order to enable or disable this script just change the execution
    # bits.
    #
    # By default this script does nothing.

    # Print the IP address
    _IP=$(hostname -I) || true
    if [ "$_IP" ]; then
      printf "My IP address is %s\n" "$_IP"
    fi

    cd /home/pi/PiLCD
    python PiLCD.py &

    exit 0

Naturally, reference where you cloned the project if it is in a different location on your Pi filesystem.


Changes
-------------

Version 1.0
- Initial release
