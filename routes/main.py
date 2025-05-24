from flask import Blueprint, render_template, request, jsonify
import mysql.connector
import paho.mqtt.publish as publish

main_routes = Blueprint('main_routes', __name__, url_prefix='/')

received_data = []  # Store received MQTT messages

@main_routes.route('/')
def index():
    return render_template('index.html')

@main_routes.route('/info')
def test():
    return render_template('info.html')

@main_routes.route('/control')
def control():
    return render_template('control.html')

@main_routes.route('/watering')
def watering():
    return render_template('watering.html')

# mqtt data send

@main_routes.route('/api/pump-control', methods=['POST'])
def pump_control():
    data = request.get_json()
    action = data.get('action')

    if action not in ['on', 'off']:
        return jsonify({'status': 'error', 'message': 'Ungültige Aktion'}), 400

    # ⬇️ Hier kannst du MQTT oder GPIO aufrufen
    print(f"Pumpe soll geschaltet werden: {action}")  # Zum Debuggen

    # Beispiel MQTT (nur wenn du publish brauchst):
    # import paho.mqtt.publish as publish
    publish.single("watering/control", action, hostname="localhost")  # ggf. IP anpassen

    return jsonify({'status': 'success', 'action': action})

#mqtt data grab

@main_routes.route('/get_mqtt_data')
def get_mqtt_data():
    return jsonify({'data': received_data})


# database data
@main_routes.route('/api/latest-data')
def latest_data():
    conn = mysql.connector.connect(
        host='localhost',
        user='sflask',
        password='12345678',
        database='flask_server'
    )
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM wetness ORDER BY id DESC LIMIT 1")
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    
    if result:
        return jsonify(result)
    else:
        return jsonify({"topic": "", "payload": "", "timestamp": ""})

