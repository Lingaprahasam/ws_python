import os


class Helper():
    def __init__(self) -> None:
        pass

    def parseTopic(self, topic):
        '''
        parse the topic in to its components
        returns topic component list
        '''
        normTopic = os.path.normpath(topic)
        return normTopic.split(os.sep)

    def publish(
            self, clientObj, clientName, topicDomain='defaultDomain', payload=None, qos=0, retain=False,
            properties=None):
        '''
        publish using the client object
        makes use of the client name and its domain

        domain
            - status
            - command

        default domain is 'defaultDomain'
        '''
        topic = clientName + '/' + topicDomain
        clientObj.publish(topic, payload=payload, qos=qos, retain=retain, properties=properties)
