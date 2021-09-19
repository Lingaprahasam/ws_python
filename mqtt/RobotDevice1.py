from RobotFramework import *
from RobotDeviceObj import *


def initDevice():
    device1Obj.connect()


def on_message(client, userdata, message):
    topicArr = helper.parseTopic(message.topic)
    print(("Received a message from {0} =").format(
        topicArr[2]), str(message.payload.decode("utf-8")))
    helper.publish(device1Obj, device1, state, qos=0, payload='ON')


def main():
    try:
        initDevice()
        helper.publish(device1Obj, device1, state, qos=0, payload='ON')
        device1Obj.subscribe(device2AllTopics, 1)

        while True:
            device1Obj.on_message = on_message
    except:
        helper.publish(device1Obj, device1, state, qos=0, payload=state_stopped)
        print('Device1 is stopped')
    finally:
        device1Obj.disconnect()


if __name__ == "__main__":
    main()
