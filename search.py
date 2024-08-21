# Finds exact verse match without any processing of data
import json

def load_quran(json_file):
    with open(json_file, 'r', encoding='utf-8') as file:
        quran_data = json.load(file)
    return quran_data

def search_verse(quran_data, search_text):
    for surah in quran_data:
        for verse in surah['verses']:
            if search_text.strip() == verse['text'].strip():
                return f"Surah: {surah['name']} (Transliteration: {surah['transliteration']}), Verse {verse['id']}: {verse['text']}"
    return "Verse not found."

# Load the Qur'an data
quran_data = load_quran('quran.json')

# Example search
search_text = "لَا يُكَلِّفُ ٱللَّهُ نَفۡسًا إِلَّا وُسۡعَهَاۚ لَهَا مَا"  
# Replace with your search text
result = search_verse(quran_data, search_text)

print(result)
