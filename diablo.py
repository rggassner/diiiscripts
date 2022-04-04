from win32gui import GetWindowText, GetForegroundWindow
from PIL import Image
import keyboard, time, datetime, win32com.client, os
import pyautogui, json

#List with keys used to play
key_setup = ['z','x','c','v']

#Interval after searching for all skills
a_interval=0.1

#Interval after searching every skills
s_interval=0.1

#set the confidence level when searching images
confidence=0.9

#auxiliar variables
aux=-1
build=0

start_time=datetime.datetime.now()
speaker = win32com.client.Dispatch("SAPI.SpVoice")

#Read json into config
def read_conf():
    my_config=[]
    try:
        f = open('my_conf.json')
        my_config = json.load(f)
    except:
        pass
    #for every build, load the image file for every key
    for build in my_config:
        build['key_image']={}
        for key in build['keys']:
            build['key_image'][key]=Image.open(build['name']+"/"+key+".bmp")
    return my_config

def new_build(my_conf):
    build={}
    build['keys']={}
    build_name=str(len(my_conf)+1)
    os.mkdir(build_name)
    build['name']=build_name
    speaker.Speak('Setup')
    for ekey in key_setup:
        speaker.Speak("Key "+ ekey+ ". Move mouse to top left of skill and press shift.")
        while not keyboard.is_pressed('shift'):
            pass
        top_skill=pyautogui.position()
        speaker.Speak("Key "+ ekey+ ". Move mouse to bottom right of skill and press shift.")
        while not keyboard.is_pressed('shift'):
            pass
        bottom_skill=pyautogui.position()
        im = pyautogui.screenshot(region=[top_skill[0],top_skill[1],bottom_skill[0]-top_skill[0],bottom_skill[1]-top_skill[1]]) 
        im.save(build_name+"/"+ekey+".bmp")
        build['keys'][ekey]=[top_skill[0],top_skill[1],bottom_skill[0]-top_skill[0],bottom_skill[1]-top_skill[1]]
    my_conf.append(build)
    for build in my_conf:
        build.pop('key_image', None)
    with open('my_conf.json', 'w') as f:
        json.dump(my_conf, f)
    speaker.Speak("We're done setting up.")

my_conf=read_conf()

while 1:
    if GetWindowText(GetForegroundWindow()) == "Diablo III" and aux == 1:
        #for every key in the build
        for key in my_conf[build]['keys']:
            image_location=pyautogui.locateOnScreen(my_conf[build]['key_image'][key],confidence=confidence,region=my_conf[build]['keys'][key])
            if image_location:
                keyboard.press_and_release(key)
            time.sleep(s_interval)
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
    if keyboard.is_pressed('shift+s'):
        new_build(my_conf)
        my_conf=read_conf()
    time.sleep(a_interval)
