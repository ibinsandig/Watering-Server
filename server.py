from flask import Flask
from routes.main import main_routes # type: ignore
import time
import paho.mqtt.client as mqtt
from flask_socketio import SocketIO
import threading
from db.insert_data_wetness import insert_data_wetness # type: ignore
from db.insert_data_pump import insert_data_pump # type: ignore
import mysql.connector # type: ignore

app = Flask(__name__, static_url_path='/static')
app.register_blueprint(main_routes)
socketio = SocketIO(app)

"""Konfiguration des MQTT-Brokers und der Topics"""
MQTT_BROKER = 'localhost'
MQTT_PORT = 1883
MQTT_TOPIC_SUB_MOISTURE = 'watering/status'
MQTT_TOPIC_SUB_PUMP = 'watering/pump'
MQTT_TOPIC_PUB_PUMP = 'watering/control'
MQTT_TOPIC_PUB_TRIGGER = 'watering/trigger'

"""Subscriben des MQTT-Topics"""
def on_connect(client, userdata, flags, rc):
    client.subscribe(MQTT_TOPIC_SUB_MOISTURE)
    client.subscribe(MQTT_TOPIC_SUB_PUMP)

def on_message(client, userdata, msg):
    if msg.topic == MQTT_TOPIC_SUB_MOISTURE:
        insert_data_wetness(msg.topic, msg.payload.decode())
    elif msg.topic == MQTT_TOPIC_SUB_PUMP:
        insert_data_pump(msg.topic, msg.payload.decode())
    socketio.emit('mqtt_message', {
        'topic': msg.topic,
        'payload': msg.payload
    })

"""Verbinden mit dem MQTT-Broker in einer unendlichen Schleife"""
def connect_mqtt():
    while True:
        try:    
            mqtt_client = mqtt.Client()
            mqtt_client.on_connect = on_connect
            mqtt_client.on_message = on_message 
            mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
            mqtt_client.loop_forever()
            break  # wenn die Verbindung erfolgreich ist, verlasse die Schleife    
        except Exception as e:
            print(f"Fehler beim Verbinden zum MQTT-Broker: {e}")
            print("Versuche erneut in 5 Sekunden...")
            time.sleep(5)
        
threading.Thread(target=connect_mqtt).start()
 
if __name__ == '__main__':
    socketio.run(app, allow_unsafe_werkzeug=True, host='0.0.0.0', port=3000)