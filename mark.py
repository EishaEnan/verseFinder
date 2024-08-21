import unittest
import json
from fuzzysearch import load_quran, search_verse  # Update with the correct import

class TestVerseSearch(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.quran_data = load_quran('processed_data.json')
        with open('test_data.json', 'r', encoding='utf-8') as file:
            cls.test_data = json.load(file)['tests']

    def test_search_verses(self):
        for test in self.test_data:
            with self.subTest(test=test):
                search_text = test['search_text']
                expected_verse_number = test['expected_verse_number']
                
                result, _ = search_verse(self.quran_data, search_text)
                verse_number, surah_name = self.extract_verse_info(result)
                
                if verse_number != expected_verse_number:
                    print(f"Search text: {search_text}")
                    print(f"Expected verse number: {expected_verse_number}")
                    print(f"Found verse number: {verse_number}")
                    print(f"Surah name: {surah_name}")
                    print("------------------------")
                
                self.assertEqual(verse_number, expected_verse_number)

    def extract_verse_info(self, result):
        # Extract the verse number and surah name from the result string
        verse_number = None
        surah_name = None
        
        if "Verse" in result:
            start_index = result.index("Verse") + len("Verse ")
            end_index = result.index(":", start_index)
            verse_number = int(result[start_index:end_index].strip())
        
        if "Surah" in result:
            start_index = result.index("Surah") + len("Surah: ")
            end_index = result.index(" (Transliteration", start_index)
            surah_name = result[start_index:end_index].strip()
        
        return verse_number, surah_name

if __name__ == '__main__':
    unittest.main()
