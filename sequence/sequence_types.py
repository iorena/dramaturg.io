import csv


class SequenceType:
    def load_sequence_types():
        pos_sequences = {}
        neg_sequences = {}
        with open("sequence/sequence_types.csv") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter="\t")
            for row in csv_reader:
                pos_sequences[row[0]] = (row[1], row[2])
                neg_sequences[row[0]] = (row[3], row[4])
        return pos_sequences, neg_sequences
