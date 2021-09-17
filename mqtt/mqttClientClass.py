import paho.mqtt.client as mqtt
import time


class MQTTClientObj(mqtt.Client):
    def __init__(self, cname, **kwargs):
        super(MQTTClientObj, self).__init__(cname, **kwargs)
        self.last_pub_time = time.time()
        self.topic_ack = []
        self.run_flag = False
        self.subscribe_flag = False
        self.bad_connection_flag = False
        self.connected_flag = False
        self.disconnect_flag = False
        self.disconnect_time = 0.0
        self.devices = []

    def connect(self, host, port):
        try:
            self.on_connect
            super(MQTTClientObj, self).connect(host, port)
            super(MQTTClientObj, self).loop_start()

            while self.connected_flag == False:
                print('Connecting to the broker...')
                time.sleep(.01)

            print('Connected!')
        except Exception:
            super(MQTTClientObj, self).loop_stop()
            print('Error connecting to broker')
            print('Please check the broker address and port')
            raise

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            self.connected_flag = True
            pass
        else:
            print("Bad connection Returned code=", rc)

    def disconnect(self):
        self.on_disconnect
        super(MQTTClientObj, self).disconnect()

    def on_disconnect(self, client, userdata, rc=0):
        self.disconnect_flag = True
        client.loop_stop()

    def publish(self, topic, payload=None, qos=0, retain=False, properties=None):
        self.on_publish
        super(MQTTClientObj, self).publish(topic, payload=payload, qos=qos, retain=retain, properties=properties)

    def on_publish(self, client, userdata, result):
        pass

    def subscribe(self, topic, qos):
        self.on_subscribe
        super(MQTTClientObj, self).subscribe(topic, qos)

    def on_subscribe(self, client, userdata, mid, granted_qos):
        pass
