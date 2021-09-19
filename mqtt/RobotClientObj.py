from mqttClientClass import MQTTClientObj
from RobotFramework import *


class RobotClientObj(MQTTClientObj):
    def __init__(self, id, topic_root=topic_root, topic_prefix=topic_prefix):
        super(RobotClientObj, self).__init__(id)
        self.topic_prefix = topic_prefix
        self.topic_root = topic_root

    def connect(self, host='127.0.0.1', port=1883):
        super(RobotClientObj, self).connect(host=host, port=port)

    def disconnect(self):
        super(RobotClientObj, self).disconnect()

    def publish(self, topic, payload=None, qos=0, retain=False, properties=None):
        super(RobotClientObj, self).publish(self.topic_root + '/' + self.topic_prefix + '/' + topic,
                                            payload=payload, qos=qos, retain=retain, properties=properties)

    def subscribe(self, *args):
        try:
            if len(args) == 2:
                (topicItem, qosItem) = args

                super(
                    RobotClientObj, self).subscribe(
                    topic=self.topic_root + '/' + self.topic_prefix + '/' + topicItem, qos=qosItem)
            elif len(args) == 1:
                for tuple1 in args:
                    for item in tuple1:
                        (topicItem, qosItem) = item
                        super(
                            RobotClientObj, self).subscribe(
                            topic=self.topic_root + '/' + self.topic_prefix + '/' + topicItem, qos=qosItem)
        except:
            print('Error Occured: subscribe')
            raise
