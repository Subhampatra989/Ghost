import webbrowser
import wikipedia
import pyttsx3
import speech_recognition as sr

# Initialize the speech engine
engine = pyttsx3.init()

def speak(text):
    """Speaks the given text aloud."""
    engine.say(text)
    engine.runAndWait()

def listen():
    """Listens to user's voice input and returns recognized text."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
        try:
            query = recognizer.recognize_google(audio)
            return query.lower().strip()
        except sr.UnknownValueError:
            speak("Sorry, I didn't catch that.")
        except sr.RequestError:
            speak("Network error.")
    return ""

def perform_task(query):
    """Performs actions based on the recognized voice command."""
    query = query.lower().strip()

    if 'open youtube' in query:
        speak("Opening YouTube")
        webbrowser.open("https://www.youtube.com")

    elif 'open whatsapp' in query:
        speak("Opening WhatsApp Web")
        webbrowser.open("https://web.whatsapp.com")

    elif 'search' in query:
        speak("What should I search for?")
        search_query = listen()
        if search_query:
            url = f"https://www.google.com/search?q={search_query}"
            speak(f"Searching for {search_query}")
            webbrowser.open(url)

    elif 'who is' in query or 'what is' in query or 'tell me something about' in query or 'explain' in query:
        try:
            topic = query.replace("tell me something about", "").replace("explain", "").strip()
            result = wikipedia.summary(topic, sentences=2)
            speak(f"Sure! {result}")
        except Exception:
            speak("Sorry, I couldn't find information on that.")

    elif 'stop' in query or 'exit' in query:
        speak("Goodbye!")
        exit()

    else:
        speak("I'm still learning. Can you rephrase that?")
