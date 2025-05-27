from flask import Flask
from routes.main import main_routes # type: ignore
import time
import paho.mqtt.client as mqtt
from flask_socketio import SocketIO
import threading
from db.datab import insert_data_flaskiot # type: ignore
import mysql.connector # type: ignore

app = Flask(__name__, static_url_path='/static')
app.register_blueprint(main_routes)
socketio = SocketIO(app)

"""Konfiguration des MQTT-Brokers und der Topics"""
MQTT_BROKER = 'localhost'
MQTT_PORT = 1883
MQTT_TOPIC_SUB = 'watering/status'
MQTT_TOPIC_PUB = 'watering/control'

"""Subscriben des MQTT-Topics"""
def on_connect(client, userdata, flags, rc):
    status = {
        0: "Erfolgreich verbunden",
        1: "Fehler: Falsche Protokollversion",
        2: "Fehler: Ungültige Client-ID",
        3: "Fehler: Server nicht verfügbar",
        4: "Fehler: Falsche Zugangsdaten",
        5: "Fehler: Nicht autorisiert"
    }
    print(f"MQTT Verbindungsstatus: {status.get(rc, 'Unbekannter Fehler')}")
    
    if rc == 0:
        client.subscribe(MQTT_TOPIC_SUB)
        print(f"Subscribed to topic: {MQTT_TOPIC_SUB}")

def on_message(client, userdata, msg):
    payload = msg.payload.decode()
    print(f"Received message: {payload} on topic {msg.topic}")
    
    # Speichern in MariaDB über die externe Datei
    insert_data_flaskiot(msg.topic, payload)
    
    # Weiterleiten der Nachricht an Web-Clients
    socketio.emit('mqtt_message', {
        'topic': msg.topic,
        'payload': payload
    })

#            # Set up MQTT client
#            on_connect

"""Verbinden mit dem MQTT-Broker in einer unendlichen Schleife"""
def connect_mqtt():
    try:    
        mqtt_client = mqtt.Client()
        mqtt_client.on_connect = on_connect
        mqtt_client.on_message = on_message 
        mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
        mqtt_client.loop_start()        
    except Exception as e:
        print(f"Fehler beim Verbinden zum MQTT-Broker: {e}")
        print("Versuche erneut in 5 Sekunden...")
        time.sleep(5)
        connect_mqtt()
        
threading.Thread(target=connect_mqtt).start()
 
if __name__ == '__main__':
    socketio.run(app, allow_unsafe_werkzeug=True, host='0.0.0.0', port=3000)