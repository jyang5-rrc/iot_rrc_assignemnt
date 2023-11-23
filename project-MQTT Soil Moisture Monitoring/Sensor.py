from machine import Pin, ADC, RTC
import time

class Sensor:
      
      # initialize sensor
      def __init__(self, pin) :
            self.pin = pin
            try:
                  self.adc = ADC(Pin(self.pin))
                  self.adc.atten(ADC.ATTN_11DB)  # set 11dB input attenuation
                  self.rtc = RTC()
            except Exception as e:
                  print("Error initializing sensor:", e)

      # get current time in format YYYY-MM-DD HH:MM:SS
      def get_current_time(self):
            try:
                  year, month, day, _, hour, minute, second, _ = self.rtc.datetime()
                  timestamp = '{:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}'.format(year, month, day, hour, minute, second)
                  return timestamp
            except Exception as e:
                  print("Error getting current time:", e)
                  return None
      
      # moisture sensor function to return moisture data
      def moisture(self) :
            try :
                  self.dict = {'raw': self.adc.read(),
                        'percent' : 100 * self.adc.read()/4095, 
                        'volts': 3.3 * self.adc.read()/4095,
                        'timestamp': self.get_current_time()}
                  return self.dict
            except Exception as e:
                  print("Error getting moisture data:", e)
                  return None
            
      
    
    #pin = 36