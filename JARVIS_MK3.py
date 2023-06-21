#takes query through voice for 5 seconds and gives response through voice as well as text, 
#Remembers previous conversations(saves all conversations in a text file which works as a virtual memory)
import pyttsx3
import openai
import speech_recognition as sr

openai.api_key="sak-HWE4IOemjbXD7Aogz9bKT3BlbkFJ3j7fOGUWZFrXrEZge2n0"
model_engine="text-davinci-003"
engine = pyttsx3.init()
r = sr.Recognizer()
i=1

while True:
    with sr.Microphone() as source:
        print("Say something!")
        audio = r.record(source, duration=5)
    try:
        text = r.recognize_google(audio)
        print("You said: ", text)
    except sr.UnknownValueError:
        print("Can't understand audio, Try again.")
        continue
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
        continue
    if "goodbye jarvis" in text.lower():
        response="Welcome sir, I hope I was helpful"
        print("response: ",response)
        engine.say(response)
        engine.runAndWait()
        with open('Conversation.txt', 'a') as file:
            file.write(('User: '+text+"\n"+'JARVIS: '+response+'\n\n'))
        break
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
