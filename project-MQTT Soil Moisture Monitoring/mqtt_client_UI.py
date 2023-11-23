import threading
import tkinter as tk
from tkinter import scrolledtext
import paho.mqtt.client as mqtt
import json

# Define the MQTT host and topics
MQTT_HOST = "test.mosquitto.org"
main_topic = "yjjtopic/iot/moisture"
raw_topic = main_topic + "/raw"
percent_topic = main_topic + "/percent"
volts_topic = main_topic + "/volts"

# Initialize dictionary for topic textboxes
topic_textboxes = {}

# Function to update the UI with a new message
def update_ui(topic, message):
    if topic in topic_textboxes:
        textbox = topic_textboxes[topic]
        textbox.delete('1.0', tk.END)
        textbox.insert(tk.END, message)

# Callback when client receives a CONNACK response from the server
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        client.subscribe([(main_topic, 0), (raw_topic, 0), (percent_topic, 0), (volts_topic, 0)])
        update_ui(main_topic, "Subscribed to topics\n")
    else:
        update_ui(main_topic, f"Failed to connect with result code: {rc}\n")

# Callback when a PUBLISH message is received from the server
def on_message(client, userdata, msg):
    try:
        # Decode the JSON data
        payload = msg.payload.decode('utf-8')
        myData = json.loads(payload)
        message = json.dumps(myData, indent=2)
        update_ui(msg.topic, message)
    except json.JSONDecodeError:
        # If JSON data is malformed, just display the raw payload
        update_ui(msg.topic, payload)
    except Exception as e:
        update_ui(main_topic, f"Error in on_message: {e}\n")

# Create the main window
root = tk.Tk()
root.title("MQTT Client Subscriber")

# Create UI elements for each topic
for topic in [main_topic, raw_topic, percent_topic, volts_topic]:
    label = tk.Label(root, text=topic)
    label.pack()
    textbox = scrolledtext.ScrolledText(root, height=5, width=50)
    textbox.pack()
    topic_textboxes[topic] = textbox

# MQTT client setup
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# Threading function to run the MQTT client
def run_mqtt_client():
    try:
        client.connect(MQTT_HOST, 1883, 60)
        client.loop_start()
    except Exception as e:
        update_ui(main_topic, f"Error connecting to MQTT broker: {e}\n")

# Start the MQTT client in a separate thread
mqtt_thread = threading.Thread(target=run_mqtt_client, daemon=True)
mqtt_thread.start()

# Start the Tkinter event loop
root.mainloop()
