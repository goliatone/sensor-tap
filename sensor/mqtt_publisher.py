import paho.mqtt.client as mqtt
import json

class MqttClient():

    def __init__(self,id=None, topic='root', url = "localhost", port = 1883, keepalive = 60):
        self.url = url
        self.port = port
        self.keepalive = keepalive
        self.id = id
        self.topic = topic

        client = mqtt.Client()
        client.on_connect = self.on_connect
        client.on_message = self.on_message
        client.on_disconnect = self.on_disconnect

        payload = '{"uuid":"%s", "status":"disconnected"}' %(self.id)
        client.will_set('devices/disconnected', payload=payload, qos=0, retain=False)

        try:
            client.connect(url, port, keepalive)
            client.loop_start()
        except Exception, e:
            print e

        self.client = client


    def on_connect(self, client, userdata, flags, rc):
        print "Connected with result code " + str(rc)


    def on_message(self, client, userdata, msg):
        print "Message: " + msg + userdata


    def on_disconnect(self, client, userdata, rc):
        print "ON disconnect"


    def notify(self, payload=None, topic=None):
        if not payload: return []
        if not self.url: raise Exception('Invalid URL option')
        topic = self.topic if not topic else topic
        try:
            data=json.dumps(payload)
            print "NOTIFY:\n%s\n%s" %(topic, data)
            self.client.publish(topic, data)
        except Exception as e:
            print 'Error: ', e

        return []
