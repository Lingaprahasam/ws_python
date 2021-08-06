from re import search
import pyvda
import pygetwindow as gw
import win32gui
import cv2
import pyautogui
import numpy as np
import time


# get application title
def getAppTitle(appName):
    # get all running application titles
    allTitles = gw.getAllTitles()
    # print(allTitles)

    # get app title
    for title in allTitles:
        if search("^.*"+appName+"$", str(title)):
            appTitle = str(title)
            break

    return appTitle

# Stream application gui interface
def streamAppGUI(appName):
    appTitle = getAppTitle(appName)
    appWindow = gw.getWindowsWithTitle(appTitle)[0]
        
    image = pyautogui.screenshot(region=(appWindow.topleft.x,appWindow.topleft.y, appWindow.size.width, appWindow.size.height))
    image.save(r"C:\Users\selis\Documents\screenshot.png")
    imgCV = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    
    # display an image
    cv2.imshow("test image", imgCV)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def MoveAppToDesktop(appName):
    # number_of_active_desktops = pyvda.GetDesktopCount()
    current_desktop = pyvda.GetCurrentDesktopNumber()

    # get appTitle
    appTitle = getAppTitle(appName)

    # pygetwindow instance
    appWindow = gw.getWindowsWithTitle(appTitle)[0]

    #win32gui instance
    current_window_handle = win32gui.FindWindow(None, appTitle)
    
    # Maximize if it is minimized
    # win32gui.ShowWindow(current_window_handle,5)
    # win32gui.SetForegroundWindow(current_window_handle)
    if (appWindow.isMaximized == False):
        appWindow.maximize()
    
    # Move to next desktop
    pyvda.MoveWindowToDesktopNumber(current_window_handle, current_desktop+1)
    
    # Move to desktop 2
    pyvda.GoToDesktopNumber(current_desktop+1)
    time.sleep(0.1)
    # record video
    streamAppGUI(appTitle)
    time.sleep(0.1)
    # Move back to original desktop
    pyvda.GoToDesktopNumber(current_desktop)


if __name__ == '__main__':
    vogtAppName = "Notepad"
    MoveAppToDesktop(vogtAppName)