from mqttClientClass import MQTTClientObj


class RobotComponent(MQTTClientObj):
    def __init__(self, id, topicId='defaultRobot'):
        super(RobotComponent, self).__init__(id)
        self.topicHeader = 'robots'
        self.topicSubHeader = topicId
        super(RobotComponent, self).setTopicHeader(self.topicHeader)
        super(RobotComponent, self).setTopicSubHeader(topicId)

    def connect(self, host='127.0.0.1', port=1883):
        super(RobotComponent, self).connect(host=host, port=port)

    def disconnect(self):
        super(RobotComponent, self).disconnect()

    def publish(self, topic='defaultTopic', msg='defaultMsg'):
        super(RobotComponent, self).publish(topic, msg)

    def subscribe(self, *args):
        try:
            if len(args) == 2:
                (topicItem, qosItem) = args
                super(
                    RobotComponent, self).subscribe(
                    self.topicHeader + '/' + self.topicSubHeader + '/' + topicItem, qosItem)
            else:
                for tuple1 in args:
                    for item in tuple1:
                        (topicItem, qosItem) = item
                        super(
                            RobotComponent, self).subscribe(
                            self.topicHeader + '/' + self.topicSubHeader + '/' + topicItem, qosItem)
        except:
            print('Error Occured: subscribe')

    def on_message(client, userdata, message):
        return super().on_message(userdata, message)
