import paho.mqtt.client as mqtt
import json

# Define the MQTT host and topic
MQTT_HOST = "test.mosquitto.org"
main_topic = "yjjtopic/iot/moisture"
raw_topic = main_topic + "/raw"
percent_topic = main_topic + "/percent"
volts_topic = main_topic + "/volts"

# Callback when client receives a CONNACK response from the server
def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code : {rc}")
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    if rc == 0:
        client.subscribe(main_topic)
        print("Subscription: 1")  # Indicate a successful subscription
        

# Callback when a PUBLISH message is received from the server
def on_message(client, userdata, msg):
    try:
        # Decode the JSON data
        myData = json.loads(msg.payload.decode('utf-8'))
        
        # check if the JSON data is empty
        # check if the JSON data has a dictionary
        # Convert the JSON data to plain sentences
        json_items = []
        timestamp = myData.get('timestamp') # get the timestamp from the JSON data
        if myData:
            print(f"\nReceived JSON data on topic: {msg.topic}")
            for key, value in myData.items():
                if isinstance(value, dict):
                  json_items.append(f"{key}:")
                  for key, value in value.items():
                      if key != 'timestamp':    
                        json_items.append(f"{key} : {value} @ {timestamp}")
                else:
                    if key != 'timestamp': 
                        json_items.append(f"{key} : {value} @ {timestamp}")
            for item in json_items:
                print(item)
        else:
            print("The JSON data is empty.")
    except Exception as e:
        print(f"Error in on_message: {e}")

# Create an MQTT client instance
client = mqtt.Client()

# Connect to the MQTT broker                                                                                 
try:
    client.connect(MQTT_HOST, 1883, 60)
except Exception as e:
    print(f"Error connecting to MQTT broker: {e}")
    
# Assign the on_connect and on_message callback functions
client.on_connect = on_connect
client.on_message = on_message

# Start the loop to process callback events
client.loop_forever()
  