from syntaxmaker.syntax_maker import (create_verb_pharse, create_personal_pronoun_phrase, turn_vp_into_question,
                                      create_copula_phrase, create_phrase, auxiliary_verbs, add_auxiliary_verb_to_vp,
                                      add_advlp_to_vp, set_vp_mood_and_tense, turn_vp_into_prefect)
from language.dictionary import word_dictionary

import random


class Sentence:
    def __init__(self, speaker, listeners, pos, action_type, obj_type):
        self.speaker = speaker
        self.listeners = listeners
        if action_type.subj == "project":
            self.subj = pos["subj"]
        elif action_type.subj == "Listener":
            self.subj = listeners[0].name
        elif action_type.subj == "Speaker":
            self.subj = speaker
        else:
            self.subj = action_type.subj
        if action_type.verb == "project":
            self.verb = pos["verb"]
        else:
            self.verb = action_type.verb
        self.obj = pos["obj"]
        self.obj_type = obj_type
        self.action_type = action_type
        self.inflected = self.get_inflected_sentence()
        self.styled = self.get_styled_sentence()

    def get_inflected_sentence(self):
        if self.verb is None:
            return None
        if self.verb is "olla":
            vp = create_copula_phrase()
        else:
            vp = create_verb_pharse(self.get_synonym(self.verb))

        mood = self.action_type.modus
        tense = "PRESENT"

        #check person
        if self.speaker.name == self.subj:
            person = "1"
            vp.components["subject"] = create_personal_pronoun_phrase()
        elif self.subj in [listener.name for listener in self.listeners]:
            person = "2"
            vp.components["subject"] = create_personal_pronoun_phrase("2")
        else:
            person = "3"
            vp.components["subject"] = create_phrase("NP", self.get_synonym(self.subj))

        #check "object"
        if self.obj is not None:
            obj = self.get_synonym(self.obj)
            if self.verb is "olla" and self.obj_type is "location":
                advlp = create_phrase("NP",obj, {"CASE": "INE"})
                add_advlp_to_vp(vp, advlp)
            elif self.verb is "olla" and self.obj_type is "affect":
                predv = create_phrase("NP", obj)
                add_advlp_to_vp(vp, predv)
            #todo: fork syntaxmaker to allow copula sentence of type "x has y"
            elif self.verb is "olla" and self.obj_type is "owner":
                pred = create_phrase("NP", "omistaja")
                predv = create_phrase("NP", obj, {"CASE": "GEN"})
                add_advlp_to_vp(vp, predv)
                add_advlp_to_vp(vp, pred)
            #correct case for locations can be gotten with2vec
            elif self.verb == "siirtyä":
                advlp = create_phrase("NP", obj, {"CASE": "ILL"})
                add_advlp_to_vp(vp, advlp)
            #for some reason syntaxmaker doesn't accept objects for thes "hommata" and "saada", so must workaround
            #this also causes problems when using imperative forms because object case isn't altered accordingly
            elif self.verb in word_dictionary["hankkia"]:
                case = "GEN"
                if mood == "IMPV":
                    case = "NOM"
                obj = create_phrase("NP", obj, {"CASE": case})
                add_advlp_to_vp(vp, obj)

        #check tempus
        if self.action_type.tempus is "imperf":
            tense = "PAST"
        elif self.action_type.tempus is "postpast":
            tense = "PAST"
            turn_vp_into_prefect(vp)

        set_vp_mood_and_tense(vp, mood, tense)

        if self.action_type.aux_verb is not None:
            averb = random.choices(self.action_type.aux_verb)[0]
            add_auxiliary_verb_to_vp(vp, averb)
        if self.action_type.ques:
            turn_vp_into_question(vp)
        as_string = vp.to_string().split()
        #workaround because syntaxmaker doesn't support sentences with no subject
        if mood == "IMPV":
            as_string.remove("sinä")
        return as_string

    def get_synonym(self, word):
        if word not in word_dictionary:
            return word
        options = word_dictionary[word]
        return random.choices(options)[0]

    def get_styled_sentence(self):
        if self.inflected is None:
            return None
        return self.speaker.style.get_styled_expression(self.inflected)
