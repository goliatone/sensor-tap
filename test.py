import time
from sensor.mqtt_publisher import MqttClient

id = 'adfjadfajd;fajdf'
topic = 'location/HQ/device/RPI/id/4/sensor/TMP'

client = MqttClient(id=id, topic=topic)


count = 0

while True:
    time.sleep(count)
    client.notify({"ID":1, "count": count})
    count+=1
