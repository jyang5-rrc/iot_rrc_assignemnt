import network
import time
import webrepl
import ntptime
from machine import RTC


# Set Wifi
def do_connect():
    try:
        # Connect to WiFi
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        print('Connecting to network...')
        
        # check if wifi is connected,if not,connect to wifi
        while not wlan.isconnected():
            wlan.connect('Jun5678','526bannatyne')
            time.sleep(5)
        # print network config,including IP address    
        print('Network config:',wlan.ifconfig())
    except:
        print('Error connecting to wifi')
        pass

# Adjust time
def adjust_time(year, month, day, hour, delta_hours):
    """ Adjust the hour and handle day, month, and year changes. """
    hour += delta_hours
    while hour < 0:
        hour += 24
        day -= 1
        if day < 1:
            month -= 1
            if month < 1:
                month = 12
                year -= 1
            # Determine the number of days in the new month
            if month in [1, 3, 5, 7, 8, 10, 12]:
                day = 31
            elif month in [4, 6, 9, 11]:
                day = 30
            else:  # February
                # Check for leap year
                if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
                    day = 29
                else:
                    day = 28
    return year, month, day, hour

# Set time
def set_ntp_time():
    # Synchornize time using NTP
    try:
        ntptime.host = 'pool.ntp.org' # set host
        ntptime.settime() # set time
        year, month, day, _, hour, minute, second, _= RTC().datetime() # get current time
        
        # Adjust for CST time (UTC-6)
        year, month, day, hour = adjust_time(year, month, day, hour, -6)
        
        current_time = '{:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}'.format(year, month, day, hour, minute, second)
        return current_time
    except Exception as e:
        print('Error setting time:', str(e))
        pass

do_connect()
webrepl.start()
timestamp = set_ntp_time()
print('NTP current UTC-6 time:',timestamp) # print current time
