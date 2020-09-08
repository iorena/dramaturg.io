from concepts.affect.emotion import Emotion


class ActionType:

    def __init__(self, name, neg, ques, subj, verb, obj, aux_verb, modus, tempus, passive, pre_add, post_add):
        self.name = name
        if len(name) == 6:
            self.class_name = name[0:3]
        else:
            self.class_name = name
        self.neg = neg == "TRUE"
        self.ques = ques == "TRUE"
        self.subj = subj
        if self.subj == "None":
            self.subj = None
        self.verb = verb
        if verb == "None":
            self.verb = None
        self.obj = obj
        if obj == "None":
            self.obj = None
        if aux_verb == "None":
            self.aux_verb = None
        else:
            self.aux_verb = aux_verb.split(",")
        self.modus = modus
        self.tempus = tempus
        self.passive = passive == "TRUE"
        if pre_add == "None":
            self.pre_add = None
        else:
            self.pre_add = pre_add.split(";")
        if post_add == "None":
            self.post_add = None
        else:
            self.post_add = post_add.split(";")

    def add_pad_data(self, effect_p, effect_a, effect_d, lower_bound_p, lower_bound_a, lower_bound_d, upper_bound_p, upper_bound_a, upper_bound_d):
        self.effect = Emotion(None, effect_p, effect_a, effect_d)
        self.lower_bound = Emotion(None, lower_bound_p, lower_bound_a, lower_bound_d)
        self.upper_bound = Emotion(None, upper_bound_p, upper_bound_a, upper_bound_d)
        return self

    def is_accepting(self):
        if self.name[:3] in ["TTN", "MYÖ", "VSM", "VYL", "MMK", "PVK", "VLK", "VVK"]:
            return True
        return False

    def can_use(self, emotion):
        if self.upper_bound.pleasure >= emotion.pleasure and emotion.pleasure >= self.lower_bound.pleasure:
            if self.upper_bound.arousal >= emotion.arousal and emotion.arousal >= self.lower_bound.arousal:
                if self.upper_bound.dominance >= emotion.dominance and emotion.dominance >= self.lower_bound.dominance:
                    return True
        return False

    def get_hesitation(self, speaker, listener, project):
        """
        Character hesitates if his goals make him use turns that he doesn't want to use (because of relationship)
        """
        if project.proj_type not in ["statement", "proposal", "complain"]:
            return False
        perceived_mood = speaker.perception.get_object_by_name(listener.name).mood
        mood_after_turn = perceived_mood.affect_mood(self.effect)[0]
        current_mood_diff = perceived_mood - speaker.relations[listener.name]
        mood_diff_after_turn = mood_after_turn - speaker.relations[listener.name]
        if current_mood_diff.get_vector() < mood_diff_after_turn.get_vector():
            speaker.add_stress(project, listener, mood_after_turn)
            return True
        else:
            #else listener is affected
            listener.add_stress(project, speaker, None)
            return False
