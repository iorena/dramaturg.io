from language.word_token import WordToken


class AdjacencyPair:
    def __init__(self, speakers, name):
        self.speakers = speakers
        self.name = name
        self.sentences = {
            "ter": ("ter", "ter"),
            "kys": ("kys", "vas"),
            "ilm": ("ilm", "kui")
        }
        self.word_tokens = {
            "ter": [WordToken("tpart")],
            "kys": [WordToken("interr")],
            "vas": [WordToken("vpart")],
            "ilm": [WordToken("pronom"), WordToken("verb")],
            "kui": [WordToken("kpart")]
        }
        self.first_pair_part = self.get_first_part(name)
        self.second_pair_part = self.get_second_part(name)
        self.skeleton = (self.first_pair_part, self.second_pair_part)

    def __str__(self):
        return f"{self.sentences[self.name][0]} - {self.sentences[self.name][1]}"

    def get_first_part(self, name):
        return self.speakers[0], self.word_tokens[self.sentences[name][0]]

    def get_second_part(self, name):
        return self.speakers[1], self.word_tokens[self.sentences[name][1]]

    def inflect(self):
        #todo: call syntaxmaker
        return self


def main():
    print("Generated adjacency pair")


if __name__ == "__main__":
    main()
