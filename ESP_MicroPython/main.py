from machine import Pin, ADC #typing: ignore
from umqtt.simple import MQTTClient #typing: ignore
import time

"""Initialisierung der Pins und Sensoren"""
led_green = Pin(12, Pin.OUT)
led_green.off()

sensor_analog = ADC(0)
sensor_digital = Pin(4, Pin.IN)

pump = Pin(5, Pin.OUT) 

"""Globale Variablen"""
#data_analog = sensor_analog.read()
#data_digital = sensor_digital.value()
status_pump = 0
trigger = 800
pump_time = 3
pump_time_stop = 3

client = None

"""Konfiguration des MQTT-Brokers und der Topics"""
MQTT_BROKER = "192.168.178.21"
MQTT_PORT = 1883
MQTT_TOPIC_PUB = b'watering/status'
MQTT_TOPIC_PUB2 = b'watering/pump'
MQTT_TOPIC_SUB = b'watering/control'

"""Funktion zum Senden von Nachrichten über MQTT"""
def senden(zu_verwendende_topic, data, topic):
    global client
    
    if client:
        status = f"{topic}:{data}"
        print(status)
        status_msg = str(status).encode()
        print(status_msg)
        
        try:
            client.publish(zu_verwendende_topic, status_msg)
            print(f"Nachricht gesendet: {status_msg}")
        except Exception as e:
            print(f"Fehler beim Senden der Nachricht: {e}")

"""Funktion zum Empfangen von Nachrichten über MQTT"""
def empfangen(topic, msg):
    global status_pump
    
    print(f"Nachricht empfangen:")
    topic = topic.decode()
    print(f"Topic: {topic}")
    message = msg.decode()
    print(f"Nachricht: {message}")
    
    if message == "on":
        status_pump = 1
        #led_green.on()
        print("Pumpe eingeschaltet")
    elif message == "off":
        status_pump = 0
        #led_green.off()
        print("Pumpe ausgeschaltet")

"""Herstellen der MQTT-Verbindung und subscriben des Topics"""
def connect_mqtt():
    try:
        client = MQTTClient("ESP8266", MQTT_BROKER, port=MQTT_PORT)
        client.set_callback (empfangen)
        client.connect()
        client.subscribe(MQTT_TOPIC_SUB)
        print("MQTT verbunden")
        return client
    except Exception as e:
        print(f"MQTT-Verbindung fehlgeschlagen: {e}")
        return None

"""Abgleichen des analogen Sensors mit dem Triggerwert und Ausgabe eines Bools"""
def auswertung_analog(trigger):
    # umso größer der Wert ist, desto trockener ist die Erde
    # lampe an feucht genug
    if sensor_analog.read() > trigger:
        return True
    else:
        return False

"""Hauptfunktion zum Betrieb der automatischen Bewässerung"""
def run_watering():
    global client, status_pump
    
    while True:
        try:
            # MQTT-Verbindung prüfen/wiederherstellen
            if client:
                client.check_msg()
            else:
                client = connect_mqtt()
                
            # Sensordaten lesen
            analog_trocken = auswertung_analog(trigger)
            
            # Pumpenlogik: Pumpe AN wenn manuell aktiviert ODER Boden trocken
            if status_pump == 1 or analog_trocken:
                print("--------------")
                print("Pumpe wird aktiviert")
                senden(MQTT_TOPIC_PUB, sensor_digital.value(), "moistureD")
                time.sleep(1)
                senden(MQTT_TOPIC_PUB, sensor_analog.read(), "moistureA")
                print(f"Sensor analog: {sensor_analog.read()}")
                print(f"Sensor digital: {sensor_digital.value()}")
                
                led_green.on()
                pump.on()
                time.sleep(pump_time)
                pump.off()  # Pumpe nach pump_time ausschalten
                print(f"Pumpe lief für {pump_time} Sekunden")
                print("--------------")
                
            else:
                print("--------------")
                print("Pumpe bleibt aus - Boden feucht genug")
                senden(MQTT_TOPIC_PUB, sensor_digital.value(), "moistureD")
                time.sleep(1)
                senden(MQTT_TOPIC_PUB, sensor_analog.read(), "moistureA")
                led_green.off()
                print("--------------")
            
            # Pumpenstatus senden
            senden(MQTT_TOPIC_PUB2, status_pump, "pump")
            
            # Warten zwischen den Zyklen
            time.sleep(pump_time_stop)
            
        except Exception as e:
            print('Fehler in Hauptschleife:', e)
            time.sleep(5)
            client = None


"""Ausführen der Funktionen"""
client = connect_mqtt()
run_watering()