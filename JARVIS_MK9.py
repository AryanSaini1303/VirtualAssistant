#takes query through voice for as long as you speak and gives response through voice as well as text(listens for 5 seconds as of now)
#have features like stop listening and start listening
#tells accurate time and date
#takes input as voice as well as text
#searches on google,flipkart,amazon,ajio,myntra,nykaa,youtube (default search engine is google)
#plays videos on youtube
#play,pause,mute,unmute,set volume to a specified level and also increase/decrease volume by a specified factor viz.10
#plays next/previous track for spotify only
#scroll up/down, close window
#remembers conversation until it's closed so that i can take references from past conversation to answer and once the program is closed, it erases all the conversation except the one which is important(the one which is instructed to remember)
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

#function to give a response
def responseProtocol(response):
    if response!="":  
        print(response)
        engine.say(response)
        engine.runAndWait()

#function to save all conversation
def writeInMemory(text,response):
    with open('Conversation.txt', 'a') as file:
        file.write(('User:'+text))
    with open('Conversation.txt', 'a') as file:
        file.write(("\n"+"Jarvis: "+response+"\n\n"))

openai.api_key="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" 
model_engine="text-davinci-003"
engine = pyttsx3.init()#used to convert text to speech
r = sr.Recognizer()#used to recognize voice and conver it to text
time_pattern = re.compile(r'\b(1[012]|[1-9]):([0-5][0-9]) ([AP]M)\b')#pattern to detect time in a string
date_pattern = r"\d{4}/\d{2}/\d{2}"#pattern to detect date in a string
youtube = build('youtube', 'v3', developerKey="AIzaSyCqf5WsmtFlfL7PZhHH59diqC3KQ39Alvo")#used in playing videos on youtube
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
choice=input("Enter your mode of input 't' for text and ('v' or press enter) for voice: ")

