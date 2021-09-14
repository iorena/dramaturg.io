from libvoikko import Voikko


class TextParser:
    def __init__(self):
        self.nouns_bow = {}
        self.verbs_bow = {}
        self.adjectives_bow = {}
        self.stopwords = self.initialize_stopwords()
        self.voikko = Voikko(u"fi")

    def initialize_stopwords(self):
        stopword_file = '../data/stopwords.txt'
        stopwords = []
        with open(stopword_file) as f:
            lines = f.readlines()
            for line in lines:
                stopwords.append(line)
            f.close()
        return stopwords

    def parse(self, text):
        for word in text.split(" "):
            cleaned = word.lower().strip().replace(',', '')
            analysis = self.voikko.analyze(word.lower())#$[0]['BASEFORM']
            if len(analysis) == 0:
                continue
            lemmatized = analysis[0]['BASEFORM']
            if lemmatized not in self.stopwords:
                if analysis[0]['CLASS'] == "nimisana":
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

        sorted_nouns = sorted(self.nouns_bow.items(), reverse = True)
        sorted_verbs = sorted(self.verbs_bow.items(), reverse = True)
        sorted_adjs = sorted(self.adjectives_bow.items(), reverse = True)
        nouns = []
        verbs = []
        adjectives = []
        for i in range(3):
            word = sorted_nouns[i][0]
            nouns.append(word)
        for i in range(3):
            word = sorted_verbs[i][0]
            verbs.append(word)
        for i in range(3):
            word = sorted_adjs[i][0]
            adjectives.append(word)
        while len(verbs) < 3:
            verbs.append("olla")

        return nouns, verbs, adjectives



