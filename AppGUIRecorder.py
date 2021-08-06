from re import search
import pyvda
import pygetwindow as gw
import win32gui
import cv2
import pyautogui
import numpy as np
import time

class AppGUIRecorder():
    def __init__(self, appName='Notepad'):
        self.appName = appName
        self.appTitle = self.getAppTitle()        
        self.number_of_active_desktops = pyvda.GetDesktopCount()
        self.current_desktop = pyvda.GetCurrentDesktopNumber()
        self.tempDesktop=self.current_desktop


    def getAppTitle(self):
        """
            returns first application title matches the appName
        """
        appTitle = None

        # get all running application titles
        allTitles = gw.getAllTitles()
        # print(allTitles)

        try:
            # get app title
            for title in allTitles:
                if search("^.*"+self.appName.upper()+"$", str(title).upper()):
                    appTitle = str(title)
                    break
            
            if (appTitle == None):
                print ("Application \"" + str(self.appName) + "\" Not Found")
            else:
                return appTitle
        except Exception as e:
            print ("Can't find the application name")


    def streamAppGUI(self):
        """ 
            Stream application gui interface as cv2 COLOR_RGB2BGR array format
        """
        imgCV = []

        if (self.appTitle == None):
            return imgCV

        # Go to desktop
        pyvda.GoToDesktopNumber(self.tempDesktop)

        appWindow = gw.getWindowsWithTitle(self.appTitle)[0]

        # Activate the window
        appWindow.activate()

        # Maximize the app window
        if (appWindow.isMaximized == False):
            appWindow.maximize()

        time.sleep(0.3)

        image = pyautogui.screenshot(region=(appWindow.topleft.x,appWindow.topleft.y, appWindow.size.width, appWindow.size.height))
        image.save(r"C:\Users\selis\Documents\screenshot.png")
        imgCV = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

        return imgCV


    def MoveApptoAnotherDesktop(self):
        """ 
            Move - if more than one virtual desktop
            Keep - If there is only one virtual desktop
            Minimize the app - If there is only one virtual desktop

        """
    
        if (self.appTitle == None):
            return

        # pygetwindow instance
        appWindow = gw.getWindowsWithTitle(self.appTitle)[0]

        #win32gui instance
        appWindow_win32gui = win32gui.FindWindow(None, self.appTitle)

        # Get app desktop number
        appDesktop = pyvda.GetWindowDesktopNumber(appWindow_win32gui)

        if (self.number_of_active_desktops > 1):
            if ((appDesktop <= self.number_of_active_desktops) and (appDesktop != self.current_desktop)):
                # set appDesktop
               self.tempDesktop = appDesktop
            elif (appDesktop == self.current_desktop):
                if (self.current_desktop < self.number_of_active_desktops):
                        # set next desktop
                        self.tempDesktop = self.current_desktop+1
                else:
                        # set previous desktop
                        self.tempDesktop = self.current_desktop-1
        else:
            self.tempDesktop = self.current_desktop

        # Move app window to desktop
        pyvda.MoveWindowToDesktopNumber(appWindow_win32gui, self.tempDesktop)
        

    def RestoreCurrentDesktop(self):
        if (self.appTitle == None):
            return
        
        # if it is a same desktop minimize the app window
        if (self.current_desktop == self.tempDesktop):
            # pygetwindow instance
            appWindow = gw.getWindowsWithTitle(self.appTitle)[0]
            
            if (appWindow.isMaximized == True):
                appWindow.minimize()

        # restore current desktop
        if (self.current_desktop != self.tempDesktop):
            print(self.current_desktop)
            pyvda.GoToDesktopNumber(self.current_desktop)

        time.sleep(0.1)


def main():    
    vogtAppName = "Paint"
        
    try:
        appGUIRecorder = AppGUIRecorder(vogtAppName)

        appGUIRecorder.MoveApptoAnotherDesktop()

        imgCV = appGUIRecorder.streamAppGUI()

        if (imgCV != []):
            # display an image
            cv2.imshow("test image", imgCV)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

        # appGUIRecorder.RestoreCurrentDesktop()
    except Exception as e:
        print("AppGUIRecorder Error: " + str(e))


if __name__ == '__main__':
    main()