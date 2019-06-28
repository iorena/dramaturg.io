import csv

from concepts.action_type import ActionType


def load_action_types(path="../data/action_types.csv"):
    actions = {}
    with open(path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter="\t")
        for row in csv_reader:
            actions[row[0]] = ActionType(*row)
    return actions
