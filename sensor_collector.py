import grovepi
# from grove_rgb_lcd import *
import urllib, httplib
import time

##This should be there now
# Connect the DHt sensor to port 7
dht_sensor_port = 7

# Connect to PIR sensor, port 8
pir_sensor = 8
grovepi.pinMode(pir_sensor, "INPUT")

while True:
    try:
        #Get the temperature and Humidity from the DHT sensor
        [ temp, hum ] = grovepi.dht(dht_sensor_port, 1)
        print "temp =", temp, "C\thumadity =", hum,"%"
        #get movement
        move = grovepi.digitalRead(pir_sensor)
        print "movement=", move
        params = urllib.urlencode({'t': temp, 'h': hum, 'm': move,  'token':'YD4U41EMAHIGRLPE'})
        headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
        conn = httplib.HTTPConnection("192.168.1.145:3000")
        try:
            conn.request('POST', '/sensor/collect', params, headers)
            # response = conn.getresponse()
            # print response.status
            # data = response.read()
            conn.close()
            time.sleep(16)
        except Exception as e:
            print "Error: ", e

    except (IOError,TypeError) as e:
        print "Error", e
