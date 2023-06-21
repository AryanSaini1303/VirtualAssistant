#takes query through voice for as long as you speak and gives response through voice as well as text (currently listens for 5 seconds)
#have features like stop listening and start listening
#tells accurate time and date
#more memory efficient(remembers useful data only)
#takes input as voice as well as text
import pyttsx3
import openai
import speech_recognition as sr
import datetime
import re

openai.api_key="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" 
model_engine="text-davinci-003"
engine = pyttsx3.init()
r = sr.Recognizer()
time_pattern = re.compile(r'\b(1[012]|[1-9]):([0-5][0-9]) ([AP]M)\b')
date_pattern = r"\d{4}/\d{2}/\d{2}"
choice=input("Enter your mode of input 't' for text and ('v' or press enter) for voice: ")

while True:
    if choice=="t":
        text=input("\n"+"Enter query:")
    else:
        with sr.Microphone() as source:
            # r.pause_threshold=0.8#seconds
            # r.adjust_for_ambient_noise(source)
            print("Say something!")
            # audio = r.listen(source)
            audio=r.record(source,duration=5)
        try:
            text = r.recognize_google(audio)
            print("You said: ", text)
        except sr.UnknownValueError:
            print("Can't understand audio, Try again.")
            continue
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))
            continue
    if "goodbye" in text.lower():
        response="Welcome sir, I hope I was helpful"
        print("response: ",response)
        engine.say(response)
        engine.runAndWait()
        break
    elif "stop listening" in text.lower():
        response="Going to sleep mode"
        print("response: ",response)
        engine.say(response)
        engine.runAndWait()
        while True:
            if choice=="t":
                text=input("Enter query:")
            else:
                with sr.Microphone() as source:
                    # r.pause_threshold=0.8#seconds
                    # r.adjust_for_ambient_noise(source)
                    print("Say something!")
                    # audio = r.listen(source)
                    audio=r.record(source,duration=5)
                try:
                    text = r.recognize_google(audio)
                    print("You said: ", text)
                except sr.UnknownValueError:
                    print("Can't understand audio, Try again.")
                    continue
                except sr.RequestError as e:
                    print("Could not request results from Google Speech Recognition service; {0}".format(e))
                    continue
            if "start listening" in text.lower():
                print("You said: ", text)
                response="Coming back online"
                print("response: ",response)
                engine.say(response)
                engine.runAndWait()
                break
            else:
                continue
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
        print("response: ",response)
        engine.say(response)
        engine.runAndWait()
        if "remember this" in text or "remember that" in text:
            with open('Conversation.txt', 'a') as file:
                file.write(("\n"+"Jarvis: "+response+"\n\n"))
        else:
            with open("Conversation.txt",'r') as f:
                lines=f.readlines()
            with open("Conversation.txt",'w') as f:
                f.writelines(lines[:-1])