import os
from HelperFunctions import *

# Helper functions
helper = Helper()

# root topic
topic_root = 'robots'
topic_prefix = "defaultRobot"

# Devices
controller = 'controller'
device1 = 'device1'
device2 = 'device2'

# Topic Domains
state = 'state'
cmd = 'command'
req = 'request'
state_stopped = 'stopped'

# Subscribe to all device topics
device1AllTopics = os.path.join(device1, '#').replace("\\", "/")  # device1+'/#'
device2AllTopics = device2+'/#'

# Subscribe to all device state
device1State = device1+'/'+state
device2State = device2+'/'+state

# Subscribe to all device commands
device1Command = device1+'/'+cmd
device2Command = device2+'/'+cmd

# Subscribe to all device requests
device1Command = device1+'/'+req
device2Command = device2+'/'+req
