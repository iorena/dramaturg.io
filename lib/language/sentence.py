from syntaxmaker.syntax_maker import (create_verb_pharse, create_personal_pronoun_phrase, turn_vp_into_question,
                                      create_copula_phrase, create_phrase, auxiliary_verbs, add_auxiliary_verb_to_vp,
                                      add_advlp_to_vp, set_vp_mood_and_tense, turn_vp_into_prefect,
                                      negate_verb_pharse, turn_vp_into_passive)
from syntaxmaker.inflector import inflect
from language.dictionary import verb_dictionary, noun_dictionary, reversed_verb_dictionary, evaluations_dictionary, explicatives_dictionary
from concepts.character import Character
from language.embeddings import Embeddings
import random

from numpy import array
from numpy.linalg import norm


class Sentence:
    embeddings = Embeddings()

    def __init__(self, speaker, listeners, project, action_type, obj_type, reverse, hesitation):
        self.speaker = speaker
        self.listeners = listeners
        self.attribute = False
        self.project = project
        self.hesitation = hesitation
        #subject
        if project.subj is None:
            self.subj = None
        elif action_type.subj == "subject":
            self.subj = project.subj.name
        elif action_type.subj == "object":
            if project.obj is not None:
                self.subj = project.obj.name
            else:
                self.subj = Sentence.embeddings.get_noun_from_verb(project.verb)
        elif action_type.subj == "Listener":
            self.subj = listeners[0].name
        elif action_type.subj == "Speaker":
            self.subj = speaker.name
        elif action_type.subj == "parent":
            self.subj = project.parent.subj
        elif action_type.subj == "null":
            self.subj = "null"
        else:
            self.subj = action_type.subj

        #verb
        if action_type.verb == "project":
            self.verb = project.verb
        else:
            self.verb = action_type.verb
        self.verb_realization = None
        if action_type.tempus == "project":
            self.tempus = project.time
        else:
            self.tempus = action_type.tempus

        #"object"
        if project.obj is None:
            self.obj = None
        elif action_type.obj == "object":
            self.obj = project.obj.name
        elif action_type.obj == "subject":
            self.obj = project.subj.name
        elif action_type.obj == "attribute":
            print(project.obj)
            self.obj = project.obj.name
            self.attribute = True
        elif action_type.obj == "Speaker":
            self.obj = speaker.name
        elif action_type.obj == "noun":
            self.obj = "noun"
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
                explicative = None
                attribute = ""
                if self.obj_type == "owner":
                    attribute = inflect(self.obj, "N", {"PERS": "3", "CASE": "GEN", "NUM": "SG"})
                elif self.obj_type == "location":
                    attribute = inflect(self.obj, "N", {"PERS": "3", "CASE": "INE", "NUM": "SG"}) + " oleva"
                elif self.obj_type in ["weather", "appraisal"]:
                    if self.speaker.mood.arousal > random.random():
                        explicative = self.get_explicative([self.speaker.mood.pleasure, self.speaker.mood.arousal, self.speaker.mood.dominance])
                    obj_case = self.get_synonym(self.project.verb)[1]
                    attribute = inflect(self.get_synonym(self.obj), "N", {"PERS": "3", "CASE": obj_case, "NUM": "SG"})
                else:
                    print(self.obj_type)

                as_list.insert(0, attribute)
                if explicative:
                    as_list.insert(0, explicative)
            elif self.obj is not None:
                obj = self.get_synonym(self.obj)
                as_list.insert(0, obj)

            if self.action_type.pre_add is not None:
                pre_add = random.choices(self.action_type.pre_add)[0]
                if pre_add == "interrogative":
                    add = self.get_interrogative("NOM")
                else:
                    add = self.get_synonym(pre_add)
                if add != "None":
                    as_list.insert(0, add)

            if len(as_list) > 0 and self.action_type.name in ["TIAB+", "TIAB-"]:
                obj_case = self.get_synonym(self.project.verb)[1]
                if obj_case == "GEN" and (self.action_type.neg or self.action_type.passive or self.action_type.modus == "IMPV"):
                    obj_case = "PAR"
                obj = as_list.pop()
                obj_i = inflect(obj, "N", {"PERS": "3", "CASE": obj_case, "NUM": "SG"})
                as_list.append(obj_i)

            if self.action_type.post_add is not None:
                post_add = random.choices(self.action_type.post_add)[0]
                if post_add == "interrogative":
                    add = self.get_interrogative("NOM")
                else:
                    add = self.get_synonym(post_add)
                if add != "None":
                    as_list.append(add)

            if self.action_type.ques:
                as_list.append("?")

            return as_list

        if self.verb is "olla":
            vp = create_copula_phrase()
        else:
            self.verb_realization = self.get_synonym(self.verb)
            vp = create_verb_pharse(self.verb_realization[0])

        mood = self.action_type.modus

        #check person
        if self.speaker.name == self.subj:
            person = "1"
            #cannot command self
            mood = "INDV"
            vp.components["subject"] = create_personal_pronoun_phrase()
        elif self.subj in [listener.name for listener in self.listeners]:
            person = "2"
            #todo, more prodrop?
            prodrop = mood == "IMPV" or self.action_type.name in ["TOEB"]
            vp.components["subject"] = create_personal_pronoun_phrase("2", "SG", prodrop)
        else:
            person = "3"
            vp.components["subject"] = create_phrase("NP", self.get_synonym(self.subj))

        obj_case = "NOM"
        #check "object"
        if self.obj == "noun":
            obj = Sentence.embeddings.get_noun_from_verb(self.project.verb)
        else:
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
        if obj_case == "GEN" and (self.action_type.neg or self.action_type.passive or mood == "IMPV"):
            obj_case = "PAR"
        if self.obj is not None and obj_case is not "NONE" and self.obj not in ["interrogative", "demonstrative"]:
            if self.speaker.name == obj:
                obj = create_personal_pronoun_phrase()
                obj.morphology = {"PERS": "1", "NUM": "SG", "CASE": obj_case}
            elif self.listeners[0].name == obj:
                obj = create_personal_pronoun_phrase("2", "SG")
                obj.morphology = {"PERS": "2", "NUM": "SG", "CASE": obj_case}
            else:
                obj = create_phrase("NP", obj, {"CASE": obj_case})
                if self.obj == "noun":
                    add_advlp_to_vp(vp, create_phrase("NP", self.project.obj.name, {"CASE": "GEN"}))
            add_advlp_to_vp(vp, obj)
            if self.verb is "olla" and self.obj_type is "owner" and type(self.project.subj) is Character:
                pred = create_phrase("NP", "omistaja")
                add_advlp_to_vp(vp, pred)

        #check tempus
        if self.tempus == "imperf":
            tense = "PAST"
            set_vp_mood_and_tense(vp, mood, tense)
        elif self.tempus == "perf":
            tense = "PRESENT"
            set_vp_mood_and_tense(vp, mood, tense)
            turn_vp_into_prefect(vp)
        else:
            tense = "PRESENT"
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
            print("this be the verse", self.subj, self.verb, self.obj, self.project.proj_type)
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

        #add "tosi"/"erittäin" in the right place
        if self.obj_type in ["weather", "appraisal"] and self.speaker.mood.arousal > random.random() and self.action_type.name not in ["TIPB"]:
            explicative = self.get_explicative([self.speaker.mood.pleasure, self.speaker.mood.arousal, self.speaker.mood.dominance])
            as_list.insert(len(as_list) - 1, explicative)

        if self.action_type.name == "TIPB":
            if self.obj_type == "owner" and self.verb == "olla" and type(self.project.subj) is Character:
                as_list.insert(0, "omistaja")
        #add appropriate interrogative and demonstrative
        if self.obj == "interrogative":
            as_list.insert(0, self.get_interrogative(obj_case))
            as_list.append("?")
        if self.obj == "demonstrative":
            as_list.insert(0, self.get_demonstrative(obj_case))

        if self.action_type.pre_add is not None:
            pre_add = random.choices(self.action_type.pre_add)[0]
            if pre_add == "interrogative":
                add = self.get_interrogative("NOM")
            else:
                add = self.get_synonym(pre_add)
            if add != "None":
                as_list.insert(0, add)
            if self.action_type.name in ["TOTN", "TIA+", "SAM-KAN", "MYÖ", "KII"] and self.speaker.mood.arousal < random.uniform(-0.5, 0.5):
                as_list = [add]
        if self.action_type.post_add is not None:
            post_add = random.choices(self.action_type.post_add)[0]
            add = self.get_synonym(post_add)
            if add != "None":
                as_list.append(add)

        #remove null subject
        if "null" in as_list:
            as_list.remove("null")

        if self.action_type.ques:
            as_list.append("?")

        return as_list

    def get_synonym(self, word):
        if word == "EVAL":
            appraisal = self.project.get_appraisal(self.speaker)
            #if not self.speakers_agree:
            #    appraisal = self.project.get_appraisal(self.listeners[0])
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
            elif case == "AKK":
                return "kenet"
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
        elif case == "AKK":
            return "minkä"
        elif case == "ILL":
            return "mihin"
        elif case == "INE":
            return "missä"
        elif case == "ELA":
            return "mistä"
        elif case == "PAR":
            return "mitä"
        elif case == "ALL":
            return "minne"
        if self.obj_type in ["appraisal", "weather", "quality"]:
            return "millainen"
        return "mikä"

    def get_demonstrative(self, case):
        if case == "GEN":
            return "tämän"
        elif case == "AKK":
            return "tämän"
        elif case == "ILL":
            return "tähän"
        elif case == "INE":
            return "tässä"
        elif case == "ELA":
            return "tästä"
        return "tämä"

    def get_explicative(self, mood):
        valence = "pos" if not self.action_type.neg else "neg"
        distances = list(map(lambda x: norm(array(mood) - x), explicatives_dictionary[valence].values()))
        return random.choices(list(explicatives_dictionary[valence].keys()), distances)[0]

    def get_styled_sentence(self):
        if self.inflected is None:
            return None
        styled = self.speaker.style.get_styled_expression(self.inflected)

        if self.hesitation:
            styled = self.speaker.style.get_hesitant_expression(styled)

        return styled
