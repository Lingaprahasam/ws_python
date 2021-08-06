from re import search
import pyvda
import pygetwindow as gw
import win32gui
import cv2
import pyautogui
import numpy as np
import time

class AppGUIRecorder():
    def __init__(self, appName):
        self.appName = appName

    def getAppTitle(self, appName):
        """
            returns first application title matches the appName
        """
        # get all running application titles
        allTitles = gw.getAllTitles()
        # print(allTitles)

        # get app title
        for title in allTitles:
            if search("^.*"+appName.upper()+"$", str(title).upper()):
                appTitle = str(title)
                break

        return appTitle


    def streamAppGUI(self, appName):
        """ 
            Stream application gui interface
        """

        appTitle = self.getAppTitle(appName)
        appWindow = gw.getWindowsWithTitle(appTitle)[0]

        image = pyautogui.screenshot(region=(appWindow.topleft.x,appWindow.topleft.y, appWindow.size.width, appWindow.size.height))
        image.save(r"C:\Users\selis\Documents\screenshot.png")
        imgCV = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

        # display an image
        cv2.imshow("test image", imgCV)
        # cv2.waitKey(0)
        cv2.destroyAllWindows()


    def HandleAppOnDesktop(self, appName):
        """ 
            Moves/Keeps the app on a virtual desktop
                Move - If there is a virtual desktop next to the current one
                Keep - If there is only one virtual desktop
            Minimize - If there is only one virtual desktop then minimize
        """    
        number_of_active_desktops = pyvda.GetDesktopCount()
        current_desktop = pyvda.GetCurrentDesktopNumber()

        # get appTitle
        appTitle = self.getAppTitle(appName)

        # pygetwindow instance
        appWindow = gw.getWindowsWithTitle(appTitle)[0]

        #win32gui instance
        appWindow_win32gui = win32gui.FindWindow(None, appTitle)

        # Get app native desktop
        appDesktop = pyvda.GetWindowDesktopNumber(appWindow_win32gui)

        if (number_of_active_desktops > 1):
            if ((appDesktop <= number_of_active_desktops) and (appDesktop != current_desktop)):
                # set appDesktop
               tempDesktop = appDesktop
            elif (appDesktop == current_desktop):
                if (current_desktop < number_of_active_desktops):
                        # set next desktop
                        tempDesktop = current_desktop+1
                else:
                        # set previous desktop
                        tempDesktop = current_desktop-1
        else:
            tempDesktop = current_desktop

        # Move app window to desktop
        pyvda.MoveWindowToDesktopNumber(appWindow_win32gui, tempDesktop)
        # Go to desktop
        pyvda.GoToDesktopNumber(tempDesktop)

        # Activate the window
        appWindow.activate()

        # Maximize the app window
        if (appWindow.isMaximized == False):
            appWindow.maximize()

        time.sleep(0.3)

        # record video    
        self.streamAppGUI(appTitle)

        # if it is a same desktop minimize the app window
        if (current_desktop == appDesktop):
            if (appWindow.isMaximized == True):
                appWindow.minimize()

        # go back to current desktop
        if (current_desktop != tempDesktop):        
            pyvda.GoToDesktopNumber(current_desktop)

        time.sleep(0.1)

def main():    
    vogtAppName = "Notepad"
    appGUIRecorder = AppGUIRecorder()
    appGUIRecorder.HandleAppOnDesktop(vogtAppName)

if __name__ == '__main__':
    main()