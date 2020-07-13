import csv


def load_situations(path="../data/situation_rules.csv"):
    situations = {}
    with open(path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter="\t")
        for row in csv_reader:
            characters = row[1].split(",")
            a_expansions = row[2].split(",") if row[2] != "none" else None
            b_expansions = row[3].split(",") if row[3] != "none" else None
            a_project = row[4] if row[4] != "none" else "none"
            b_project = row[5] if row[5] != "none" else "none"
            situations[row[0]] = {"characters": characters,
                                "a_expansions": a_expansions,
                                "b_expansions": b_expansions,
                                "a_project": a_project,
                                "b_project": b_project}
    for i in situations:
        print(i, situations[i])
    return situations
