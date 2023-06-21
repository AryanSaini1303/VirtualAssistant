#takes query through voice for as long as you speak and gives response through voice as well as text (currently listens for 5 seconds)
#Remembers previous conversations(saves all conversations in a text file which works as a virtual memory)
#have features like stop listening and start listening
#more memory efficient(remembers useful data only)
import pyttsx3
import openai
import speech_recognition as sr
import datetime
import pytz

openai.api_key="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" 
model_engine="text-davinci-003"
engine = pyttsx3.init()
r = sr.Recognizer()
utc_time = datetime.datetime.utcnow()
target_tz = pytz.timezone('Asia/Kolkata')
local_time = utc_time.replace(tzinfo=pytz.utc).astimezone(target_tz)
current_time=local_time.strftime("%I:%M %p")
current_date=datetime.date.today()
with open('Conversation.txt', 'a') as file:
    file.write(('User:current time is '+str(current_time)+" and current date is "+str(current_date)+'\n'+'Jarvis:okay, sir'+'\n\n'))

while True:
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
        with open("Conversation.txt",'r') as f:
                lines=f.readlines()
        with open("Conversation.txt",'w') as f:
            for line in lines:
                if 'User:current time is' not in line and 'Jarvis:okay, sir' not in line:
                    f.write(line)
        f.close()
        break
    elif "stop listening" in text.lower():
        response="Going to sleep mode"
        print("response: ",response)
        engine.say(response)
        engine.runAndWait()
        while True:
            with sr.Microphone() as source:
                # r.pause_threshold=0.8#seconds
                # r.adjust_for_ambient_noise(source)
                print("Waiting...")
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
        print("prompt:",prompt)
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