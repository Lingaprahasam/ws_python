from RobotFramework import *
from RobotDeviceObj import *


def initController():
    controllerObj.connect()


def on_message(client, userdata, message):
    try:
        topicArr = helper.parseTopic(message.topic)

        if(topicArr[2] == device1):
            print(("Received a message from {0} =").format(
                topicArr[2]), str(message.payload.decode("utf-8")))
        elif(topicArr[2] == device2):
            print(("Received a message from {0} =").format(
                topicArr[2]), str(message.payload.decode("utf-8")))

        if(str(message.payload.decode("utf-8")) == state_stopped):
            print(("{0} has {1}.").format(topicArr[2], state_stopped))
    except:
        print('Error: controller message callback')


def main():
    try:
        initController()
        controllerObj.subscribe('device1/#', 0)
        controllerObj.subscribe('device2/#', 0)

        while True:
            controllerObj.on_message = on_message
    except:
        print('controller is stopped')
    finally:
        controllerObj.disconnect()


if __name__ == "__main__":
    main()
