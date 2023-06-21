#takes query as text input and gives response as text,
#doesn't remember previous conversations
import pyttsx3
import openai
import speech_recognition as sr

openai.api_key="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"
model_engine="text-davinci-003"
engine = pyttsx3.init()
text="hello, jarvis"
r = sr.Recognizer()

while True:
    text=input("Enter query: ")
    if "goodbye jarvis" in text.lower():
        response="Welcome sir, I hope I was helpful"
        print("response: ",response)
        engine.say(response)
        engine.runAndWait()
        break
    else:
        completion = openai.Completion.create(
            engine=model_engine,
            prompt=text,
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.5,
        )
        response = completion.choices[0].text.strip()
        print("response: ",response)
        engine.say(response)

