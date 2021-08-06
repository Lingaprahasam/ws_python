import win32gui
import win32con
import win32ui
import win32api
from ctypes import windll
from PIL import Image
import pygetwindow as gw
import pyautogui
from re import search
import pyvda
import numpy as np
import cv2
import pynput
import mss

class ScreenGrabberStreamError(Exception):
    """Base class for other exceptions"""
    pass

class ScreenGrabberAppNotFound(Exception):
    """Base class for other exceptions"""
    pass

class ScreenGrabberMoveAppError(Exception):
    """Base class for other exceptions"""
    pass

class ScreenGrabber():
    def __init__(self, appName=None):
        self.appName = appName        
        self.number_of_active_desktops = pyvda.GetDesktopCount()
        self.current_desktop = pyvda.GetCurrentDesktopNumber()
        self.tempDesktop=self.current_desktop
        # get screen size
        self.scrWidth, self.scrHeight = pyautogui.size()
        
        self.cropWindow = False
        # default invisible window border
        self.windowBorder = 8
        
        try:
            self.appTitle = self.getAppTitle()
        except ScreenGrabberAppNotFound:
            raise ScreenGrabberAppNotFound
    
    def getAppTitle(self):
        """returns first application title matches the appName
        """
        appTitle = None

        # get all running application titles
        allTitles = gw.getAllTitles()

        try:
            # get app title
            for title in allTitles:                
                if search("^.*"+self.appName.lower()+"$", str(title).lower()):                        
                    appTitle = str(title)
                    break
            return appTitle

        except Exception as e:
            raise ScreenGrabberAppNotFound
        
    def MaximizeApp(self):
        """Maximize the application
        """
        appWindow = gw.getWindowsWithTitle(self.appTitle)[0]

        # Activate the window
        # appWindow.restore()

        # Maximize the app window
        if (appWindow.isMaximized == False):
            appWindow.maximize()

    def SetAppToFullScreen(self):
        """Set the application to full screen
        """
        appWindow = gw.getWindowsWithTitle(self.appTitle)[0]

        # if (appWindow.topleft.x != -1*self.windowBorder):
            # appWindow.moveTo(0-self.windowBorder,0)
            # appWindow.moveTo(0,0)

        if((appWindow.width != self.scrWidth+(2*self.windowBorder)) or (appWindow.height != self.scrHeight)):
            appWindow.resizeTo(self.scrWidth+(2*self.windowBorder), self.scrHeight)
    
    def streamAppGUI(self):
        """Stream application gui interface
        """
        hwnd = win32gui.FindWindow(None, self.appTitle)

        # get the size of the app window
        appWindow = gw.getWindowsWithTitle(self.appTitle)[0]
        win32gui.SetWindowPos(hwnd, win32con.HWND_TOP, appWindow.topleft.x,appWindow.topleft.y, appWindow.size.width, appWindow.size.height, win32con.SWP_SHOWWINDOW)
        left, top, right, bot = win32gui.GetWindowRect(hwnd)

        hwndDC = win32gui.GetWindowDC(hwnd)
        mfcDC  = win32ui.CreateDCFromHandle(hwndDC)
        saveDC = mfcDC.CreateCompatibleDC()
        saveBitMap = win32ui.CreateBitmap()
        saveBitMap.CreateCompatibleBitmap(mfcDC, right-left, bot-top)        
        saveDC.SelectObject(saveBitMap)

        #here is the main part. It grabs the window image based on parameters berfore
        result = windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 0)
        bmpinfo = saveBitMap.GetInfo()
        bmpstr = saveBitMap.GetBitmapBits(True)

        #create an image object that we can look at
        im = Image.frombuffer('RGB',(bmpinfo['bmWidth'], bmpinfo['bmHeight']),bmpstr, 'raw', 'BGRX', 0, 1)
        print(im)

        #if it succeeded in printing the window, we can show it
        if result == 1:
            im.show()
            im.save("dump.png")

        #clean up stuff. This should not run every frame!
        win32gui.DeleteObject(saveBitMap.GetHandle())
        saveDC.DeleteDC()
        mfcDC.DeleteDC()
        win32gui.ReleaseDC(hwnd, hwndDC)
    
    def streamAppGUIAsCV(self):
        """Stream application gui interface in CV format
        """
        try:
        
            hwnd = win32gui.FindWindow(None, self.appTitle)

            # get the size of the app window
            appWindow = gw.getWindowsWithTitle(self.appTitle)[0]
            win32gui.SetWindowPos(hwnd, win32con.HWND_TOP, appWindow.topleft.x,appWindow.topleft.y, appWindow.size.width, appWindow.size.height, win32con.SWP_SHOWWINDOW)
            left, top, right, bot = win32gui.GetWindowRect(hwnd)

            hwndDC = win32gui.GetWindowDC(hwnd)
            mfcDC  = win32ui.CreateDCFromHandle(hwndDC)
            saveDC = mfcDC.CreateCompatibleDC()
            bmp = win32ui.CreateBitmap()
            bmp.CreateCompatibleBitmap(mfcDC, right-left, bot-top)        
            saveDC.SelectObject(bmp)

            #here is the main part. It grabs the window image based on parameters berfore
            result = windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 0)
            bmpinfo = bmp.GetInfo()
            bmpstr = bmp.GetBitmapBits(True)

            #create an image object that we can look at
            signedIntsArray = bmp.GetBitmapBits(True)
            img = np.fromstring(signedIntsArray, dtype='uint8')
            img.shape = (appWindow.size.height,appWindow.size.width,4)

            mfcDC.DeleteDC()
            saveDC.DeleteDC()
            win32gui.ReleaseDC(hwnd, hwndDC)
            win32gui.DeleteObject(bmp.GetHandle())

            # cvImg = cv2.cvtColor(img, cv2.COLOR_BGRA2RGB)
            cvImg = cv2.cvtColor(img, cv2.COLOR_RGB2RGBA)

            # crop image
            if self.cropAppWindow:
                resultImg = cvImg[self.startY:self.endY, self.startX:self.endX]
            else:
                resultImg = cvImg

            return resultImg
        except:
            # raise Exception("ScreenGrabber: streamAppGUIAsCV Error")
            # print("ScreenGrabber: streamAppGUIAsCV Error")
            raise ScreenGrabberStreamError
    
    def streamAppGUIMSS(self, left=1920, top=0, width=500, height=500):
        """Stream application gui interface from monitor number specified in CV format
        """
        monitor = {'left': left, 'top': top, 'width': width, 'height': height}

        try:
            with mss.mss() as sct:
                # Get raw pixels from the screen, save it to a Numpy array
                # img = np.array(sct.grab(monitor))
                img = np.array(sct.grab(sct.monitors[2]))

                # crop image
                if self.cropAppWindow:
                    resultImg = img[self.startY:self.endY, self.startX:self.endX]
                else:
                    resultImg = img

                

                return resultImg
        except Exception as e:            
            print("ScreenGrabber: " + str(e))
            raise ScreenGrabberStreamError
    
    def MoveApptoAnotherVirtualDesktop(self):
        """ Move - if more than one virtual desktop
            Keep - If there is only one virtual desktop
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

    def MoveApptoAnotherMonitor(self):
        """ Moves the application to another monitor
        """
    
        if (self.appTitle == None):
            return

        # pygetwindow instance
        appWindow = gw.getWindowsWithTitle(self.appTitle)[0]

        with mss.mss() as sct:
            print (sct.monitors[1])
            print (sct.monitors[2])

    def cropAppWindow(self, startY=98, endY=960, startX=50, endX=910):
        '''crops the application window image
        '''
        self.cropWindow = True
        self.startY = startY
        self.endY = endY
        self.startX = startX
        self.endX = endX

def main1():
    # vogtAppName = "Paint"
    vogtAppName = "PHAsis"
    imgCV = None

    from pynput.keyboard import Listener

    try:
        appGUIRecorder = ScreenGrabber(vogtAppName)
    except ScreenGrabberAppNotFound:
        print('Application ' + vogtAppName + ' is not found')
        return       

    try:
        # appGUIRecorder = ScreenGrabber(vogtAppName)
        appGUIRecorder.MaximizeApp()
        # appGUIRecorder.MoveApptoAnotherVirtualDesktop()
        appGUIRecorder.cropAppWindow()
        
        # appGUIRecorder.SetAppToFullScreen()
        appGUIRecorder.MoveApptoAnotherMonitor()

        while True:
            try:
                # appGUIRecorder.SetAppToFullScreen()
                # imgCV = appGUIRecorder.streamAppGUIAsCV()
                imgCV = appGUIRecorder.streamAppGUIMSS()

                if (imgCV != []):                
                    # display an image
                    cv2.imshow("test image", imgCV)
                    cv2.waitKey(0)
                    break
                if cv2.waitKey(25) & 0xFF == ord('q'):
                    cv2.destroyAllWindows()
                    break
            except ScreenGrabberStreamError:
                print("ScreenGrabberStreamError")
                break
                # continue

    except KeyboardInterrupt:
        cv2.imshow("snap image", imgCV)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    except Exception as e:
        print(str(e))

def main():
    vogtAppName = "Paint"
    imgCV = None

    from pynput.keyboard import Listener

    while True:

        try:
            appGUIRecorder = ScreenGrabber(vogtAppName)
            # appGUIRecorder.MaximizeApp()
            
            appGUIRecorder.MoveApptoAnotherDesktop()
            appGUIRecorder.cropAppWindow()


            while True:
                try:
                    appGUIRecorder.SetAppToFullScreen()
                    imgCV = appGUIRecorder.streamAppGUIAsCV()

                    if (imgCV != []):                
                        # display an image
                        cv2.imshow("test image", imgCV)
                    if cv2.waitKey(25) & 0xFF == ord('q'):
                        cv2.destroyAllWindows()
                        break
                except ScreenGrabberStreamError as e:
                    print("Error Streaming: " + str(e))
                    continue

                print('Record while loop Ends')

        except KeyboardInterrupt:
            cv2.imshow("snap image", imgCV)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

    print('Program Ends')

        


if __name__ == '__main__':
    main1()


