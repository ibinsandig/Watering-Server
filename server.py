from flask import Flask
from routes.main import main_routes
import time
import paho.mqtt.client as mqtt
from flask_socketio import SocketIO
import threading


app = Flask(__name__, static_url_path='/static')
app.register_blueprint(main_routes)
socketio = SocketIO(app)

MQTT_BROKER = 'localhost'
MQTT_PORT = 1883
MQTT_TOPIC_SUB = 'watering/status'
MQTT_TOPIC_PUB = 'watering/control'

# MQTT Callback functions
def on_connect(client, userdata, flags, rc):
    print(f"Connected to MQTT Broker with result code {rc}")
    client.subscribe(MQTT_TOPIC_SUB)

def on_message(client, userdata, msg):
    print(f"Received message: {msg.payload.decode()} on topic {msg.topic}")
    # Emit the received data to all connected web clients
    socketio.emit('mqtt_message', {'topic': msg.topic, 'payload': msg.payload.decode()})

# Set up MQTT client


# Connect to MQTT broker
def connect_mqtt():
    mqtt_client = mqtt.Client()
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message 
    mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
    mqtt_client.loop_start()            

threading.Thread(target=connect_mqtt).start()
 
if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=3000)