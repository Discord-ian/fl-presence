from pypresence import Presence
import time
import requests
import ctypes
import os
import webbrowser
import logging
import platform
import random
import string

dev_level = logging.DEBUG
onLaunch = True
EnumWindows = ctypes.windll.user32.EnumWindows
EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int))
GetWindowText = ctypes.windll.user32.GetWindowTextW
GetWindowTextLength = ctypes.windll.user32.GetWindowTextLengthW
IsWindowVisible = ctypes.windll.user32.IsWindowVisible
titles = []
storedTitle = ""
currentVersion = "1.9.0"

logger = logging.getLogger()
logger.setLevel(level=dev_level)


def foreach_window(hwnd, lParam):  # https://sjohannes.wordpress.com/2012/03/23/win32-python-getting-all-window-titles/
    if IsWindowVisible(hwnd):
        length = GetWindowTextLength(hwnd)
        buff = ctypes.create_unicode_buffer(length + 1)
        GetWindowText(hwnd, buff, length + 1)
        titles.append(buff.value)
    return True


def outputDebug():
    logging.info("StoredTitle = {} // rpcActive = {}".format(storedTitle, rpcActive))


def checkForUpdate():
    global rpcActive
    global storedTitle
    global titles
    EnumWindows(EnumWindowsProc(foreach_window), 0)
    testForFLP = [string for string in titles if ".flp" in string]
    testForUntitled = [string for string in titles if "FL Studio" in string]
    testForFLP = ''.join(testForFLP)
    testForUntitled = ''.join(testForUntitled)
    if testForFLP != "":  # it is not unnamed
        forCheck = testForFLP.split(".flp")[0]  # remove the .flp
    elif testForUntitled != "":
        if "Google Chrome" in testForUntitled:
            forCheck = ""
        else:
            forCheck = "Untitled"
    else:
        forCheck = ""
    if forCheck == "" and rpcActive:
        RPC.clear()  # kills the RPC when there is no FL Studio found to be running and it is stated as currently active
        rpcActive = False  # inform everything else that the RPC is closed
        storedTitle = ""
    details = "Project: {}".format(forCheck)
    if rpcActive and forCheck != storedTitle:
        storedTitle = forCheck
        RPC.update(large_image="main", state=phrase, details=details, start=time.time())
    elif forCheck != "" and not rpcActive:
        RPC.update(large_image="main", state=phrase, details=details, start=time.time())
        storedTitle = forCheck
        rpcActive = True
    print("StoredTitle = {} // rpcActive = {}".format(storedTitle, rpcActive))  # debug stuff
    titles = []  # prevent the list from looping


def checkIfLatest():
    print("Checking for update @ https://discordian.dev/dev/fl/latestversion")
    check = requests.get(url="https://discordian.dev/dev/fl/latestversion")
    if check.json()["version"] != currentVersion:
        box = ctypes.windll.user32.MessageBoxW(0,
                                               "There is an update available. You are on version {}, and the latest version is {}.".format(
                                                   currentVersion, check.json()["version"]), "Version Checker", 1)
        if box == 1:
            webbrowser.open('https://github.com/Discord-ian/fl-presence/releases')
            print("Opening webbrowser to https://github.com/Discord-ian/fl-presence/releases")
            os._exit(0)
    else:
        print("No update found")


658520672976502784

logging.info("If you get an error stating that the RPC handshake failed, Discord is probably not open")
while True:
    if onLaunch:
        RPC = Presence("658520672976502784")  # discord application ID
        try:
            RPC.connect()
        except Exception as e:  # TODO: fix generic exception
            onLaunch = True
            logging.warning("RPC handshake failed... trying again in 15 seconds")
        else:
            onLaunch = False
            try:
                checkIfLatest()
            except Exception as e:
                logging.debug(e)
            phrase = "Making Music"
        rpcActive = False
    checkForUpdate()
    time.sleep(15)  # blocking statement is ok in this case
