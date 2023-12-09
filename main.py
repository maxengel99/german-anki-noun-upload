
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
from anki_controller import AnkiController

anki_controller = AnkiController()

current_card_ids = anki_controller.invoke("findCards", { "query": '"deck:German::German Class Words" tag:noun'})
current_cards_info = anki_controller.invoke("cardsInfo", { "cards": current_card_ids['result']})
def get_full_word(word, gender):
    if gender == 'M':
        return "der " + word
    elif gender == 'F':
        return "die " + word
    else:
        return "das " + word

visited = set()
for card_info in current_cards_info["result"]:
    word = card_info["fields"]["German"]["value"]
    if word in visited:
        continue

    print("inserting the word - ")
    print(word)

    gender = card_info["fields"]["Gender"]["value"]
    
    fields = { "Noun": word, "Gender": gender, "Full Word": get_full_word(word, gender) }
    deck_name = "German::German Gender Nouns"
    model_name = "German Noun Gender"
    json_args = {
        "deckName": deck_name,
        "modelName": model_name,
        "fields": fields,
        "options": { "allowDuplicate": False },
        "tags": []
    }
    visited.add(word)
    anki_controller.invoke("addNote", { "note": json_args })
