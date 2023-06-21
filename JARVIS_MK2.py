#takes query through voice for 5 seconds and gives response as text
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

