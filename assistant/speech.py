import speech_recognition as sr

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎙️ Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        recognizer.pause_threshold = 1
        recognizer.energy_threshold = 300

        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=8)
            print("🧠 Recognizing...")
            query = recognizer.recognize_google(audio, language='en-in')
            return query.lower()

        except sr.WaitTimeoutError:
            print("⏱️ Timeout: No speech detected.")
            return "none"

        except sr.UnknownValueError:
            print("❌ Couldn’t understand your voice.")
            return "none"

        except sr.RequestError:
            print("🌐 Network error. Please check your internet.")
            return "none"

        except Exception as e:
            print(f"⚠️ Error: {e}")
            return "none"
