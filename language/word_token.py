from language.dictionary import pos_dictionary, word_dictionary

import random


class WordToken:
    def __init__(self, wc, pos=None, data=None):
        self.data = data
        self.pos = pos
        self.wc = wc
        options = pos_dictionary[wc]
        self.word = random.choices(options)[0]
        if data is not None:
            if data in word_dictionary:
                options = word_dictionary[data]
                self.word = random.choices(options)[0]
            else:
                self.word = str(data)

    def __str__(self):
        return f"{self.word}"
