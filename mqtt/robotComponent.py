from mqttClientClass import MQTTClientObj


class RobotComponent(MQTTClientObj):
    def __init__(self, id, topicId='defaultRobot'):
        super(RobotComponent, self).__init__(id)
        super(RobotComponent, self).setTopicHeader('robots')
        super(RobotComponent, self).setTopicSubHeader(topicId)

    def connect(self, host='127.0.0.1', port=1883):
        super(RobotComponent, self).connect(host=host, port=port)

    def disconnect(self):
        super(RobotComponent, self).disconnect()

    def publish(self, topic='defaultTopic', msg='None'):
        super(RobotComponent, self).publish(topic, msg)
