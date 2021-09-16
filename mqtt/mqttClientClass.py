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
        self.topicHeader = ''
        self.topicSubHeader = ''

    def setTopicHeader(self, topicHeader='DefaultHeader'):
        self.topicHeader = topicHeader

    def setTopicSubHeader(self, topicSubHeader='DefaultSubHeader'):
        self.topicSubHeader = topicSubHeader

    def connect(self, host, port):
        try:
            self.on_connect
            super(MQTTClientObj, self).connect(host, port)
            super(MQTTClientObj, self).loop_start()

            while self.connected_flag == False:
                time.sleep(.01)
        except:
            super(MQTTClientObj, self).loop_stop()
            print('Error connecting to broker')
            print('Please check the broker address and port')

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            self.connected_flag = True
            # print("connected OK Returned code=", rc)
            pass
        else:
            print("Bad connection Returned code=", rc)

    def disconnect(self):
        self.on_disconnect
        super(MQTTClientObj, self).disconnect()

    def on_disconnect(self, client, userdata, rc=0):
        self.disconnect_flag = True
        client.loop_stop()

    def publish(self, topic, msg):
        self.on_publish
        super(MQTTClientObj, self).publish(self.topicHeader+'/'+self.topicSubHeader+'/'+topic, msg)

    def on_publish(self, client, userdata, result):
        pass

    def subscribe(self, topic, qos):
        self.on_subscribe
        super(MQTTClientObj, self).subscribe(topic, qos)

    def on_subscribe(self, client, userdata, mid, granted_qos):
        print('Subscription successful')
        pass

    def on_message(client, userdata, message):
        print("received message =", str(message.payload.decode("utf-8")))
