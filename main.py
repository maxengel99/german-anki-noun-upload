
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

nouns_dictionary = Nouns()

def is_noun(word):
    return word[0].isupper() and " " not in word

payload = {
    "action": "findCards",
    "version": 6,
    "params": {
        "query": "deck:current"
    }
}

response = json.load(urllib.request.urlopen(
    'http://localhost:8765', json.dumps(payload).encode('utf-8')))

payloadTwo = {
    "action": "cardsInfo",
    "version": 6,
    "params": {
        "cards": response['result']
    }
}

responseTwo = json.load(urllib.request.urlopen(
    'http://localhost:8765', json.dumps(payloadTwo).encode('utf-8')))

noun_list = set()
for card in responseTwo['result']:
    word = card['fields']['German']['value']
    if is_noun(word):
        noun_list.add(word)

found_words = {}
not_found_words = set()
words_with_multiple_genders = set()

for noun in noun_list:
    noun_found = nouns_dictionary[noun]
    if noun_found:
        if 'genus' in noun_found[0]:
            found_words[noun] = noun_found[0]['genus']
        else:
            words_with_multiple_genders.add(noun)
        
    else:
        not_found_words.add(noun)

print(found_words)
print(not_found_words)
print(words_with_multiple_genders)
