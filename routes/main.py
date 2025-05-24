from flask import Blueprint, render_template, request, jsonify
import mysql.connector
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

@main_routes.route('/get_mqtt_data')
def get_mqtt_data():
    return jsonify({'data': received_data})

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
