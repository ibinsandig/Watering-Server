from flask import Flask, request, jsonify
from routes.main import main_routes
import time
# import paho.mqtt.client as mqtt           Wurde bei Installation von flask mqtt deinstalliern
import flask_mqtt as mqtt

app = Flask(__name__, static_url_path='/static')
app.register_blueprint(main_routes)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3000, threaded=True)
