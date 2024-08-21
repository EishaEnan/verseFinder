import json
import re

# Define the Arabic letters we want to keep
arabic_letters = "ابجدهوزحطيكلمنسعفصقرشتثخذضظغ"
# Include some additional Arabic characters that may appear
additional_arabic_letters = "إآأءةىؤرل"

def clean_text(text):
    # Replace various forms of alif with the simple alif
    text = re.sub(r'[آأإ]', 'ا', text)
    # Replace the specific character ٱ with ا
    text = text.replace('ٱ', 'ا')
    # Create a regex pattern to keep only the specified Arabic letters and spaces
    allowed_chars = arabic_letters + additional_arabic_letters + " "
    pattern = f"[^{allowed_chars}]"  # Match any character not in allowed_chars
    # Replace all disallowed characters with an empty string while preserving spaces
    cleaned_text = re.sub(pattern, '', text)
    return cleaned_text

def process_and_save_json(input_file, output_file):
    # Load the JSON data
    with open(input_file, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    # Process each verse to keep only the specified Arabic letters and spaces
    for surah in data:
        for verse in surah['verses']:
            verse['text'] = clean_text(verse['text'])
    
    # Save the cleaned data to a new JSON file
    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

# Example usage
input_json_file = 'quran.json'
output_json_file = 'cleaned_quran.json'

process_and_save_json(input_json_file, output_json_file)
