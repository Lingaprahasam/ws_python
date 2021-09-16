from RobotDevices import *
import time


def initDevice():
    device2.connect()


def publishDeviceState():
    device2.publish(topic='sensor2', msg='sensor2Value')


def on_message(client, userdata, message):
    print("device2 received message =", str(message.payload.decode("utf-8")))
    publishDeviceState()


def main():
    initDevice()
    publishDeviceState()
    device2.subscribe('sensor1', 1)

    try:
        while True:
            device2.on_message = on_message
    except:
        device2.disconnect()


if __name__ == "__main__":
    main()
