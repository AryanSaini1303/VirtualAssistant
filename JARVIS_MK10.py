#takes query through voice for as long as you speak and gives response through voice as well as text(listens for 5 seconds as of now)
#have features like stop listening and start listening
#tells accurate time and date
#takes input as voice as well as text
#searches on google,flipkart,amazon,ajio,myntra,nykaa,youtube (default search engine is google)
#plays videos on youtube
#play,pause,mute,unmute,set volume to a specified level and also increase/decrease volume by a specified factor viz.10
#plays next/previous track for spotify only
#scroll up/down, close window
#remembers conversation until it's closed so that it can take references from past conversation to answer and once the program is closed, it erases all the conversation except the one which is important(the one which is instructed to remember)
#uses natural language processing to recognize the meaning of the sentence/input(no need to learn predefined commands)

#importing all the libraries
import pyttsx3
import openai
import speech_recognition as sr
import datetime
import re
import subprocess
import webbrowser
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googlesearch import search
import pyautogui
import comtypes
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import keyboard
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import win32gui
import win32con
import os
from playsound import playsound
import spacy

#function to give a response
def responseProtocol(response):
    if response!="":  
        print(response)
        engine.say(response)
        engine.runAndWait()

#function to save all conversation
def writeInMemory(text,response):
    with open('Conversation.txt', 'a') as file:
        try:
            file.write(('User:'+text))
        except UnicodeEncodeError:
            file.write(('User:'))
    with open('Conversation.txt', 'a') as file:
        try:
            file.write("\n"+"Jarvis: "+response+"\n\n")
        except UnicodeEncodeError:
            file.write("\n"+"Jarvis: "+"\n\n")

openai.api_key="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" 
model_engine="text-davinci-003"
engine = pyttsx3.init()#used to convert text to speech
r = sr.Recognizer()#used to recognize voice and conver it to text
youtube = build('youtube', 'v3', developerKey="AIzaSyCqf5WsmtFlfL7PZhHH59diqC3KQ39Alvo")#used in playing videos on youtube
nlp = spacy.load("en_core_web_lg")#used in natural language processing

#inital greeting
current_time = datetime.datetime.now().time()
if current_time.hour < 12:
    response="Good morning sir, How can i be of assistance?"
    responseProtocol(response)
elif 12 <= current_time.hour < 18:
    response="Good afternoon sir, How can i be of assistance?"
    responseProtocol(response)
else:
    response="Good evening sir, How can i be of assistance?"
    responseProtocol(response)
    
#similarity strings
closing1=nlp("thank you, goodbye jarvis")
closing2=nlp("bye")
closing3=nlp("close jarvis")
closing4=nlp("goodbye jarvis")
closing5=nlp("that's all for now goodbye jarvis")
stopListening1=nlp("jarvis stop listening")
stopListening2=nlp("jarvis stop listening for a bit")
startListening1=nlp("jarvis start listening")
startListening2=nlp("okay jarvis wake up")
openApps=nlp("jarvis, please open")
searchFor=nlp("search for")
playOnYT=nlp("play on youtube")
setVolume=nlp("jarvis, set volume to some percent")
setVolume1=nlp("set volume to some %")
play=nlp("jarvis play the music")
play1=nlp("play song")
pause=nlp("jarvis pause the music")
pause1=nlp("pause this")
pause2=nlp("pause song")
mute=nlp("jarvis mute the music")
unmute=nlp("jarvis unmute the music")
mute1=nlp("mute")
unmute1=nlp("unmute")
mute2=nlp("mute it")
unmute2=nlp("unmute it")
scroll=nlp("scroll up/down the content a bit")
closeWindow=nlp("jarvis please close window")
switchWindow=nlp("jarvis please switch the window")
switchtab=nlp("jarvis please switch tab")
showAllTabs=nlp("show all my the tabs")
lock=nlp("lock my desktop jarvis")
lock1=nlp("lock my workstation jarvis")
ytFullscreen=nlp("play video on fullscreen")
ytFullscreen1=nlp("make youtube video fullscreen")
ytFullscreen2=nlp("youtube fullscreen")
exitYTFullscreen=nlp("exit youtube fullscreen")
time=nlp("what time is it?")
date=nlp("what date is it?")
time1=nlp("tell me the time")
date1=nlp("tell me the date")
increaseVolume=nlp("volume increased by ")
decreaseVolume=nlp("volume decreased by ")

