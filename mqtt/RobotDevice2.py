from RobotFramework import *


def initDevice():
    device2Obj.connect()


def on_message(client, userdata, message):
    topicArr = helper.parseTopic(message.topic)
    print(("Received a message from {0} =").format(
        topicArr[2]), str(message.payload.decode("utf-8")))
    helper.publish(device2Obj, device2, state, qos=0, payload='ON')


def main():
    try:
        initDevice()
        helper.publish(device2Obj, device2, state, qos=0, payload='ON')
        device2Obj.subscribe(device1AllTopics, 1)

        while True:
            device2Obj.on_message = on_message
    except:
        helper.publish(device2Obj, device2, state, qos=0, payload=state_stopped)
        print('Device2 is stopped')
    finally:
        device2Obj.disconnect()


if __name__ == "__main__":
    main()
