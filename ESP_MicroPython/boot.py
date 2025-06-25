import machine # type: ignore
import time
import network # type: ignore
import socket

# Interne LED initialisieren (GPIO2, LOW = AN)
check_led = machine.Pin(2, machine.Pin.OUT)

# LED blinken lassen während des Verbindens
for _ in range(10):
    check_led.off()
    time.sleep(0.2)
    check_led.on()
    time.sleep(0.2)

"""Wlan aktivieren"""
wlan = network.WLAN(network.STA_IF)
wlan.active(True)


print("Verbinde mit WLAN...")
ssid = "Wlan2"
password = "1234wlan5678"

"""Wlan verbinden"""
wlan.connect(ssid, password)

"""versucht x mal zu verbinden"""
max_wait = 100
while max_wait > 0:
    if wlan.isconnected():
        break
    max_wait -= 1
    print("Verbindungsversuch...")
    print("Status:", wlan.status())
    time.sleep(1)


if wlan.isconnected():
    print("Verbunden! IP-Adresse:", wlan.ifconfig()[0])
else:
    print("Verbindung fehlgeschlagen!")
    print("Status:", wlan.status())

    #- 0 – No connection (WLAN interface is idle).
    #- 1 – Connecting to a network.
    #- 2 – Connection failed.
    #- 3 – Connected successfully.
    #- 4 – Connection lost.
    #- 5 – Wrong password.
    #- 6 – No AP found (SSID not available).
    #- 7 – Connection timeout.
