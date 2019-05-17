from syntaxmaker.syntax_maker import *


class Sentence:
    def __init__(self, speaker, listeners, pos, question, aux):
        self.speaker = speaker
        self.listeners = listeners
        self.subj = pos["subj"]
        self.verb = pos["verb"]
        self.obj = pos["obj"]
        self.inflected = self.getInflectedSentence(question, aux)
        self.styled = self.getStyledSentence()

    def getInflectedSentence(self, question, aux):
        if self.verb is None:
            return None
        if self.verb.word is "olla":
            vp = create_copula_phrase()
        else:
            vp = create_verb_pharse(self.verb.word)

        if self.speaker.name is self.subj.word:
            vp.components["subject"] = create_personal_pronoun_phrase()
        elif self.subj.word in [listener.name for listener in self.listeners]:
            vp.components["subject"] = create_personal_pronoun_phrase("2")
        else:
            vp.components["subject"] = create_phrase("NP", self.subj.word)
        if self.obj is not None:
            if self.verb.word is "olla":
                vp.components["predicative"] = create_phrase("NP", self.obj.word)
            else:
                vp.components["dir_object"] = create_phrase("NP", self.obj.word)

        if aux:
            aux = random.choices(list(auxiliary_verbs.keys()))[0]
            add_auxiliary_verb_to_vp(vp, aux)
        if question:
            turn_vp_into_question(vp)
        as_string = vp.to_string().split()
        return as_string

    def getStyledSentence(self):
        if self.inflected is None:
            return None
        return self.speaker.style.getStyledExpression(self.inflected)