while True:
    if choice=="t":
        text=input("\n"+"Enter query:")
    else:
        with sr.Microphone() as source:
            playsound('./mixkit-click-error-1110.wav')
            print("\n"+"Say something!")
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
    if "goodbye jarvis" in text.lower() or "good bye jarvis" in text.lower():
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
    elif "stop listening" in text.lower():
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
            if "start listening" in text.lower():
                print("You said: ", text)
                response="Coming back online"
                responseProtocol(response)
                writeInMemory(text,response)
                break
            else:
                continue
    elif text.lower().startswith("open") or text.lower().startswith("jarvis open") or text.lower().startswith("jarvis can you please open") or text.lower().startswith("jarvis please open"):
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
    elif text.lower().startswith("search for"):
        url=""#to clear the variable everytime this iteration triggers
        appName=""#to clear the variable everytime this iteration triggers
        searchQuery=""#to clear the variable everytime this iteration triggers
        words=""#to clear the variable everytime this iteration triggers
        words=text.lower().split()
        appName=words[-1]
        if appName=="video":
            text=text.lower().replace("prime video","primevideo")
            newwords=text.split()
            appName=newwords[-1]
        words=words[2:]
        if appName.lower()!="google" and appName.lower()!="flipkart" and appName.lower()!="youtube" and appName.lower()!="amazon" and appName.lower()!="myntra" and appName.lower()!="ajio" and appName.lower()!="nykaa"and appName.lower()!="primevideo":
            appName="google"
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
    elif text.lower().startswith("play") and text.lower().endswith("youtube"):
        words=text.split()
        words=words[1:]
        words=words[:-2]
        video_name=" ".join(words)
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
    elif text.lower()=="play" or text.lower()=="pause":
        pyautogui.press("playpause")
    elif "set volume" in text.lower() or "set the volume" in text.lower() or text.lower()=="mute" or text.lower()=="unmute":
        words=text.split()
        if words[-1].lower()=="percent" or words[-1].lower()=="percentage" or words[-1].lower()=="%":
            words=words[:-1]
        if words[-1][-1].lower()=="%":
            words[-1]=words[-1][:-1]
        if text.lower()!="mute" and text.lower()!="unmute":
            newLevel=int(words[-1])
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(
            IAudioEndpointVolume._iid_, 
            comtypes.CLSCTX_ALL, 
            None
        )
        volume = interface.QueryInterface(IAudioEndpointVolume)
        if text.lower()=="mute":
            volume.SetMute(1, None)
        elif text.lower()=="unmute":
            volume.SetMute(0,None)
        else:
            scalar = volume.GetMasterVolumeLevelScalar()
            level=int(scalar*100)                        
            if  level-newLevel>0:
                factor=int((level-newLevel)/2)                
                pyautogui.press('volumedown', presses=factor)
            else:
                factor=int((-1)*((level-newLevel)/2))                
                pyautogui.press('volumeup', presses=factor)
    elif "play next track" in text.lower() or "play the next track" in text.lower() or "play previous track" in text.lower() or "play the previous track" in text.lower():#works only for spotify
        if "next" in text.lower():
            sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id="79598783a6e84d75bc48e52cf5548511",
            client_secret="7101c8145ac34784b30ea8d08b4177b5",
            redirect_uri="http://localhost:8080",
            scope="user-read-playback-state,user-modify-playback-state"))
            sp.next_track()
        elif "previous" in text.lower():
            sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id="79598783a6e84d75bc48e52cf5548511",
            client_secret="7101c8145ac34784b30ea8d08b4177b5",
            redirect_uri="http://localhost:8080",
            scope="user-read-playback-state,user-modify-playback-state"))
            sp.previous_track()
    elif "scroll up" in text.lower() or "scroll down" in text.lower():
            i=800
            sensi=i
            if "down" in text.lower():
                sensi=-i
            pyautogui.scroll(sensi)
    elif "close window" in text.lower() or "close this window" in text.lower() or "close the current window" in text.lower() or "close the window" in text.lower():
        window = win32gui.GetForegroundWindow()
        win32gui.PostMessage(window, win32con.WM_CLOSE, 0, 0)
    elif "change window" in text.lower() or "switch window" in text.lower() or "change the window" in text.lower() or "switch the window" in text.lower():
        pyautogui.hotkey('alt', 'tab')
    elif "change tab" in text.lower() or "switch tab" in text.lower() or "change the tab" in text.lower() or "switch the tab" in text.lower():
        pyautogui.hotkey('ctrl', 'tab')
    elif "show me all the tabs" in text.lower() or "show all the tabs" in text.lower() or "show all tabs" in text.lower() or "show me all the windows" in text.lower() or "show all the windows" in text.lower() or "show all windows" in text.lower():
        pyautogui.hotkey("win","tab")
    elif "lock my desktop" in text.lower() or "lock desktop" in text.lower():
        os.system("rundll32.exe user32.dll, LockWorkStation")
    elif "youtube fullscreen" in text.lower() or "youtube on fullscreen" in text.lower() or "youtube full screen" in text.lower() or "youtube on full screen" in text.lower():
        pyautogui.hotkey('f')
    elif "exit youtube fullscreen" in text.lower() or "close youtube fullscreen" in text.lower():
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
        matchTime=time_pattern.search(response)
        matchDate=re.search(date_pattern,response)
        if matchTime:
            current_time=datetime.datetime.now().strftime("%I:%M %p")
            response="It's "+current_time
        elif matchDate:
            current_date=datetime.date.today()
            response="Today is "+str(current_date)
        elif "volume decreased by " in response.lower() or "volume increased by " in response.lower() or "increasing volume by " in response.lower() or "decreasing volume by " in response.lower() or "volume has been decreased by " in response.lower() or "volume has been increased by " in response.lower():
            words=text.split()
            if words[-1]=="percent" or words[-1]=="percentage":
                words=words[:-1]
            factor=int(words[-1])
            for i in range(int(factor/2)):
                if "decreased" in response:
                    keyboard.press_and_release('volume down')
                    response=""
                elif "increased" in response:
                    keyboard.press_and_release('volume up')
                    response=""
        responseProtocol(response)
        with open('Conversation.txt', 'a') as file:
            file.write(("\n"+"Jarvis: "+response+"\n\n"))