# choose input as text or voice
choice=input("Enter your mode of input 't' for text and ('v' or press enter) for voice: ")

#main loop starts
while True:
    # checks for the mode of input
    if choice=="t":
        text=input("\n"+"Enter query:")
    else:
        with sr.Microphone() as source:
            print("\n"+"Say something!")
            playsound('./mixkit-click-error-1110.wav')
            audio=r.record(source,duration=5)
            # r.pause_threshold=0.8#seconds
            # r.adjust_for_ambient_noise(source)
            # audio = r.listen(source)
        try:
            text = r.recognize_google(audio,language='en-IN')
            print("You said: ", text)
        except sr.UnknownValueError:
            print("Can't understand audio, Try again.")
            continue
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))
            continue
    
    # deciding output based on different inputs i.e text
    if (((nlp(text.lower())).similarity(closing1)>=0.7) or ((nlp(text.lower())).similarity(closing2)>=0.7) or ((nlp(text.lower())).similarity(closing4)>=0.7) or ((nlp(text.lower())).similarity(closing3)>=0.7) or ((nlp(text.lower())).similarity(closing5)>=0.7)) and (nlp(text.lower())).similarity(startListening1)<0.7 and (0.7>nlp(text.lower()).similarity(closeWindow)) and ("close" in text.lower() or "goodbye" in text.lower() or "bye" in text.lower()):
        response="i hope i was helpful, Until next time sir."
        responseProtocol(response)
        writeInMemory(text,response)
        with open("Conversation.txt","r") as f:
            lines=f.readlines()
        with open("Conversation.txt","w") as f:
            i=0
            while i<(len(lines)):
                if lines[i].lower().strip().startswith("remember that") or lines[i].lower().strip().startswith("remember this") or lines[i].lower().strip().endswith("remember that") or lines[i].lower().strip().endswith("remember this") or  lines[i].lower().strip().startswith("jarvis remember that") or lines[i].lower().strip().startswith("jarvis remember this"):
                    f.write(lines[i])
                    f.write(lines[i+1]+"\n")
                i+=1
        break
    elif(nlp(text.lower()).similarity(time)>0.7 or nlp(text.lower()).similarity(date)>0.7 or nlp(text.lower()).similarity(time1)>0.7 or nlp(text.lower()).similarity(date1)>0.7) and ("time" in text.lower() or "date" in text.lower()):
        if "time" in text.lower():
            current_time=datetime.datetime.now().strftime("%I:%M %p")
            response="It's "+current_time
            responseProtocol(response)
            writeInMemory(text,response)
        elif "date" in text.lower():
            current_date=datetime.date.today()
            response="Today is "+str(current_date)
            responseProtocol(response)
            writeInMemory(text,response)
    elif ((nlp(text.lower())).similarity(stopListening1)>=0.75 or (nlp(text.lower())).similarity(stopListening2)>=0.75) and ((nlp(text.lower())).similarity(stopListening1)>(nlp(text.lower())).similarity(startListening1)) and ("stop listening" in text.lower()):
        response="Going to sleep mode"
        responseProtocol(response)
        writeInMemory(text,response)
        while True:
            if choice=="t":
                text=input("\nEnter query:")
            else:
                with sr.Microphone() as source:
                    print("\n"+"Say something!")
                    audio=r.record(source,duration=5)
                    # r.pause_threshold=0.8#seconds
                    # r.adjust_for_ambient_noise(source)
                    # audio = r.listen(source)
                try:
                    text = r.recognize_google(audio,language='en-IN')
                except sr.UnknownValueError:
                    print("Can't understand audio, Try again.")
                    continue
                except sr.RequestError as e:
                    print("Could not request results from Google Speech Recognition service; {0}".format(e))
                    continue
            if ((nlp(text.lower())).similarity(startListening1)>=0.75 or (nlp(text.lower())).similarity(startListening2)>=0.75) and ((nlp(text.lower())).similarity(startListening1)>(nlp(text.lower())).similarity(stopListening1)) and ("start listening" in text.lower() or "wake up" in text.lower()):
                print("You said: ", text)
                response="Coming back online"
                responseProtocol(response)
                writeInMemory(text,response)
                break
            else:
                continue
    elif (nlp(text.lower())).similarity(openApps)>=0.75 and ((nlp(text.lower())).similarity(switchWindow)<(nlp(text.lower())).similarity(openApps)) and ("open" in text.lower()):
        app=""
        words=text.split()
        index=words.index("open")
        if index+1<len(words):
            app=words[index+1]
            if app.lower()=="prime" or app.lower()=="Prime":
                app="primevideo"
            response="Opening "+app
        responseProtocol(response)
        writeInMemory(text,response)
        if app.lower()=="amazon":
            try:
                subprocess.Popen([app+'.exe'])
            except Exception:
                url='https://'+app+'.in'
                webbrowser.open_new_tab(url)
            continue
        else:
            try:
                subprocess.Popen([app+'.exe'])
            except Exception:
                url='https://'+app+'.com'
                webbrowser.open_new_tab(url)
            continue
    elif "play next track" in text.lower() or "play the next track" in text.lower() or "play previous track" in text.lower() or "play the previous track" in text.lower() or "play next song" in text.lower() or "play the next song" in text.lower() or "play previous song" in text.lower() or "play the previous song" in text.lower():#works only for spotify
        if "previous" in text.lower():
            sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id="79598783a6e84d75bc48e52cf5548511",
            client_secret="7101c8145ac34784b30ea8d08b4177b5",
            redirect_uri="http://localhost:8080",
            scope="user-read-playback-state,user-modify-playback-state"))
            sp.previous_track()
        elif "next" in text.lower():
            sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id="79598783a6e84d75bc48e52cf5548511",
            client_secret="7101c8145ac34784b30ea8d08b4177b5",
            redirect_uri="http://localhost:8080",
            scope="user-read-playback-state,user-modify-playback-state"))
            sp.next_track()
    elif (((nlp(text.lower())).similarity(play)>=0.7) or ((nlp(text.lower())).similarity(pause)>=0.7) or ((nlp(text.lower())).similarity(pause1)>=0.7) or ((nlp(text.lower())).similarity(play1)>=0.7) or ((nlp(text.lower())).similarity(pause2)>=0.7)) and (((nlp(text.lower())).similarity(mute)<(nlp(text.lower())).similarity(play)) or ((nlp(text.lower())).similarity(unmute)<(nlp(text.lower())).similarity(pause))) and ("play" in text.lower() or "pause" in text.lower()) and ("youtube" not in text.lower()):
        pyautogui.press("playpause")
    elif ((nlp(text.lower())).similarity(setVolume)>=0.7 or (nlp(text.lower())).similarity(setVolume1)>=0.7) and ((nlp(text.lower())).similarity(switchWindow)<(nlp(text.lower())).similarity(setVolume)) and ("volume" in text.lower()):
        words=text.split()
        if words[-1].lower()=="percent" or words[-1].lower()=="percentage" or words[-1].lower()=="%":
            words=words[:-1]
        if words[-1][-1].lower()=="%":
            words[-1]=words[-1][:-1]
        newLevel=int(words[-1])
        print(newLevel)
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(
            IAudioEndpointVolume._iid_, 
            comtypes.CLSCTX_ALL, 
            None
        )
        volume = interface.QueryInterface(IAudioEndpointVolume)
        scalar = volume.GetMasterVolumeLevelScalar()
        level=int(scalar*100)                        
        if  level-newLevel>0:
            factor=int((level-newLevel)/2)                
            pyautogui.press('volumedown', presses=factor)
        else:
            factor=int((-1)*((level-newLevel)/2))                
            pyautogui.press('volumeup', presses=factor)
    elif ((nlp(text.lower())).similarity(mute)>=0.75 or (nlp(text.lower())).similarity(unmute)>=0.75 or (nlp(text.lower())).similarity(mute1)>=0.75 or (nlp(text.lower())).similarity(unmute1)>=0.75 or (nlp(text.lower())).similarity(mute2)>=0.75 or (nlp(text.lower())).similarity(unmute2)>=0.75) and ("mute" in text.lower() or "unmute" in text.lower()):
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(
            IAudioEndpointVolume._iid_, 
            comtypes.CLSCTX_ALL, 
            None
        )
        volume = interface.QueryInterface(IAudioEndpointVolume)
        if "unmute" in text.lower():
            volume.SetMute(0, None)
        elif "mute" in text.lower():
            volume.SetMute(1,None)
    elif (nlp(text.lower())).similarity(scroll)>=0.75 and (nlp(text.lower())).similarity(closeWindow)<(nlp(text.lower())).similarity(scroll) and ("scroll" in text.lower()):
            i=800
            sensi=i
            if "down" in text.lower():
                sensi=-i
            pyautogui.scroll(sensi)
    elif (nlp(text.lower())).similarity(closeWindow)>0.75 and ((nlp(text.lower())).similarity(closeWindow)>(nlp(text.lower())).similarity(switchWindow)) and ("close" in text.lower()):
        window = win32gui.GetForegroundWindow()
        win32gui.PostMessage(window, win32con.WM_CLOSE, 0, 0)
    elif (nlp(text.lower())).similarity(switchWindow)>0.75 and (nlp(text.lower())).similarity(switchtab)<(nlp(text.lower())).similarity(switchWindow) and ("switch" in text.lower() or "change" in text.lower()):
        pyautogui.hotkey('alt', 'tab')
    elif (nlp(text.lower())).similarity(switchtab)>0.75 and (nlp(text.lower())).similarity(switchtab)>(nlp(text.lower())).similarity(switchWindow) and (nlp(text.lower())).similarity(switchtab)>(nlp(text.lower())).similarity(showAllTabs) and ("switch" in text.lower or "change" in text.lower()):
        pyautogui.hotkey('ctrl', 'tab')
    elif (nlp(text.lower())).similarity(showAllTabs)>0.75 and ("show" in text.lower()):
        pyautogui.hotkey("win","tab")
    elif ((nlp(text.lower())).similarity(lock)>0.75 or (nlp(text.lower())).similarity(lock1)>0.75) and ("lock" in text.lower()):
        os.system("rundll32.exe user32.dll, LockWorkStation")
    elif ((nlp(text.lower())).similarity(ytFullscreen)>0.8 or (nlp(text.lower())).similarity(ytFullscreen1)>0.8 or (nlp(text.lower())).similarity(exitYTFullscreen)>0.75 or (nlp(text.lower())).similarity(ytFullscreen2)>0.75) and ("fullscreen" in text.lower() or "full screen" in text.lower()):
        pyautogui.hotkey('f')
    elif text.lower().strip().startswith("remember that") or text.lower().strip().startswith("remember this") or text.lower().strip().endswith("remember that") or text.lower().strip().endswith("remember this") or  text.lower().strip().startswith("jarvis remember that") or text.lower().strip().startswith("jarvis remember this"):
        response="okay i'll remember that."
        responseProtocol(response)
        writeInMemory(text,response)
    else:
        with open('Conversation.txt', 'a') as file:
            file.write(('User:'+text))
        with open('Conversation.txt', 'r') as file:
            prompt= file.read()
        completion = openai.Completion.create(
            engine=model_engine,
            prompt=prompt,
            max_tokens=256,
            n=1,
            stop=None,
            temperature=0.5,
        )
        response1 = completion.choices[0].text.strip()
        words=response1.split()
        if "Jarvis:" in words:
            words.remove("Jarvis:")
        response=" ".join(words)
        
        #deciding output based on different responses by the model i.e. response
        if (nlp(response.lower()).similarity(increaseVolume) or nlp(response.lower()).similarity(decreaseVolume)) and ("volume" in response.lower()):
            i=0
            words=text.split()
            if words[-1]=="percent" or words[-1]=="percentage":
                words=words[:-1]
            if words[-1][-1]=="%":
                words[-1]=words[-1].replace("%",'')
            factor=int(words[-1])
            for i in range(int(factor/2)):
                if "decreased" in response:
                    keyboard.press_and_release('volume down')
                elif "increased" in response:
                    keyboard.press_and_release('volume up')
                i+=1
            response=""
        elif (("searching for" in response.lower()) and ("on youtube" in response.lower() or "on google" in response.lower() or "on flipkart" in response.lower() or "on prime video" in response.lower() or "on primevideo" in response.lower() or "on amazon" in response.lower() or "on myntra" in response.lower() or "on ajio" in response.lower() or "on nykaa" in response.lower())) or ("search for"in text.lower() and "on google" in text.lower()):
            appName=""
            words=text.lower().split()
            pattern = r'(?i)\b(flipkart|google|youtube|amazon|myntra|ajio|nykaa|video|primevideo)\b'
            appList= re.findall(pattern, text.lower())
            for x in appList:
                appName=x
            words=words[2:]
            if appName=="video":
                text=text.lower().replace("prime video","primevideo")
                appList=re.findall(pattern,text)
                for x in appList:
                    appName=x
            start_index=text.lower().index("for") + 4
            end_index=text.lower().index("on "+appName)
            searchQuery=text[start_index:end_index].strip()
            if appName.lower()=="flipkart" or appName.lower()=="google" or appName.lower()=="youtube":
                url = "https://www."+appName.lower()+".com/search?q=" + searchQuery
                response="Searching for "+searchQuery+" on "+appName
                responseProtocol(response)
                writeInMemory(text,response)
            elif appName.lower()=="amazon":
                url = "https://www.amazon.in/s?k=" +searchQuery
                response="Searching for "+searchQuery+" on "+appName
                responseProtocol(response)
                writeInMemory(text,response)
            elif appName.lower()=="myntra":
                url = "https://www.myntra.com/"+searchQuery+"?rawQuery="+searchQuery
                response="Searching for "+searchQuery+" on "+appName
                responseProtocol(response)
                writeInMemory(text,response)
            elif appName.lower()=="ajio":
                url = "https://www.ajio.com/search/?text="+searchQuery
                response="Searching for "+searchQuery+" on "+appName
                responseProtocol(response)
                writeInMemory(text,response)
            elif appName.lower()=="nykaa":
                url = "https://www.nykaa.com/search/result/?q="+searchQuery+"&root=search&searchType=Manual&sourcepage=Search+Page"
                response="Searching for "+searchQuery+" on "+appName
                responseProtocol(response)
                writeInMemory(text,response)
            elif appName.lower()=="primevideo":
                url = "https://www.primevideo.com/search/ref=atv_nb_sug?ie=UTF8&phrase="+searchQuery
                response="Searching for "+searchQuery+" on "+appName
                responseProtocol(response)
                writeInMemory(text,response)
            webbrowser.open_new_tab(url) 
            continue
        elif "playing" in response.lower() and "on youtube" in response.lower():
            start = text.lower().find("play")
            end = text.lower().find("on youtube")
            video_name = text.lower()[start+4:end].strip()
            try:
                # search for videos matching the video name
                search_response = youtube.search().list(q=video_name, part='id,snippet', maxResults=1).execute()
                video_title=search_response['items'][0]['snippet']['title']
                response="Playing "+str(video_title)+" on youtube"
                # extract the video ID of the first result
                video_id = search_response['items'][0]['id']['videoId']
                url = f'https://www.youtube.com/watch?v={video_id}'
                responseProtocol(response)
                writeInMemory(text,response)
                webbrowser.open(url)
                continue
            except HttpError as e:
                print('An error occurred:', e)
                url = None
            except KeyError:
                video_name += 'site:youtube.com' 
                for j in search(video_name,stop=1):        
                    if 'youtube.com' in j:
                        webbrowser.open(j)
                response="There are plenty of good videos, i think you should choose which one to watch."
                responseProtocol(response)
                writeInMemory(text,response)
                continue
                
        responseProtocol(response)
        with open('Conversation.txt', 'a') as file:
            file.write(("\n"+"Jarvis: "+response+"\n\n"))