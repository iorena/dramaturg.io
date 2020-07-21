from syntaxmaker.syntax_maker import (create_verb_pharse, create_personal_pronoun_phrase, turn_vp_into_question,
                                      create_copula_phrase, create_phrase, auxiliary_verbs, add_auxiliary_verb_to_vp,
                                      add_advlp_to_vp, set_vp_mood_and_tense, turn_vp_into_prefect,
                                      negate_verb_pharse, turn_vp_into_passive)
from syntaxmaker.inflector import inflect
from language.dictionary import Dictionary
from concepts.character import Character
from language.embeddings import Embeddings
import random

from numpy import array
from numpy.linalg import norm


class Sentence:
    embeddings = Embeddings("isoäiti", "maljakko")

    def __init__(self, speaker, listeners, project, action_type, obj_type, reverse, hesitation):
        self.speaker = speaker
        self.listeners = listeners
        self.attribute = False
        self.project = project
        self.hesitation = hesitation
        self.add_add = None
        #subject
        if project.subj is None:
            self.subj = None
        elif action_type.subj == "Listener" or type(project.subj) is str and project.subj == "Listener":
            self.subj = self.listeners[0].name
        elif action_type.subj == "subject":
            if type(project.subj) is str:
                self.subj = project.subj
            else:
                self.subj = project.subj.name
        elif action_type.subj == "object":
            if project.obj is not None:
                if type(project.obj) is str:
                    self.subj = project.obj
                else:
                    self.subj = project.obj.name
            else:
                self.subj = Sentence.embeddings.get_noun_from_verb(project.verb)
        elif action_type.subj == "Speaker":
            self.subj = speaker.name
        elif action_type.subj == "parent":
            self.subj = project.parent.subj
        elif action_type.subj == "null":
            self.subj = "null"
        else:
            self.subj = action_type.subj

        #verb
        if action_type.verb == "project" or action_type.verb == "isolated":
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
        elif action_type.obj == "object" or action_type.obj == "subject":
            if self.project.obj_type == "static":
                self.obj = project.obj
            else:
                self.obj = project.obj.name
        elif action_type.obj == "attribute":
            self.obj = project.obj.name
            self.attribute = True
        elif action_type.obj == "Speaker":
            self.obj = speaker.name
        elif action_type.obj == "noun":
            self.obj = "noun"
        else:
            self.obj = action_type.obj

        ### exceptions ###
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

        #can't be surprised by own want -> change to other's want of something done by self
        #doesn't work, dunno why
        if self.action_type.name[:3] == "YLL" and self.verb == "haluta":
            self.add_add = self.obj
            self.subj = self.listeners[0].name
            self.obj = self.speaker.name
        elif self.action_type.name[:3] == "VYL" and self.verb == "haluta":
            self.add_add = self.obj
            self.subj = self.speaker.name
            self.obj = self.listeners[0].name

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

            as_list = self.add_pre_add(as_list)

            if len(as_list) > 0 and self.action_type.name in ["TIAB+", "TIAB-"]:
                obj_case = self.get_synonym(self.project.verb)[1]
                if obj_case == "GEN" and (self.action_type.neg or self.action_type.passive or self.action_type.modus == "IMPV"):
                    obj_case = "PAR"
                obj = as_list.pop()
                obj_i = inflect(obj, "N", {"PERS": "3", "CASE": obj_case, "NUM": "SG"})
                as_list.append(obj_i)

            if self.add_add is not None:
                as_list.append(self.add_add)

            as_list = self.add_post_add(as_list)

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

        #if verb is isolated, return just that (+ adds)
        if self.action_type.verb == "isolated":
            return self.get_isolated_verb(vp)

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
        if self.obj_type == "static":
            obj_case = "NOM"
        #for some reason syntaxmaker doesn't accept objects for thes "hommata" and "saada", so must workaround
        #this also causes problems when using imperative forms because object case isn't altered accordingly
        elif self.verb in list(map(lambda x: x[0], Dictionary.verb_dictionary["hankkia"])):
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

        as_list = self.add_pre_add(as_list)
        as_list = self.add_post_add(as_list)

        #remove null subject
        if "null" in as_list:
            as_list.remove("null")

        #remove "lienyt", thanks syntaxmaker
        if "lienyt" in as_list:
            as_list.insert(as_list.index("lienyt"), "ollut")
            as_list.remove("lienyt")

        if self.action_type.ques:
            as_list.append("?")

        return as_list

    def get_synonym(self, word):
        print(word)
        appraisal = self.project.get_appraisal(self.speaker)
        if word in Dictionary.valence_dictionary:
            index = 0
            if appraisal.id > 92:
                index = 1
            return Dictionary.valence_dictionary[word][index]
        if word == "EVAL":
            #if not self.listener_agrees:
            #    appraisal = self.project.get_appraisal(self.listeners[0])
            options = Dictionary.evaluations_dictionary[appraisal.name]
            return random.choice(options)
        if word in Dictionary.noun_dictionary:
            return random.choice(Dictionary.noun_dictionary[word])
        if word in Dictionary.verb_dictionary:
            options = Dictionary.verb_dictionary[word]
            return random.choice(options)
        if self.reversed and word in Dictionary.reversed_verb_dictionary:
            options = Dictionary.reversed_verb_dictionary[word]
            return random.choice(options)
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

    def add_pre_add(self, as_list):
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
        return as_list

    def add_post_add(self, as_list):
        if self.action_type.post_add is not None:
            post_add = random.choices(self.action_type.post_add)[0]
            if post_add == "interrogative":
                add = self.get_interrogative("NOM")
            else:
                add = self.get_synonym(post_add)
            if add != "None":
                as_list.append(add)
        return as_list


    def get_isolated_verb(self, vp):
        # returns verb inflected but without subject or object
        as_list = vp.to_string().split()
        del as_list[0]
        return self.add_post_add(self.add_pre_add(as_list))

    def get_explicative(self, mood):
        valence = "pos" if not self.action_type.neg else "neg"
        distances = list(map(lambda x: norm(array(mood) - x), Dictionary.explicatives_dictionary[valence].values()))
        return random.choices(list(Dictionary.explicatives_dictionary[valence].keys()), distances)[0]

    def get_styled_sentence(self):
        if self.inflected is None:
            return None
        styled = self.speaker.style.get_styled_expression(self.inflected)

        if self.hesitation:
            styled = self.speaker.style.get_hesitant_expression(styled)

        return styled
