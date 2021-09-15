from myRobotObj import RobotComponent
import time


def main():
    sensor1 = RobotComponent('1')
    sensor1.connect()
    sensor1.publish(topic='sensor1', msg='sensor1Value')
    time.sleep(4)
    sensor1.disconnect()


if __name__ == "__main__":
    main()
