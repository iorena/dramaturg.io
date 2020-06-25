import csv


def load_situations(path="../data/situation_rules.csv"):
    situations = {}
    with open(path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter="\t")
        for row in csv_reader:
            a_sequences = row[1].split(",") if row[1] != "none" else None
            b_sequences = row[2].split(",") if row[2] != "none" else None
            a_expansions = row[3].split(",") if row[3] != "none" else None
            b_expansions = row[4].split(",") if row[4] != "none" else None
            a_project = row[5] if row[5] != "none" else "none"
            b_project = row[6] if row[6] != "none" else "none"
            situations[row[0]] = {"a_sequences": a_sequences,
                                "b_sequences": b_sequences,
                                "a_expansions": a_expansions,
                                "b_expansions": b_expansions,
                                "a_project": a_project,
                                "b_project": b_project}
    for i in situations:
        print(i, situations[i])
    return situations
