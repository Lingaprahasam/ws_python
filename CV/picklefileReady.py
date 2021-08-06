import os
import sys
import pickle
import numpy as np

circlePos=np.float32([(10,10),(10,500),(500,500),(500,10)])
red_max = np.array([255,255,255])
red_min = np.array([0,0,0])
green_max = np.array([255,255,255])
green_min=np.array([0,0,0])
black_max = np.array([255,255,255])
black_min = np.array([0,0,0])
teal_max = np.array([255,255,255])
teal_min = np.array([0,0,0])


print(os.path.isfile(os.path.join(sys.path[0], "data.txt")))

with open(os.path.join(sys.path[0], "data.txt"),"rb") as file:
    try:
        (circlePos,red_max,red_min,green_max,green_min,black_max,black_min,teal_max,teal_min)=pickle.load(file)
        # print((circlePos,red_max,red_min,green_max,green_min,black_max,black_min,teal_max,teal_min))
        print("======================")
        print(circlePos)
        print("======================")
        print(red_min)
        print("======================")
        print(red_max)
        print("======================")
        print(green_min)
        print("======================")
        print(green_max)
        print("======================")
        print(teal_min)
        print("======================")
        print(teal_max)
        print("======================")

    except Exception as e:
        print(str(e))