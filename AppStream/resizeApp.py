from re import search
import pygetwindow as gw
import pyautogui


vogtAppName = "Notepad"
browserName = "Firefox"
vogtAppWidthPerc = 40
browserAppWidthPerc = 60

# get screen size
scrWidth, ScrHeight = pyautogui.size()

# get all running application titles
allTitles = gw.getAllTitles()
# print(allTitles)

# get browser app title
for title in allTitles:
    if search("^.*"+browserName+"$", str(title)):
        browserApp = str(title)
        break

# get vogt app title
for title in allTitles:
    # if search(vogtAppName, str(title)):
    if search("^.*"+vogtAppName+"$", str(title)):
        vogtApp = str(title)

vogtAppWindow = gw.getWindowsWithTitle(vogtApp)[0]
browserAppWindow = gw.getWindowsWithTitle(browserApp)[0]

vogtAppWindowWidth = int((scrWidth*vogtAppWidthPerc)/100)
browserAppWindowWidth = int((scrWidth*browserAppWidthPerc)/100)

vogtAppWindow.resizeTo(vogtAppWindowWidth, ScrHeight)
browserAppWindow.resizeTo(browserAppWindowWidth, ScrHeight)

if (vogtAppWindow.topright.x != scrWidth):
    vogtAppWindow.moveTo(scrWidth-vogtAppWindow.size.width,0)

if (browserAppWindow.topleft.x != 0):
    browserAppWindow.moveTo(0,0)