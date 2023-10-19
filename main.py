
"""
1. Get words from anki
2. Filter for nouns
3. Get gender
4. Upload to new deck
5. If already in deck, skip
6. If gender not found, prompt user for gender
"""

import json
import urllib.request
from german_nouns.lookup import Nouns
from anki_controller import AnkiController
from word_processor import WordProcessor

nouns_dictionary = Nouns()
anki_controller = AnkiController()
word_processor = WordProcessor()

current_card_ids = anki_controller.invoke("findCards", { "query": '"deck:German::German Class Words"'})
current_cards_info = anki_controller.invoke("cardsInfo", { "cards": current_card_ids['result']})
found_words, not_found_words, words_with_multiple_genders = word_processor.process_words(current_cards_info['result'])

print(found_words)
print(not_found_words)
print(words_with_multiple_genders)
