import os
import webbrowser
import time
import pyttsx3
import pyjokes
import pyautogui
import pywhatkit
import requests
import threading
from datetime import datetime
from assistant import speech
from assistant.chatgpt import fallback_to_chatgpt
from word2number import w2n  
import time

engine = pyttsx3.init()

def speak(text):
    print(f"GHOST: {text}")
    engine.say(text)
    engine.runAndWait()

def wish():
    hour = datetime.now().hour
    if 0 <= hour < 12:
        speak("Good morning sir!")
    elif 12 <= hour < 18:
        speak("Good afternoon sir!")
    else:
        speak("Good evening sir!")
    speak("GHOST is activated")

def listen_for_command():
    command = speech.listen()
    if command and command != "none":
        print(f"✅ You said: {command}")
        return command.lower()
    return None

def listen_for_wake_word():
    while True:
        print("🔎 Listening for wake word...")
        command = speech.listen()
        if command and "hello ghost" in command.lower():
            speak("Hi, I'm here.")
            handle_commands()

def handle_commands():
    while True:
        command = listen_for_command()
        if not command:
            speak("")
            continue

        if "stop" in command:
            speak("Okay sir, going back to sleep.")
            return
        if "fuck you" in command:
            speak("Chup saale gandu.")

        elif "open" in command:
            if "youtube" in command:
                webbrowser.open("https://www.youtube.com")
                speak("Opening YouTube for you.")
            elif "camera" in command:
                os.system("start microsoft.windows.camera:") 
                speak("Opening camera for you.")
            else:
                site = command.split("open")[-1].strip().replace(" ", "")
                webbrowser.open(f"https://{site}.com")
                speak(f"Opening {site} for you.")

        elif "play music" in command:
            music_dir = "F:\\Songs\\Imagine_Dragons"
            if os.path.exists(music_dir):
                songs = os.listdir(music_dir)
                if songs:
                    os.startfile(os.path.join(music_dir, songs[0]))
                    speak("Playing music for you.")
                else:
                    speak("No songs found in the music folder.")
            else:
                speak("Music directory not found.")

        elif "tell me a joke" in command:
            speak(pyjokes.get_joke())

        elif "take screenshot" in command:
            filename = "screenshot.png"
            pyautogui.screenshot(filename)
            speak("Screenshot captured.")

        elif "search" in command:
            query = command.replace("search", "").strip()
            if query:
                webbrowser.open(f"https://www.google.com/search?q={query}")
                speak(f"Searching for {query}")
            else:
                speak("What should I search for?")

        elif "time" in command:
            current_time = datetime.now().strftime("%I:%M %p")
            speak(f"The time is {current_time}")

        

        elif "weather" in command:
            speak("Please tell me the city name.")
            city = listen_for_command()
            if city:
                try:
                    api_key = "6302fa7cbf8583a6102b6887e362ccd2"
                    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
                    response = requests.get(url).json()
                    if response["cod"] != "404":
                        temp = response["main"]["temp"]
                        desc = response["weather"][0]["description"]
                        speak(f"The temperature in {city} is {temp}°C with {desc}")
                    else:
                        speak("City not found.")
                except:
                    speak("Failed to get weather data.")

        elif "send whatsapp" in command:
            speak("Whom do you want to message? Say the name as saved in WhatsApp.")
            name = listen_for_command()
            speak("What should I say?")
            message = listen_for_command()

            speak(f"Opening WhatsApp to send your message to {name}.")
            os.system('start shell:AppsFolder\\5319275A.WhatsAppDesktop_cv1g1gvanyjgm!App')

            # Allow WhatsApp to load
            time.sleep(8)

            pyautogui.hotkey("alt", "tab") 
            time.sleep(1)

            pyautogui.hotkey("ctrl", "f")
            time.sleep(1)
            pyautogui.write(name)
            time.sleep(1)
            pyautogui.press("enter")
            time.sleep(2)


            pyautogui.write(message)
            pyautogui.press("enter")

            speak(f"Message sent to {name} on WhatsApp.")

        elif "whatsapp call" in command:
            speak("Whom do you want to call? Say the name as saved in WhatsApp.")
            name = listen_for_command()
            speak("Voice call or video call?")
            call_type = listen_for_command()

            speak(f"Opening WhatsApp to make a {call_type} to {name}.")
            os.system('start shell:AppsFolder\\5319275A.WhatsAppDesktop_cv1g1gvanyjgm!App')


            time.sleep(8)

            pyautogui.hotkey("alt", "tab") 
            time.sleep(1)

            pyautogui.hotkey("ctrl", "f")
            time.sleep(1)
            pyautogui.write(name)
            time.sleep(1)
            pyautogui.press("enter")
            time.sleep(2)

            if "voice" in call_type:
         
                pyautogui.moveTo(1250, 100)  
                pyautogui.click()
                speak(f"Making a voice call to {name}.")
            elif "video" in call_type:
            
                pyautogui.moveTo(1300, 100)  
                pyautogui.click()
                speak(f"Making a video call to {name}.")
            else:
                speak("Invalid call type. Please say 'voice' or 'video'.")

        elif "remind me" in command:
            speak("What should I remind you?")
            reminder = listen_for_command()
            speak("In how many minutes?")
            minutes = listen_for_command()

            try:
                
                mins = w2n.word_to_num(minutes)
                speak(f"Setting a reminder in {mins} minutes.")

                def reminder_alert():
                    import time
                    time.sleep(mins * 60) 
                    speak(f"Reminder: {reminder}")

                threading.Thread(target=reminder_alert).start()

            except ValueError:
                speak("Couldn't understand the number. Please try again with a number like five or ten.")
            except Exception as e:
                speak(f"An error occurred: {e}")

        elif "fun fact" in command:
            try:
                res = requests.get("https://uselessfacts.jsph.pl/random.json?language=en").json()
                speak(res["text"])
            except:
                speak("I couldn't fetch a fun fact right now.")

        elif "lock screen" in command:
            speak("Locking the screen.")
            os.system("rundll32.exe user32.dll,LockWorkStation")

        elif "shutdown" in command:
            speak("Shutting down the system.")
            os.system("shutdown /s /t 1")

        elif "restart" in command:
            speak("Restarting the system.")
            os.system("shutdown /r /t 1")

        elif "sleep" in command:
            speak("Putting system to sleep.")
            os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")

        elif "launch" in command:
            speak("Which app should I open?")
            app_name = listen_for_command()
            paths = {
    "notepad": "notepad.exe",
    "calculator": "calc.exe",
    "vscode": r"C:\Users\subha\AppData\Local\Programs\Microsoft VS Code\Code.exe",
    "chrome": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    "spotify": r"C:\Users\subha\AppData\Roaming\Spotify\Spotify.exe"
}

            if app_name in paths:
                os.startfile(paths[app_name])
                speak(f"Launching {app_name}")
            else:
                speak("I don't know how to open that app yet.")

        else:
            response = fallback_to_chatgpt(command)
            speak(response)

     
        speak("I'm done. Say 'hello ghost' when you need me again.")
        return

if __name__ == "__main__":
    speak("Initializing GHOST")
    wish()
    listen_for_wake_word()
