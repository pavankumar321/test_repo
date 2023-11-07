import network
import time

#def connectWiFi(ssid,password):
def connectWiFi(ssid,password,country):
   #rp2.country(country)
   wlan = network.WLAN(network.STA_IF)
   wlan.active(True)
   if wlan.isconnected():
       return 1,wlan.isconnected()
   wlan.connect(ssid, password)
   # Wait for connect or fail
   max_wait = 10
   while max_wait > 0:
      if wlan.status() < 0 or wlan.status() >= 3:
        break
    
      max_wait -= 1
      print('waiting for connection...')
      time.sleep(1)

   # Handle connection error
   if wlan.status() != 3:
      raise RuntimeError('network connection failed')
   else:
      print('connected')
      status = wlan.ifconfig()
      print( 'ip = ' + status[0] )
   return status,wlan.isconnected()