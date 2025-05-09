from flask import Flask, request, jsonify
from routes.main import main_routes
import time
# import paho.mqtt.client as mqtt
import flask_mqtt as Mqtt


app = Flask(__name__, static_url_path='/static')
app.register_blueprint(main_routes)

from flask import Flask, request, jsonify
from flask_mqtt import Mqtt
from routes.main import main_routes

app = Flask(__name__, static_url_path='/static')
app.register_blueprint(main_routes)

# MQTT Konfiguration
app.config['MQTT_BROKER_URL'] = 'test.mosquitto.org'  
app.config['MQTT_BROKER_PORT'] = 1883
app.config['MQTT_USERNAME'] = ''
app.config['MQTT_PASSWORD'] = ''
app.config['MQTT_KEEPALIVE'] = 60
app.config['MQTT_TLS_ENABLED'] = False

mqtt = Mqtt(app)

# Beispiel-Callback
@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    print(f"MQTT-Nachricht erhalten: {message.topic} – {message.payload.decode()}")

@app.route('/')
def index():
    return 'Server läuft'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3000, threaded=True)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3000, threaded=True)
