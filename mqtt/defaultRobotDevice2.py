from myRobotObj import RobotComponent
import time


def main():
    sensor2 = RobotComponent('2')
    sensor2.connect()
    sensor2.publish(topic='sensor2', msg='sensor2Value')
    time.sleep(4)
    sensor2.disconnect()


if __name__ == "__main__":
    main()
