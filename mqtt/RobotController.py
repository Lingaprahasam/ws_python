from RobotDevices import *
import time


def initController():
    controller.connect()


def on_message(client, userdata, message):
    print("controller received message =", str(message.payload.decode("utf-8")))


def main():
    initController()
    controller.subscribe([('sensor1', 1), ('sensor2', 1)])

    try:
        while True:
            controller.on_message = on_message
    except:
        controller.disconnect()


if __name__ == "__main__":
    main()
