from win32gui import GetWindowText, GetForegroundWindow
import keyboard
#import mouse
import time
import datetime
import win32com.client
import os
import re
import pyautogui

speaker = win32com.client.Dispatch("SAPI.SpVoice")
#my_config = [{'name':'Greater Rift','keymap':{'./z.bmp':'z', './x.bmp':'x', './c.bmp':'c', './left.bmp':'left'} },{'name':'Bounties'}]

start_time=datetime.datetime.now()
interval_map = {'b':[3000,start_time]}

def read_conf():
    my_config=[]
    iterdir = iter(os.walk("."))
    next(iterdir)
    for root, dirs, files in iterdir:
        my_config.append({'name':root[2:]})
        my_config[len(my_config)-1]['keymap']={}
        for each_file in files:
            my_config[len(my_config)-1]['keymap'][each_file]=re.search('(.*)\.bmp', each_file, re.IGNORECASE).group(1)
    return my_config

#im_region=(startx,starty,width,height)
im_region=(1254,2000,800,126)

#set the confidence level when searching images
confidence=0.999

#set save_actionbar to False after setting up to gain performance
save_actionbar = False

aux=-1
build=0

my_conf=read_conf()
print (my_conf)

while 1:
    if GetWindowText(GetForegroundWindow()) == "Diablo III" and aux == 1:
        #save actionbar       
        if save_actionbar:
            #capture action bar
            im = pyautogui.screenshot(region=im_region) 
            im.save("actionbar.png")
        #for every image in the build directory
        for ifile in my_conf[build]['keymap']:
            image_location=pyautogui.locateOnScreen(my_conf[build]['name']+"/"+ifile,confidence=confidence,region=im_region)
            if image_location:
                if len(my_conf[build]['keymap'][ifile]) == 1:
                    keyboard.press_and_release(my_conf[build]['keymap'][ifile])
                else:
                    #keyboard.press('shift')
                    #mouse.click(my_conf[build]['keymap'][ifile])
                    #keyboard.release('shift')            
                    pass
        for item in interval_map:
            now=datetime.datetime.now()
            if int(((now - interval_map[item][1])*1000).seconds)  > interval_map[item][0]:
                keyboard.press_and_release(item)
                interval_map[item][1] = now
        time.sleep(0.1)
    if keyboard.is_pressed('shift+a'):
        aux=aux*-1
        if aux == 1:
            speaker.Speak('Starting '+str(my_conf[build]['name']))
        else:
            speaker.Speak('Waiting')
    if keyboard.is_pressed('shift+q'):
        if build == (len(my_conf)-1):
            build=0
        else:
            build=build+1
        speaker.Speak(my_conf[build]['name'])
    time.sleep(0.01)
#todo:
#setup build from shortcut
