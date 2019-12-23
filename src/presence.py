from pypresence import Presence, Activity 
import time
import requests
import ctypes
import os
import webbrowser
onLaunch = True
EnumWindows = ctypes.windll.user32.EnumWindows
EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int))
GetWindowText = ctypes.windll.user32.GetWindowTextW
GetWindowTextLength = ctypes.windll.user32.GetWindowTextLengthW
IsWindowVisible = ctypes.windll.user32.IsWindowVisible
titles = []
storedTitle = ""


def foreach_window(hwnd, lParam):
	if IsWindowVisible(hwnd):
		length = GetWindowTextLength(hwnd)
		buff = ctypes.create_unicode_buffer(length + 1)
		GetWindowText(hwnd, buff, length + 1)
		titles.append(buff.value)
	return True


def checkForUpdate():
	global rpcActive
	global storedTitle
	global titles
	EnumWindows(EnumWindowsProc(foreach_window), 0)
	testForFLP = [string for string in titles if ".flp" in string]
	testForUntitled = [string for string in titles if "FL Studio" in string]
	testForFLP = ''.join(testForFLP)
	testForUntitled = ''.join(testForUntitled)
	if testForFLP is not "": # it is not unnamed
		forCheck = testForFLP.split(".flp")[0] # remove the .flp
	elif testForUntitled is not "":
		forCheck = "Untitled"
	else:
		forCheck = ""
	if forCheck is "" and rpcActive:
		RPC.clear()  # kills the RPC when there is no FL Studio found to be running and it is stated as currently active
		rpcActive = False  # inform everything else that the RPC is closed
		storedTitle = ""
	details = "Project: {}".format(forCheck)
	if rpcActive and forCheck != storedTitle:
		storedTitle = forCheck
		RPC.update(large_image="main", state=phrase, details=details, start=time.time())
	elif forCheck is not "" and not rpcActive:
		RPC.update(large_image="main", state=phrase, details=details, start=time.time())
		storedTitle = forCheck
		rpcActive = True
	print("StoredTitle = {} // rpcActive = {}".format(storedTitle, rpcActive))  # debug stuff
	titles = []  # prevent the list from looping


def checkIfLatest():
	print("Checking for update @ https://im-stuck-in.space/dev/fl/latestversion")
	currentVersion = "1.0.0"
	check = requests.get(url="https://im-stuck-in.space/dev/fl/latestversion")
	if check.json()[0] != currentVersion:
		box = ctypes.windll.user32.MessageBoxW(0, "There is an update available. You are on version {}, and the latest version is {}.".format(currentVersion,check.json()[0]), "Version Checker", 1)
		if box == 1:
			webbrowser.open('https://github.com/Discord-ian/fl-presence/releases')
			print("Opening webbrowser to https://github.com/Discord-ian/fl-presence/releases")
			os._exit(0)
	else:
		print("No update found")


while True:
	if onLaunch:
		# with open('config.json') as userCfg:
		#	data = json.load(userCfg) might add back at a later date
		RPC = Presence("658520672976502784")  # discord application ID
		try:
			RPC.connect()
		except Exception as e:
			onLaunch = True
			print("trying again.")
		else:
			onLaunch = False
			checkIfLatest()
			phrase = "Making Music"
		rpcActive = False
	checkForUpdate()
	time.sleep(15)
	print("----------------------")