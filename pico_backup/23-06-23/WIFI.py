import network, rp2, time

# set your WiFi Country
#rp2.country('IT')

wlan = network.WLAN(network.STA_IF)
wlan.active(True)

# set power mode to get WiFi power-saving off (if needed)
wlan.config(pm = 0xa11140)

wlan.connect('vistan_skivvy', 'skivvy234')

while not wlan.isconnected() and wlan.status() >= 0:
 print("Waiting to connect:")
 time.sleep(1)

print(wlan.ifconfig())