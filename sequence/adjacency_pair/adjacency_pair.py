from language.word_token import WordToken

from syntaxmaker.syntax_maker import *


class AdjacencyPair:
    def __init__(self, speakers, name, topic):
        self.speakers = speakers
        self.name = name
        self.verb, self.noun = topic
        self.sentences = {
            "ter": ("ter", "ter"),
            "kys": ("kys", "vas"),
            "ilm": ("ilm", "kui"),
            "hav": ("hav", "kui")
        }
        self.word_tokens = {
            "ter": [WordToken("tpart")],
            "kys": [WordToken("verb"), WordToken("ppron")],
            "vas": [WordToken("vpart")],
            "ilm": [WordToken("ppron", "subj"), WordToken("verb", None, self.verb)],
            "kui": [WordToken("kpart")],
            "hav": [WordToken("pron", "subj"), WordToken("verb"), WordToken("noun", None, self.noun)]
        }
        self.first_pair_part = self.get_first_part(name)
        self.second_pair_part = self.get_second_part(name)
        self.skeleton = (self.first_pair_part, self.second_pair_part)
        self.inflected = (self.inflect(self.first_pair_part), self.inflect(self.second_pair_part))

    def __str__(self):
        return f"{self.sentences[self.name][0]} - {self.sentences[self.name][1]}"

    def get_first_part(self, name):
        return self.speakers[0], self.word_tokens[self.sentences[name][0]]

    def get_second_part(self, name):
        return self.speakers[1], self.word_tokens[self.sentences[name][1]]

    def inflect(self, line):
        """
        TODO: this should be heavily rethought and refactored so it doesn't become a gigantic jungle of if else
        """
        if self.name == "ilm" and len(line[1]) > 1:
            words = line[1]
            verb = words[1]
            vp = create_verb_pharse(verb.word)
            vp.components["subject"] = create_personal_pronoun_phrase()
            as_string = vp.to_string().split()
            words[0].setInflectedForm(as_string[0])
            verb.setInflectedForm(as_string[1])
        if self.name == "kys" and line[1][0].wc == "verb":
            words = line[1]
            vp = create_verb_pharse(line[1][0].word)
            vp.components["subject"] = create_personal_pronoun_phrase("2")
            turn_vp_into_question(vp)
            as_string = vp.to_string().split()
            words[0].setInflectedForm(as_string[0])
            words[1].setInflectedForm(as_string[1])
        if self.name == "hav" and len(line[1]) > 2:
            words = line[1]
            p = create_copula_phrase()
            p.components["subject"] = create_phrase("NP", words[0].word)
            p.components["predicative"] = create_phrase("NP", words[2].word)
            as_string = p.to_string().split()
            words[1].setInflectedForm(as_string[1])
        return line


def main():
    print("Generated adjacency pair")


if __name__ == "__main__":
    main()
