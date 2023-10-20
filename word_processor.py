from german_nouns.lookup import Nouns

class WordProcessor:
    """Handles processing of words"""
    def __init__(self):
        self.nouns_dictionary = Nouns()

    def is_noun(self, word):
        return word[0].isupper() and " " not in word

    def bucket_words(self, cards):
        noun_list = set()
        for card in cards:
            word = card['fields']['German']['value']
            if self.is_noun(word):
                noun_list.add(word)

        found_nouns = {}
        not_found_nouns = set()
        nouns_with_multiple_genders = set()

        for noun in noun_list:
            noun_found = self.nouns_dictionary[noun]
            if noun_found:
                if 'genus' in noun_found[0]:
                    found_nouns[noun] = noun_found[0]['genus']
                else:
                    nouns_with_multiple_genders.add(noun)
                
            else:
                not_found_nouns.add(noun)
        
        return found_nouns, not_found_nouns, nouns_with_multiple_genders

    def get_words_to_upload(self, found_nouns, current_gender_nouns):
        current_gender_nouns_set = set()
        words_to_upload_to_gender = {}
        for noun in current_gender_nouns["result"]:
            current_gender_nouns_set.add(noun["fields"]["Noun"]["value"])
        
        for word in found_nouns:
            if word not in current_gender_nouns_set:
                words_to_upload_to_gender[word] = self.nouns_dictionary[word][0]["genus"].upper()

        return words_to_upload_to_gender