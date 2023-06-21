#takes query through voice for as long as you speak and gives response through voice as well as text, 
#Remembers previous conversations(saves all conversations in a text file which works as a virtual memory)
#have features like stop listening and start listening
import pyttsx3
import openai
import speech_recognition as sr
from datetime import datetime

openai.api_key="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" 
model_engine="text-davinci-003"
engine = pyttsx3.init()
r = sr.Recognizer()
i=1
current_time=datetime.now()
with open('Conversation.txt', 'a') as file:
    file.write(('User:the current date and time is '+str(current_time)+"\n"+'JARVIS:okay sir'+'\n\n'))

while True:
    with sr.Microphone() as source:
        r.pause_threshold=0.8#seconds
        r.adjust_for_ambient_noise(source)
        print("Say something!")
        audio = r.listen(source)
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
        with open('Conversation.txt', 'a') as file:
            file.write(('User: '+text+"\n"+'JARVIS: '+response+'\n\n'))
        break
    elif "stop listening" in text.lower():
        response="Going to sleep mode"
        print("response: ",response)
        engine.say(response)
        engine.runAndWait()
        with open('Conversation.txt', 'a') as file:
            file.write(('User: '+text+"\n"+'JARVIS: '+response+'\n\n'))
        while True:
            with sr.Microphone() as source:
                r.adjust_for_ambient_noise(source)
                print("Waiting...")
                audio = r.listen(source)
            try:
                text = r.recognize_google(audio)
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
                with open('Conversation.txt', 'a') as file:
                    file.write(('User: '+text+"\n"+'JARVIS: '+response+'\n\n'))
                break
            else:
                continue
    else:
        with open('Conversation.txt', 'a') as file:
            file.write(('User:'+text+"\n"))
        with open('Conversation.txt', 'r') as file:
            prompt= file.read()
        print("prompt:",prompt)
        completion = openai.Completion.create(
            engine=model_engine,
            prompt=prompt,
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.5,
        )
        response1 = completion.choices[0].text.strip()
        words=response1.split()
        if "Jarvis:" in words:
            words.remove("Jarvis:")
        response=" ".join(words)
        print("response: ",response)
        engine.say(response)
        engine.runAndWait()
        with open('Conversation.txt', 'a') as file:
            file.write(("Jarvis: "+response+"\n\n"))
