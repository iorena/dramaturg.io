from libvoikko import Voikko

class TextParser:
    def __init__(self):
        self.nouns_bow = {}
        self.verbs_bow = {}
        self.adjectives_bow = {}
        self.stopwords = self.initialize_stopwords()
        self.voikko = Voikko(u"fi")
        self.omorfi = Omorfi()
        self.cases = self.get_cases()

    def get_cases(self):
        return {
            "nimento": "NOM",
            "omanto": "GEN",
            "kohdanto": "AKK",
            "olento": "ESS",
            "osanto": "PAR",
            "tulento": "TRA",
            "sisaolento": "INE",
            "sisaeronto": "ELA",
            "sisatulento": "ILL",
            "ulko-olento": "ADE",
            "ulko-eronto": "ABL",
            "ulkotulento": "ALL",
            "vajanto": "ABE",
            "keinonto": "INS"
        }

    def initialize_stopwords(self):
        stopword_file = '../data/stopwords.txt'
        stopwords = []
        with open(stopword_file) as f:
            lines = f.readlines()
            for line in lines:
                stopwords.append(line)
            f.close()
        return stopwords

    def parse_bow(self, text):
        sentence_words = []
        for sentence in text.split("."):
            sentence = sentence.lstrip().replace('\n', '')
            words = sentence.split(" ")

            words = list(map(lambda word: word.lower().strip().replace(',', ''), words))
            words = list(map(lambda word: self.voikko.analyze(word.lower()), words))

            #skip sentences that have any words that voikko doesn't recognize
            if len(list(filter(lambda analysis: len(analysis) == 0, words))) > 0:
                continue
            if len(list(filter(lambda analysis: analysis[0]['BASEFORM'] in self.stopwords, words))) > 0:
                continue

            for word in words:
                self.sort_pos(word)


    def get_play_words(self):
        nouns = list(self.nouns_bow.keys())
        verbs = list(self.verbs_bow.keys())
        adjectives = list(self.adjectives_bow.keys())
        return nouns[0:3], verbs[0:3], adjectives[0:3]


    def sort_pos(self, analysis):
        lemmatized = analysis[0]['BASEFORM']
        w_class = analysis[0]['CLASS']
        if 'SIJAMUOTO' in analysis[0]:
            w_case = analysis[0]['SIJAMUOTO']
        else:
            w_case = None

        if lemmatized not in self.stopwords:
            if analysis[0]["CLASS"] == "nimisana":
                if lemmatized in self.nouns_bow:
                    self.nouns_bow[lemmatized] = self.nouns_bow[lemmatized] + 1
                else:
                    self.nouns_bow[lemmatized] = 1
            elif analysis[0]["CLASS"] == "teonsana":
                if lemmatized in self.verbs_bow:
                    self.verbs_bow[lemmatized] = self.verbs_bow[lemmatized] + 1
                else:
                    self.verbs_bow[lemmatized] = 1
            elif analysis[0]["CLASS"] == "laatusana":
                if lemmatized in self.adjectives_bow:
                    self.adjectives_bow[lemmatized] = self.adjectives_bow[lemmatized] + 1
                else:
                    self.adjectives_bow[lemmatized] = 1

