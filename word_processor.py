from german_nouns.lookup import Nouns

class WordProcessor:
    """Handles processing of words"""
    def __init__(self):
        self.nouns_dictionary = Nouns()

    def is_noun(self, word):
        return word[0].isupper() and " " not in word

    def process_words(self, cards):
        noun_list = set()
        for card in cards:
            word = card['fields']['German']['value']
            if self.is_noun(word):
                noun_list.add(word)

        found_words = {}
        not_found_words = set()
        words_with_multiple_genders = set()

        for noun in noun_list:
            noun_found = self.nouns_dictionary[noun]
            if noun_found:
                if 'genus' in noun_found[0]:
                    found_words[noun] = noun_found[0]['genus']
                else:
                    words_with_multiple_genders.add(noun)
                
            else:
                not_found_words.add(noun)
        
        return found_words, not_found_words, words_with_multiple_genders