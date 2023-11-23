from machine import Pin, ADC, RTC, Timer
from umqtt.robust import MQTTClient
import json
import time
from boot import set_ntp_time 

class Sensor:
      # initialize sensor
      def __init__(self, pin) :
            self.pin = pin
            try:
                  self.adc = ADC(Pin(self.pin))
                  self.adc.atten(ADC.ATTN_11DB)  # set 11dB input attenuation
            except Exception as e:
                  print("Error initializing sensor:", e)

      # get current time in format YYYY-MM-DD HH:MM:SS
      # def get_current_time(self):
      #       try:
      #             year, month, day, _, hour, minute, second, _ = self.rtc.datetime()
      #             timestamp = '{:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}'.format(year, month, day, hour, minute, second)
      #             return timestamp
      #       except Exception as e:
      #             print("Error getting current time:", e)
      #             return None
      
      # moisture sensor function to return moisture data
      def moisture(self) :
        timestamp = set_ntp_time()
        try :
                self.dict = {'Raw': "{0} @ {1}" .format(self.adc.read(), timestamp ),
                    'Percent' : "{:.1f}% @ {}".format((self.adc.read() / 4095) * 100, timestamp ), 
                    'Volts': "{:.3f}V @ {}".format(3.3 * self.adc.read()/4095, timestamp)}
                return self.dict
        except Exception as e:
                print("Error getting moisture data:", e)
                return None


# Function to attempt to connect to the broker
def connect_to_broker():
    try:
        client.connect()
        print("Connected to broker successfully")
    except OSError as e:
        print("Failed to connect to broker: ", str(e))

# Function to publish messages
def publish_message(topic, message):
    try:
        client.publish(topic, message)
        print(f"Published to {topic}: {message}")
    except OSError as e:
        print(f"Failed to publish message: {str(e)}")
        # Reconnect to broker if publishing failed
        connect_to_broker()

# timer callback function
def timer_callback(timer):
    # get moisture data
    moisture_data = sensor.moisture()
    j = json.dumps(moisture_data)
    # publish moisture data
    publish_message(main_topic, j)
    
    # publish raw data
    raw_data = "Raw :" + str(moisture_data['Raw'])
    publish_message(raw_topic, raw_data)
    
    # publish percent data
    percent_data = "Percent :" + str(moisture_data['Percent'])
    publish_message(percent_topic, percent_data)
    
    # publish volts data
    volts_data = "Volts :" + str(moisture_data['Volts'])
    publish_message(volts_topic, volts_data)

def main() :
    global client, sensor, main_topic,raw_topic, percent_topic, volts_topic
    pin = 36
    unique_id = "6b56d771-8b20-43b7-a0df-cadbad7f4b40"
    main_topic = "yjjtopic/iot/moisture"
    raw_topic = main_topic + "/raw"
    percent_topic = main_topic + "/percent"
    volts_topic = main_topic + "/volts"
    mqtt_host = "test.mosquitto.org"
    # Initialize the MQTT client
    client = MQTTClient(unique_id, mqtt_host)
    
    # initialize sensor
    sensor = Sensor(pin)
    
    # connect to broker
    connect_to_broker()
    # publish moisture data every 10 seconds
    timer = Timer(0)
    timer.init(period=10000, mode=Timer.PERIODIC, callback=timer_callback)

if __name__ == "__main__":
    main()




