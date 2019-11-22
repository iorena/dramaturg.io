import csv

def load_pad_values(path="../data/seq_and_action_types_to_pad.csv"):
    values = {}
    with open(path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter="\t")
        for row in csv_reader:
            #tuple where first value is effect, second is tuple that describes the edges of usability
            values[row[0]] = ((float(row[1]), float(row[2]), float(row[3])), ((float(row[4]), float(row[5]), float(row[6])), (float(row[7]), float(row[8]), float(row[9]))))
    return values


