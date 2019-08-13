from syntaxmaker.syntax_maker import (create_verb_pharse, create_personal_pronoun_phrase, turn_vp_into_question,
                                      create_copula_phrase, create_phrase, auxiliary_verbs, add_auxiliary_verb_to_vp,
                                      add_advlp_to_vp, set_vp_mood_and_tense, turn_vp_into_prefect,
                                      negate_verb_pharse, turn_vp_into_passive)
from syntaxmaker.inflector import inflect
from language.dictionary import verb_dictionary, noun_dictionary, reversed_verb_dictionary, evaluations_dictionary
from concepts.character import Character

import random


class Sentence:
    def __init__(self, speaker, listeners, project, action_type, obj_type, reverse):
        self.speaker = speaker
        self.listeners = listeners
        self.attribute = False
        self.project = project
        #subject
        if action_type.subj == "subject":
            self.subj = project.subj.name
        elif action_type.subj == "object":
            self.subj = project.obj.name
        elif action_type.subj == "Listener":
            self.subj = listeners[0].name
        elif action_type.subj == "Speaker":
            self.subj = speaker.name
        elif action_type.subj == "parent":
            self.subj = project.parent.subj
        else:
            self.subj = action_type.subj

        #verb
        if action_type.verb == "project":
            self.verb = project.verb
        else:
            self.verb = action_type.verb
        self.verb_realization = None

        #"object"
        if project.obj is None:
            self.obj = None
        elif action_type.obj == "object":
            self.obj = project.obj.name
        elif action_type.obj == "attribute":
            self.obj = project.obj.name
            self.attribute = True
        else:
            self.obj = action_type.obj

        #you can't command yourself, so instead you command the other person to do the action for you
        self.reversed = reverse
        if self.reversed and self.subj == speaker.name:
            self.subj = self.listeners[0].name
        elif self.reversed and self.subj == self.listeners[0].name:
            self.subj = speaker.name

        self.obj_type = obj_type
        self.action_type = action_type
        self.inflected = self.get_inflected_sentence()
        self.styled = self.get_styled_sentence()

    def get_inflected_sentence(self):
        #if there is no verb, skip creating a verb "pharse" with syntaxmaker and just pile words in a list
        if self.verb is None:
            if self.subj is None:
                as_list = []
            else:
                as_list = [self.get_synonym(self.subj)]
                #todo: figure out rule that governs when attributes are added and when not
            if self.attribute:
                attribute = ""
                if self.obj_type == "owner":
                    attribute = inflect(self.obj, "N", {"PERS": "3", "CASE": "GEN", "NUM": "SG"})
                elif self.obj_type == "location":
                    attribute = inflect(self.obj, "N", {"PERS": "3", "CASE": "INE", "NUM": "SG"}) + " oleva"
                as_list.insert(0, attribute)
            elif self.obj is not None:
                as_list.insert(0, self.get_synonym(self.obj))

            if self.action_type.pre_add is not None:
                as_list.insert(0, self.get_synonym(self.action_type.pre_add))

            if self.action_type.ques:
                as_list.append("?")

            return as_list

        if self.verb is "olla":
            vp = create_copula_phrase()
        else:
            self.verb_realization = self.get_synonym(self.verb)
            vp = create_verb_pharse(self.verb_realization[0])

        mood = self.action_type.modus
        tense = "PRESENT"

        #check person
        if self.speaker.name == self.subj:
            person = "1"
            vp.components["subject"] = create_personal_pronoun_phrase()
        elif self.subj in [listener.name for listener in self.listeners]:
            person = "2"
            prodrop = mood == "IMPV"
            vp.components["subject"] = create_personal_pronoun_phrase("2", "SG", prodrop)
        else:
            person = "3"
            vp.components["subject"] = create_phrase("NP", self.get_synonym(self.subj))

        obj_case = "NOM"
        #check "object"
        obj = self.get_synonym(self.obj)
        if self.project.verb is "olla" and self.obj_type is "location":
            obj_case = "INE"
        #todo: fork syntaxmaker to allow copula sentence of type "x has y"?
        elif self.project.verb is "olla" and self.obj_type is "owner":
            obj_case = "GEN"
        #for some reason syntaxmaker doesn't accept objects for thes "hommata" and "saada", so must workaround
        #this also causes problems when using imperative forms because object case isn't altered accordingly
        elif self.verb in list(map(lambda x: x[0], verb_dictionary["hankkia"])):
            obj_case = "GEN"
            if mood == "IMPV":
                obj_case = "NOM"
        elif self.verb_realization:
            obj_case = self.verb_realization[1]
        if self.obj is not None and self.obj != "interrogative":
            obj = create_phrase("NP", obj, {"CASE": obj_case})
            add_advlp_to_vp(vp, obj)
            if self.verb is "olla" and self.obj_type is "owner" and type(self.project.subj) is Character:
                pred = create_phrase("NP", "omistaja")
                add_advlp_to_vp(vp, pred)

        #check tempus
        if self.project.time is "past":
            tense = "PAST"
        elif self.project.time is "postpast":
            tense = "PAST"
            turn_vp_into_prefect(vp)

        set_vp_mood_and_tense(vp, mood, tense)

        if self.action_type.passive:
            turn_vp_into_passive(vp)

        if self.action_type.neg:
            negate_verb_pharse(vp)

        if self.action_type.aux_verb is not None:
            averb = random.choices(self.action_type.aux_verb)[0]
            add_auxiliary_verb_to_vp(vp, averb)
        if self.action_type.ques:
            turn_vp_into_question(vp)
        if self.verb is not None:
            as_list = vp.to_string().split()

        #add "minulle" in reversed commands
        if self.reversed:
            if person is "1":
                pers = "sinu"
            elif person is "2":
                pers = "minu"
            case = "lle"
            if self.verb == "siirtyä":
                case = "t"
            as_list.insert(len(as_list) - 1, pers + case)

        if self.action_type.name == "TIPB":
            if self.obj_type == "owner" and self.verb == "olla" and type(self.project.subj) is Character:
                as_list.insert(0, "omistaja")
        #add appropriate interrogative
        if self.obj == "interrogative":
            as_list.insert(0, self.get_interrogative(obj_case))
            as_list.append("?")
        if self.action_type.name in ["TIAB+", "TIAB-"]:
            obj = as_list.pop()
            as_list.append(inflect(obj, "N", {"PERS": "3", "CASE": obj_case, "NUM": "SG"}))

        if self.action_type.pre_add is not None:
            add = self.get_synonym(self.action_type.pre_add)
            as_list.insert(0, add)
            if self.action_type.name in ["TOTN", "TIA+", "SAM-KAN", "MYÖ", "KII"] and self.speaker.mood.arousal < random.uniform(-0.5, 0.5):
                as_list = [add]
        if self.action_type.post_add is not None:
            add = self.get_synonym(self.action_type.post_add)
            as_list.append(add)

        if self.action_type.ques:
            as_list.append("?")

        return as_list

    def get_synonym(self, word):
        if word == "EVAL":
            appraisal = self.project.get_appraisal(self.speaker)
            if not self.project.speakers_agree([self.speaker, self.listeners[0]]):
                appraisal = self.project.get_appraisal(self.listeners[0])
            options = evaluations_dictionary[appraisal.name]
            return random.choices(options)[0]
        if word in noun_dictionary:
            return random.choices(noun_dictionary[word])[0]
        if word in verb_dictionary:
            options = verb_dictionary[word]
            return random.choices(options)[0]
        if self.reversed and word in reversed_verb_dictionary:
            options = reversed_verb_dictionary[word]
            return random.choices(options)[0]
        return word

    def get_interrogative(self, case):
        person = type(self.obj) is Character
        if person:
            if case == "GEN":
                return "kenen"
            elif case == "ILL":
                return "keneen"
            elif case == "INE":
                return "kenessä"
            elif case == "ELA":
                return "kenestä"
            elif case == "PAR":
                return "ketä"
            return "kuka"

        if case == "GEN":
            return "minkä"
        elif case == "ILL":
            return "mihin"
        elif case == "INE":
            return "missä"
        elif case == "ELA":
            return "mistä"
        elif case == "PAR":
            return "mitä"
        return "mikä"

    def get_styled_sentence(self):
        if self.inflected is None:
            return None
        return self.speaker.style.get_styled_expression(self.inflected)
