from grovepi import *
from grove_rgb_lcd import *
import urllib, httplib

##This should be there now
# Connect the DHt sensor to port 7
dht_sensor_port = 7

while True:
    try:
        #Get the temperature and Humidity from the DHT sensor
        [ temp, hum ] = dht(dht_sensor_port, 1)
        print "temp =", temp, "C\thumadity =", hum,"%"

        params = urllib.urlencode({'t': temp, 'h': hum, 'token':'YD4U41EMAHIGRLPE'})
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
