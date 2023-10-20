
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
import easygui
from german_nouns.lookup import Nouns
from anki_controller import AnkiController
from word_processor import WordProcessor

nouns_dictionary = Nouns()
anki_controller = AnkiController()
word_processor = WordProcessor()

current_card_ids = anki_controller.invoke("findCards", { "query": '"deck:German::German Class Words"'})
current_cards_info = anki_controller.invoke("cardsInfo", { "cards": current_card_ids['result']})
found_nouns, not_found_nouns, nouns_with_multiple_genders = word_processor.bucket_words(current_cards_info['result'])

current_gender_noun_card_ids = anki_controller.invoke("findCards", { "query": '"deck:German::German Gender Nouns"'})
current_gender_noun_cards_info = anki_controller.invoke("cardsInfo", { "cards": current_gender_noun_card_ids['result']})
words_to_upload_to_gender = word_processor.get_words_to_upload(found_nouns, current_gender_noun_cards_info)

for word, gender in words_to_upload_to_gender.items():
    fields = { "Noun": word, "Gender": gender }
    deck_name = "German::German Gender Nouns"
    model_name = "German Noun Gender"
    json_args = {
        "deckName": deck_name,
        "modelName": model_name,
        "fields": fields,
        "options": { "allowDuplicate": False },
        "tags": []
    }
    anki_controller.invoke("addNote", { "note": json_args })

button_list = ["Masculine", "Feminine", "Neuter"]
answer_to_field = {
    "Masculine": 'M',
    "Feminine": 'F',
    "Neuter": 'N'
}

for word in not_found_nouns:
    current_gender_nouns_set = set()
    for noun in current_gender_noun_cards_info["result"]:
        current_gender_nouns_set.add(noun["fields"]["Noun"]["value"])

    if word not in current_gender_nouns_set:     
        gender = easygui.buttonbox("The word '" + word + "' was not found. Please pick the gender of the this noun. https://www.collinsdictionary.com/us/dictionary/german-english/", "", button_list)
        print(gender)
        fields = { "Noun": word, "Gender": answer_to_field[gender] }
        deck_name = "German::German Gender Nouns"
        model_name = "German Noun Gender"
        json_args = {
            "deckName": deck_name,
            "modelName": model_name,
            "fields": fields,
            "options": { "allowDuplicate": False },
            "tags": []
        }
        anki_controller.invoke("addNote", { "note": json_args })
