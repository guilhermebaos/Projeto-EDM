from wifidata import ssid, password
from machine import Pin
import time
import network


red = Pin(25, Pin.OUT)
red.value(0)

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
if not wlan.isconnected():
    print('Connecting to network...')
    wlan.connect(ssid, password)
    while not wlan.isconnected():
        print('.', end='')
        time.sleep(0.1)
    print(' Connected!')
print('network config:', wlan.ifconfig())
red.value(1)
