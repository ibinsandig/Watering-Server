from flask import send_file, Blueprint, render_template, request, jsonify
import mysql.connector  # type: ignore
import paho.mqtt.publish as publish
import io
import matplotlib   # type: ignore
matplotlib.use('Agg')
import matplotlib.pyplot as plt # type: ignore
import pandas as pd # type: ignore
from db.insert_data_trigger import insert_data_trigger # am Anfang importieren

main_routes = Blueprint('main_routes', __name__, url_prefix='/')

received_data = []  # Speichern der empfangenen MQTT-Daten

"""Festlegen der Routen für die Startseite und die Steuerung"""
@main_routes.route('/')
def index():
    return render_template('index.html')

@main_routes.route('/control')
def control():
    return render_template('control.html')

"""Route für das Erhalten der aktuellen MQTT-Daten"""
@main_routes.route('/get_mqtt_data')
def get_mqtt_data():
    return jsonify({'data': received_data})

"""Route für das Abgreifen der letzten Feuchtigkeitsdaten aus der Datenbank"""
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

"""Route für das Plotten der Graphik moistureA"""
@main_routes.route('/moistureA-plot')
def moisture_plot():
    # Verbindung zu flask_server db
    conn = mysql.connector.connect(
        host='localhost',
        user='sflask',
        password='12345678',
        database='flask_server'
    )
    cursor = conn.cursor()

    cursor.execute("""
        SELECT payload, timestamp 
        FROM wetness 
        WHERE topic = 'watering/status' 
        ORDER BY id DESC 
        LIMIT 500
    """)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    data = []
    timestamps = []

    for payload, timestamp in reversed(rows):
        try:
            parts = payload.split(',')
            moisture_value = None
            
            # Suche spezifisch nach moistureA
            for p in parts:
                if p.strip().startswith('moistureA:'):
                    moisture_value = int(p.split(':')[1])
                    break
            
            # Nur hinzufügen wenn moistureA gefunden wurde
            if moisture_value is not None:
                data.append(moisture_value)
                timestamps.append(timestamp)
                
        except (ValueError, IndexError) as e:
            print(f"Fehler beim Parsen von moistureA: {payload} - {e}")
            continue

    # Limitiere auf die letzten 300 gültigen Einträge
    if len(data) > 300:
        data = data[-300:]
        timestamps = timestamps[-300:]

    if not data:
        # Erstelle leeren Plot wenn keine Daten vorhanden
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.text(0.5, 0.5, 'Keine moistureA Daten verfügbar', 
                horizontalalignment='center', verticalalignment='center', 
                transform=ax.transAxes, fontsize=14)
        ax.set_title("Analoge Moisture-Werte (moistureA)")
        ax.set_ylim(0, 1100)
    else:
        # den Plot erstellen
        df = pd.DataFrame({'timestamp': timestamps, 'moistureA': data})
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(df['timestamp'], df['moistureA'], color=(38/255, 138/255, 180/255), marker='o', markersize=3, linewidth=1)
        ax.set_title(f"Analoge Moisture-Werte (moistureA) - {len(data)} Datenpunkte")
        ax.set_xlabel("Zeit")
        ax.set_ylabel("Feuchtigkeit A (%)")
        ax.grid(True, alpha=0.3)
        ax.set_ylim(0, 1100)
        
        # Trigger-Wert holen
        conn = mysql.connector.connect(
            host='localhost',
            user='sflask',
            password='12345678',
            database='flask_server'
        )
        cursor = conn.cursor()
        cursor.execute("SELECT value FROM trigger_values ORDER BY id DESC LIMIT 1")
        trigger_result = cursor.fetchone()
        cursor.close()
        conn.close()
        if trigger_result and data:
            trigger_value = trigger_result[0]
            ax.axhline(trigger_value, color='red', linestyle='--', label=f'Trigger: {trigger_value}')
            ax.legend()
        
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Bild im Speicher speichern
    img = io.BytesIO()
    plt.savefig(img, format='png', dpi=100)
    plt.close(fig)
    img.seek(0)

    return send_file(img, mimetype='image/png')

"""Route für das Plotten der Graphik moistureD"""
@main_routes.route('/moistureD-plot')
def moistureD_plot():
    # Verbindung zu flask_server db
    conn = mysql.connector.connect(
        host='localhost',
        user='sflask',
        password='12345678',
        database='flask_server'
    )
    cursor = conn.cursor()

    cursor.execute("""
        SELECT payload, timestamp 
        FROM wetness 
        WHERE topic = 'watering/status' 
        ORDER BY id DESC 
        LIMIT 500
    """)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    data = []
    timestamps = []

    for payload, timestamp in reversed(rows):
        try:
            parts = payload.split(',')
            moisture_value = None
            
            # Suche spezifisch nach moistureD
            for p in parts:
                if p.strip().startswith('moistureD:'):
                    moisture_value = int(p.split(':')[1])
                    break
            
            # Nur hinzufügen wenn moistureD gefunden wurde
            if moisture_value is not None:
                data.append(moisture_value)
                timestamps.append(timestamp)
                
        except (ValueError, IndexError) as e:
            print(f"Fehler beim Parsen von moistureD: {payload} - {e}")
            continue

    # Limitiere auf die letzten 300 gültigen Einträge
    if len(data) > 300:
        data = data[-300:]
        timestamps = timestamps[-300:]

    if not data:
        # Erstelle leeren Plot wenn keine Daten vorhanden
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.text(0.5, 0.5, 'Keine moistureD Daten verfügbar', 
                horizontalalignment='center', verticalalignment='center', 
                transform=ax.transAxes, fontsize=14)
        ax.set_title("Digitale Moisture-Werte (moistureD)")
    else:
        df = pd.DataFrame({'timestamp': timestamps, 'moistureD': data})
        
        # Matplotlib-Plot erzeugen
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(df['timestamp'], df['moistureD'], color='green', marker='o', markersize=3, linewidth=1)
        ax.set_title(f"Digitale Moisture-Werte (moistureD) - {len(data)} Datenpunkte")
        ax.set_xlabel("Zeit")
        ax.set_ylabel("Feuchtigkeit D (%)")
        ax.grid(True, alpha=0.3)
        
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Bild im Speicher speichern
    img = io.BytesIO()
    plt.savefig(img, format='png', dpi=100)
    plt.close(fig)
    img.seek(0)

    return send_file(img, mimetype='image/png')

@main_routes.route('/api/trigger', methods=['GET', 'POST'])
def trigger_value():
    if request.method == 'POST':
        data = request.get_json()
        value = data.get('value')
        if value is None:
            return jsonify({'status': 'error', 'message': 'Kein Wert übergeben'}), 400
        try:
            value = int(value)
        except ValueError:
            return jsonify({'status': 'error', 'message': 'Ungültiger Wert'}), 400
        insert_data_trigger(value)
        # Trigger separat publishen!
        publish.single("watering/trigger", str(value), hostname="localhost")
        return jsonify({'status': 'success', 'value': value})
    else:
        # GET: letzten Wert auslesen
        conn = mysql.connector.connect(
            host='localhost',
            user='sflask',
            password='12345678',
            database='flask_server'
        )
        cursor = conn.cursor()
        cursor.execute("SELECT value FROM trigger_values ORDER BY id DESC LIMIT 1")
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        if result:
            return jsonify({'value': result[0]})
        else:
            return jsonify({'value': None})