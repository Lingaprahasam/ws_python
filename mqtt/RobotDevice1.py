from RobotDevices import *
import time


def initDevice():
    device1.connect()


def publishDeviceState():
    device1.publish(topic='sensor1', msg='sensor1Value')


def on_message(client, userdata, message):
    print("device1 received message =", str(message.payload.decode("utf-8")))
    publishDeviceState()


def main():
    initDevice()
    publishDeviceState()
    device1.subscribe('sensor2', 1)

    try:
        while True:
            device1.on_message = on_message
    except:
        device1.disconnect()


if __name__ == "__main__":
    main()
