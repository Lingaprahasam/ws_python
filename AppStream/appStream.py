from re import search
import pygetwindow as gw
import pyautogui
import cv2
import numpy as np


# get application title
def getAppTitle(appName):
    # get all running application titles
    allTitles = gw.getAllTitles()
    # print(allTitles)

    # get browser app title
    for title in allTitles:
        if search("^.*"+appName+"$", str(title)):
            appTitle = str(title)
            break

    return appTitle

# set vogt app and browser in right position
def setAppsInPos(app1Name="Edge", app2Name="Notepad", app1WidthPercent=60, app2WidthPercent=40):
    # default invisible window border
    windowBorder = 8
    scrWidth, ScrHeight = pyautogui.size()
    
    try:
        # get app1Title
        app1Title = getAppTitle(app1Name)

        # get app2title
        app2Title = getAppTitle(app2Name)
        
        app1Window = gw.getWindowsWithTitle(app1Title)[0]
        app2Window = gw.getWindowsWithTitle(app2Title)[0]
        
        app1WindowWidth = int((scrWidth*app1WidthPercent)/100)
        app2WindowWidth = int((scrWidth*app2WidthPercent)/100)
        
        app1Window.restore()
        app2Window.restore()
        app1Window.resizeTo(app1WindowWidth+(2*windowBorder), ScrHeight)
        app2Window.resizeTo(app2WindowWidth+(2*windowBorder), ScrHeight)        

        if (app1Window.topleft.x != -1*windowBorder):
            app1Window.moveTo(0-windowBorder,0)

        if (app2Window.topright.x != scrWidth):
            app2Window.moveTo(scrWidth-app2Window.size.width+windowBorder,0)
    except:
        print("Error setting app into position")

# Stream application gui interface
def streamAppGUI(appName):
    appTitle = getAppTitle(appName)
    appWindow = gw.getWindowsWithTitle(appTitle)[0]
        
    image = pyautogui.screenshot(region=(appWindow.topleft.x,appWindow.topleft.y, appWindow.size.width, appWindow.size.height))
    # image.save(r"C:\Users\selis\Documents\screenshot.png")
    imgCV = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    
    # display an image
    cv2.imshow("test image", imgCV)
    # cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == '__main__':
    vogtAppName = "PHAsis"
    browserName = "Edge"
    vogtAppWidthPerc = 40
    browserAppWidthPerc = 60
    
    setAppsInPos(browserName, vogtAppName, browserAppWidthPerc, vogtAppWidthPerc)
    streamAppGUI(vogtAppName)

    # while(True):
    #     streamAppGUI(vogtAppName)
