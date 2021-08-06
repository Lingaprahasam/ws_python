import win32gui
import win32con
import win32ui
import win32api
from ctypes import windll
from PIL import Image

#here you have to specify the name of the window (or the class of window)
hwnd = win32gui.FindWindow(None, 'Untitled - Notepad')

# print(hwnd)

#if the window is minimized, restore it
long=win32gui.GetWindowLong(hwnd,win32con.GWL_STYLE)
if long & win32con.WS_MINIMIZE:
    win32gui.ShowWindow(hwnd,win32con.SW_SHOWNORMAL)

#here you can set the position of the window
# win32gui.SetWindowPos(hwnd,win32con.HWND_BOTTOM,100,100,200,200,0)
width = win32api.LOWORD(500)
height = win32api.HIWORD(500)
win32gui.SetWindowPos(hwnd, win32con.HWND_TOP, 0, 0, width, height, win32con.SWP_SHOWWINDOW)

#stuff to prepare a bitmap image screenshot
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

#if it succeeded in printing the window, we can show it
if result == 1:
    im.show()
    im.save("dump.png")

#clean up stuff. This should not run every frame!
win32gui.DeleteObject(saveBitMap.GetHandle())
saveDC.DeleteDC()
mfcDC.DeleteDC()
win32gui.ReleaseDC(hwnd, hwndDC)
