# import xml.etree.ElementTree as ET
from ws4py.client.threadedclient import WebSocketClient
import requests
from requests.auth import HTTPDigestAuth
from threading import Thread,Timer
import time
from pythonping import ping

class RobWebSocketClient(WebSocketClient):
    def opened(self):
        print ("Web Sockect connection established")

    def closed(self, code, reason=None):
        print ("Closed down", code, reason)

    def set_callback(self,callback,connection):
        self.callback = callback
        self.conn = connection
        
        
        
    def getVal(self, resp):
        root = ET.fromstring(resp)
        #return int(root[1][0][2][0][4].text)
        return int(root[1][0][1][0][1].text)

    def received_message(self, event_xml):     
        if event_xml.is_text:   
            val = int(self.getVal(event_xml.data.decode("utf-8")))
            self.callback(val,self.conn)
            

        else:
            print ("Received Illegal Event " + str(event_xml))


class Connection:
    def __init__(self, host,callback):
        self.host = host
        # self.log = logger
        self.call=callback
        self.username = "Default User"
        self.password = "robotics"
        self.digest_auth = HTTPDigestAuth(self.username,self.password)

    def subscribe(self, signalName, forever=True, device="Local"):  
        self.signalName = signalName
        self.session = requests.Session()
        payload = {'resources':'1',
                   '1':'/rw/iosystem/signals/{1}/{0};state'.format(signalName,device),
                   '1-p':'2'}

        print("Posting...")
        resp=self.session.post('http://{0}/subscription'.format(self.host), auth=self.digest_auth, data=payload)
       # resp = requests.post('http://{0}/subscription'.format(self.host), auth=self.digest_auth, data=payload, headers = {"connection":"keep-alive"})
        print(str(resp.status_code))


        if resp.status_code == 201:
            self.location = resp.headers['Location']
            self.cookie = 'ABBCX={0}'.format(resp.cookies['ABBCX'])
           # self.cookie = resp.cookies
            d=self.digest_auth.build_digest_header("GET",'http://localhost/subscription')
            header = [('Cookie',self.cookie),
                    ('Authorization',d)
                    ]                

            self.ws = RobWebSocketClient(self.location, 
                                         protocols=['robapi2_subscription'], 
                                         headers=header)
            self.ws.set_callback(self.callback,self)
            self.ws.connect()
            if forever:
                self.ws.run_forever()
            else:
                t = Thread(target = self.threadSub)
                t.start()
            return True
        else:
           print ('Error subscribing ' + str(resp.status_code))
           return False


    def threadSub(self):
        self.ws.run_forever()


    def callback(self,val,connection):
        # self.log.log_info({"IO":True,"setting":False,"name":self.signalName,"value":val,"subscribed":True})
        self.call(val,connection)

    def close(self):
        #self.stop_sub()
        self.ws.close()


class RobotHandler():
    def __init__(self, host):
        self.motor_on = False


    def on_motors_signal(self,val,connection):
        # self.mqttRobot.updateState("motorOn",{"isOn":val==1})
        self.motor_on=val
        # self.updateInitState()  


def main():
    robIp = "192.168.1.127"
    pingRes = ""
    while True:
        print("Ping Started...")

        pingResp = ping(robIp, verbose=True)

        for resp in pingResp:
            # print("PingResponseList: " + str(resp))
            pingRes = str(resp)


        if "Reply from" not in pingRes:
            continue
        else:
            print("Ping to " + str(robIp) + " is successful" )
            break



    print("Test Started....")
    robotHandler = RobotHandler(robIp)
    rwsConnMotors = Connection(robIp,robotHandler.on_motors_signal)

    try:     
        res=rwsConnMotors.subscribe("I_motor_on",False,"SIM_BOARD")
    except KeyboardInterrupt:
        rwsConn.close()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        with open("ErrorReportRobotControl.txt","w") as f:
            print(str(e))
            f.write(str(e)+'\n')