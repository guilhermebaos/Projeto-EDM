from wifidata import ssid, password
import time
import network

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
