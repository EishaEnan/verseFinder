# Combination of all the modules

import json
import time
from fuzzywuzzy import process
import speech_recognition as sr
from gtts import gTTS

# Initialize the recognizer
r = sr.Recognizer()

def load_quran(json_file):
    with open(json_file, 'r', encoding='utf-8') as file:
        quran_data = json.load(file)
    return quran_data

def search_verse(quran_data, search_text, fuzzy_threshold=80):
    # Flatten the verses into a list for easy searching
    verse_list = []
    for surah in quran_data:
        for verse in surah['verses']:
            verse_list.append({
                'surah_name': surah['name'],
                'transliteration': surah['transliteration'],
                'verse_number': verse['id'],
                'text': verse['text']
            })

    # Start timing
    start_time = time.time()

    # Try exact match first
    for verse in verse_list:
        if search_text in verse['text']:
            # End timing
            end_time = time.time()
            search_duration = end_time - start_time  # Calculate duration
            
            return (f"Surah: {verse['surah_name']} (Transliteration: {verse['transliteration']}), "
                    f"Verse {verse['verse_number']}: {verse['text']}", search_duration)

    # If no exact match found, perform fuzzy matching
    texts = [verse['text'] for verse in verse_list]
    best_match = process.extractOne(search_text, texts, score_cutoff=fuzzy_threshold)

    if best_match:
        matched_verse = next(verse for verse in verse_list if verse['text'] == best_match[0])
        # End timing
        end_time = time.time()
        search_duration = end_time - start_time  # Calculate duration
        
        return (f"Surah: {matched_verse['surah_name']} (Transliteration: {matched_verse['transliteration']}), "
                f"Verse {matched_verse['verse_number']}: {matched_verse['text']}", search_duration)
    else:
        # End timing
        end_time = time.time()
        search_duration = end_time - start_time  # Calculate duration
        
        return "Verse not found.", search_duration

def recognize_speech():
    try:
        with sr.Microphone() as src:
            print('Say something in Arabic...')
            # Listen with a timeout of 5 seconds and a phrase time limit of 10 seconds
            audio = r.listen(src, timeout=5, phrase_time_limit=4)

            # Recognize speech using Google Speech Recognition
            text = r.recognize_google(audio, language='ar-AR')
            print(f"You said: {text}")

            return text

    except sr.UnknownValueError:
        print("Sorry, I could not understand the audio.")
        return None
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        return None
    except sr.WaitTimeoutError:
        print("Listening timed out while waiting for phrase to start.")
        return None

def main():
    # Load the Qur'an data
    quran_data = load_quran('cleaned_quran.json')

    # Recognize speech and get the text
    search_text = recognize_speech()
    
    if search_text:
        # Perform the search
        result, duration = search_verse(quran_data, search_text)
        
        # Print the results
        print(result)
        print(f"Search completed in {duration:.4f} seconds")
    else:
        print("No valid text to search.")

if __name__ == "__main__":
    main()
