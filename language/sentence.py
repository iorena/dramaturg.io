from syntaxmaker.syntax_maker import (create_verb_pharse, create_personal_pronoun_phrase, turn_vp_into_question,
                                      create_copula_phrase, create_phrase, auxiliary_verbs, add_auxiliary_verb_to_vp,
                                      add_advlp_to_vp, set_vp_mood_and_tense, turn_vp_into_prefect)
from language.dictionary import word_dictionary

import random


class Sentence:
    def __init__(self, speaker, listeners, pos, question, obj_type, tense):
        self.speaker = speaker
        self.listeners = listeners
        self.subj = pos["subj"]
        self.verb = pos["verb"]
        self.obj = pos["obj"]
        self.obj_type = obj_type
        self.tense = tense
        self.inflected = self.get_inflected_sentence(question)
        self.styled = self.get_styled_sentence()

    def get_inflected_sentence(self, question):
        if self.verb is None:
            return None
        if self.verb.word is "olla":
            vp = create_copula_phrase()
        else:
            vp = create_verb_pharse(self.verb.word)

        mood = "INDV"
        tense = "PRESENT"

        #check person
        if self.speaker.name is self.subj.word:
            person = "1"
            vp.components["subject"] = create_personal_pronoun_phrase()
        elif self.subj.word in [listener.name for listener in self.listeners]:
            person = "2"
            vp.components["subject"] = create_personal_pronoun_phrase("2")
        else:
            person = "3"
            vp.components["subject"] = create_phrase("NP", self.subj.word)

        #check "object"
        if self.obj is not None:
            if self.verb.word is "olla" and self.obj_type is "location":
                advlp = create_phrase("NP", self.obj.word, {"CASE": "INE"})
                add_advlp_to_vp(vp, advlp)
            elif self.verb.word is "olla" and self.obj_type is "affect":
                predv = create_phrase("NP", self.obj.word)
                add_advlp_to_vp(vp, predv)
            #todo: fork syntaxmaker to allow copula sentence of type "x has y"
            elif self.verb.word is "olla" and self.obj_type is "owner":
                pred = create_phrase("NP", "omistaja")
                predv = create_phrase("NP", self.obj.word, {"CASE": "GEN"})
                add_advlp_to_vp(vp, predv)
                add_advlp_to_vp(vp, pred)
            #correct case for locations can be gotten with word2vec
            elif self.verb.word in word_dictionary["siirtyä"]:
                advlp = create_phrase("NP", self.obj.word, {"CASE": "ILL"})
                add_advlp_to_vp(vp, advlp)
            elif self.verb.word in word_dictionary["hankkia"]:
                obj = create_phrase("NP", self.obj.word)
                vp.components["dir_object"] = obj

        #check tempus
        if self.tense is "past":
            tense = "PAST"
        elif self.tense is "postpast":
            tense = "PAST"
            turn_vp_into_prefect(vp)

        #check character relations
        #todo: how does character relation _actually_ affect speech?
        if self.speaker.relations[self.listeners[0].name] > 0.7:
            mood = "COND"

        set_vp_mood_and_tense(vp, mood, tense)

        if self.tense is "future":
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
