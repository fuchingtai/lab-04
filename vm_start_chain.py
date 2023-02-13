import paho.mqtt.client as mqtt
import time
from datetime import datetime
import socket

def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))

#Custom message callback.
def on_message_from_pong(client, userdata, message):
    print("Start recieved: "+message.payload.decode())
    my_interger_recieve = int(message.payload.decode())
    my_interger_recieve = my_interger_recieve+1
    time.sleep(2)
    client.publish("fuv/ping", f"{my_interger_recieve}")

def on_message(client, userdata, msg):
    print("Default callback - topic: " + msg.topic + "   msg: " + str(msg.payload, "utf-8"))



if __name__ == '__main__':
    #starting number
    my_integer_start = 69
    #create a client object
    client = mqtt.Client()
    
    #attach the on_connect() callback function defined above to the mqtt client
    client.on_connect = on_connect
    """Connect using the following hostname, port, and keepalive interval (in 
    seconds). We added "host=", "port=", and "keepalive=" for illustrative 
    purposes. You can omit this in python. For example:
    
    `client.connect("eclipse.usc.edu", 11000, 60)` 
    
    The keepalive interval indicates when to send keepalive packets to the 
    server in the event no messages have been published from or sent to this 
    client. If the connection request is successful, the callback attached to
    `client.on_connect` will be called."""

    #Connect to the RPI
    client.connect(host="192.168.1.26", port=1883, keepalive=60)
    
    #subscribe to PONG
    client.subscribe("fuv/pong")

    #Add the custom callbacks for PONG
    client.message_callback_add("fuv/pong", on_message_from_pong)

    #Start the entire process
    client.publish("fuv/ping", f"{my_integer_start}")

    """ask paho-mqtt to spawn a separate thread to handle
    incoming and outgoing mqtt messages."""
    client.loop_forever()
    time.sleep(1)
