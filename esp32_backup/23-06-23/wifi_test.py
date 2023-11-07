import network
import time

# set your WiFi Country
#rp2.country('IT')

wlan = network.WLAN(network.STA_IF)
wlan.active(True)

print(wlan.isconnected())