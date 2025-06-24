from machine import Pin, ADC #typing: ignore
from umqtt.simple import MQTTClient #typing: ignore
import time

"""Initialisierung der Pins und Sensoren"""
led_green = Pin(12, Pin.OUT)
led_green.off()

check_led = Pin(2, Pin.OUT)
check_led.off()  # AN (LOW = AN beim ESP8266)

sensor_analog = ADC(0)
sensor_digital = Pin(4, Pin.IN)

pump = Pin(5, Pin.OUT) 

"""Globale Variablen"""
#data_analog = sensor_analog.read()
#data_digital = sensor_digital.value()
status_pump = None
trigger = 800
pump_time = 10  # Zeit in Sekunden, die die Pumpe laufen soll
pump_time_stop = 3

client = None

"""Konfiguration des MQTT-Brokers und der Topics"""
MQTT_BROKER = "lbraun.nl"
MQTT_PORT = 1883
MQTT_TOPIC_PUB_MOISTURE = b'watering/status'
MQTT_TOPIC_PUB_PUMP = b'watering/pump'
MQTT_TOPIC_SUB_PUMP = b'watering/control'
MQTT_TOPIC_SUB_TRIGGER = b'watering/trigger'

"""Herstellen der MQTT-Verbindung und subscriben des Topics"""
def connect_mqtt():
    global client
    try:
        client = MQTTClient("ESP8266", MQTT_BROKER, port=MQTT_PORT)
        client.set_callback(empfangen)
        client.connect()
        client.subscribe(MQTT_TOPIC_SUB_PUMP)
        client.subscribe(MQTT_TOPIC_SUB_TRIGGER)
        print("MQTT verbunden")
        return client
    except Exception as e:
        print(f"MQTT-Verbindung fehlgeschlagen: {e}")
        return None

"""Funktion zum Senden von Nachrichten über MQTT"""
def senden(topic, data, typ):
    global client

    if client:
        print("^^^^^^^^^^^^^^^^^^^^^^^^")
        status = f"{typ}:{data}"
        print(status)
        status_msg = str(status).encode()
        try:
            client.publish(topic, status_msg)
            print(f"Nachricht gesendet: {status_msg}")
        except Exception as e:
            print(f"Fehler beim Senden der Nachricht: {e}")

"""Funktion zum Empfangen von Nachrichten über MQTT"""
def empfangen(topic, msg):
    global status_pump, trigger
    topic = topic.decode()
    message = msg.decode()
    print("++++++++++++++++++++++++++++++++")
    print(f"Nachricht empfangen: Topic: {topic}, Nachricht: {message}")
    if topic == "watering/control":
        if message == "on":
            status_pump = True
            print("Pumpe eingeschaltet")
        elif message == "off":
            status_pump = False
            print("Pumpe ausgeschaltet")
    elif topic == "watering/trigger":
        try:
            trigger = int(message)
            print(f"Neuer Trigger-Wert empfangen: {trigger}")
        except ValueError:
            print("Ungültiger Trigger-Wert empfangen")


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
        print("-----------------------------")
        print("Triggerwert:", trigger)
        try:
            if client:
                client.check_msg()
            else:
                client = connect_mqtt()
            analog_trocken = auswertung_analog(trigger)
            print("STATUS PUMP (((((((())))))))",status_pump)
            if status_pump == True or analog_trocken:
                senden(MQTT_TOPIC_PUB_MOISTURE, sensor_digital.value(), "moistureD")
                time.sleep(1)
                senden(MQTT_TOPIC_PUB_MOISTURE, sensor_analog.read(), "moistureA")
                led_green.on()
                pump.value(1)
                time.sleep(pump_time)
                pump.value(0)
            else:
                senden(MQTT_TOPIC_PUB_MOISTURE, sensor_digital.value(), "moistureD")
                time.sleep(1)
                senden(MQTT_TOPIC_PUB_MOISTURE, sensor_analog.read(), "moistureA")
                led_green.off()
            # Pumpenstatus separat senden
            senden(MQTT_TOPIC_PUB_PUMP, status_pump, "pump")
            time.sleep(pump_time_stop)
        except Exception as e:
            print('Fehler in Hauptschleife:', e)
            time.sleep(5)
            client = None
client = connect_mqtt()
run_watering()