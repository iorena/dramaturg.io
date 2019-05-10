from language.dictionary import dictionary

import random


class WordToken:
    def __init__(self, wc, pos=None, data=None):
        self.data = data
        self.pos = pos
        self.wc = wc
        options = dictionary[wc]
        self.word = random.choices(options)[0]

    def __str__(self):
        return f"{self.word}"

    def setInflectedForm(self, new_form):
        self.word = new_form
