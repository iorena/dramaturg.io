from syntaxmaker.syntax_maker import (create_verb_pharse, create_personal_pronoun_phrase, turn_vp_into_question,
                                      create_copula_phrase, create_phrase, auxiliary_verbs, add_auxiliary_verb_to_vp,
                                      add_advlp_to_vp, set_vp_mood_and_tense, turn_vp_into_prefect)
from language.dictionary import word_dictionary

import random


class Sentence:
    def __init__(self, speaker, listeners, pos, question, aux, obj_type, tense):
        self.speaker = speaker
        self.listeners = listeners
        self.subj = pos["subj"]
        self.verb = pos["verb"]
        self.obj = pos["obj"]
        self.obj_type = obj_type
        self.tense = tense
        self.inflected = self.get_inflected_sentence(question, aux)
        self.styled = self.get_styled_sentence()

    def get_inflected_sentence(self, question, aux):
        if self.verb is None:
            return None
        if self.verb.word is "olla":
            vp = create_copula_phrase()
        else:
            vp = create_verb_pharse(self.verb.word)

        #check person
        if self.speaker.name is self.subj.word:
            vp.components["subject"] = create_personal_pronoun_phrase()
        elif self.subj.word in [listener.name for listener in self.listeners]:
            vp.components["subject"] = create_personal_pronoun_phrase("2")
        else:
            vp.components["subject"] = create_phrase("NP", self.subj.word)

        #check "object"
        if self.obj is not None:
            if self.verb.word is "olla" and self.obj_type is "location":
                advlp = create_phrase("NP", self.obj.word, {"CASE": "INE"})
                add_advlp_to_vp(vp, advlp)
            elif self.verb.word is "olla":
                print(self.obj_type)
            #correct case for locations can be gotten with word2vec
            elif self.verb.word in word_dictionary["siirtyä"]:
                advlp = create_phrase("NP", self.obj.word, {"CASE": "ILL"})
                add_advlp_to_vp(vp, advlp)

        #check tempus
        if self.tense is "past":
            set_vp_mood_and_tense(vp, "INDV", "PAST")
        elif self.tense is "postpast":
            turn_vp_into_prefect(vp)
            set_vp_mood_and_tense(vp, "INDV", "PAST")

        if aux:
            aux = random.choices(list(auxiliary_verbs.keys()))[0]
            add_auxiliary_verb_to_vp(vp, aux)
        if question:
            turn_vp_into_question(vp)
        as_string = vp.to_string().split()
        return as_string

    def get_styled_sentence(self):
        if self.inflected is None:
            return None
        return self.speaker.style.get_styled_expression(self.inflected)
