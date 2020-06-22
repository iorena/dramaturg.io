import csv

from concepts.project import Project
from concepts.worldobject import WorldObject

def load_topics(world_state, path="../data/opposing_topics.csv"):

    objects = []
    with open(path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter="\t")
        for row in csv_reader:
            #subject
            if row[2] not in ["PERSON", "PASSIVE"]:
                objects.append(WorldObject(row[2]))
            #object
            if row[5] not in ["PERSON", "PASSIVE"] and row[5] not in [obj.name for obj in objects]:
                objects.append(WorldObject(row[5]))
    world_state.objects += objects

    pos_topics = []
    neg_topics = []
    with open(path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter="\t")
        for row in csv_reader:
            if row[2] == "PERSON":
                #todo: do we even need PERSON?
                subj = world_state.characters[0]
            elif row[2] == "PASSIVE":
                subj = None
            else:
                subj = world_state.get_object_by_name(row[2])

            verb = row[3]

            if row[5] == "NONE":
                obj = None
            else:
                obj = world_state.get_object_by_name(row[5])

            obj_type = row[6]

            score = row[1]

            if row[0] == "TRUE":
                neg_topics.append(Project(subj, verb, (obj_type, obj), "present", score))
            else:
                pos_topics.append(Project(subj, verb, (obj_type, obj), "present", score))

    return pos_topics, neg_topics
