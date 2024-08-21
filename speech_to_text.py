import speech_recognition as sr
from gtts import gTTS

# Initialize the recognizer
r = sr.Recognizer()

# Function to recognize speech and process it
def recognize_speech():
    try:
        with sr.Microphone() as src:
            print('Say something in Arabic...')
            # Listen with a timeout of 5 seconds and a phrase time limit of 10 seconds
            audio = r.listen(src, timeout=5, phrase_time_limit=4)

            # Recognize speech using Google Speech Recognition
            text = r.recognize_google(audio, language='ar-AR')
            print(f"You said: {text}")

            # Save the recognized text to a file
            with open('arabic_text.txt', 'a', encoding='utf-8') as f:
                f.write(text + '\n')


    except sr.UnknownValueError:
        print("Sorry, I could not understand the audio.")
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
    except sr.WaitTimeoutError:
        print("Listening timed out while waiting for phrase to start.")

# Call the function
recognize_speech()
