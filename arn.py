from nucleotide import Nucleotide


class Arn:

    def __init__(self, sequence: str):
        self.sequence_arn_str = sequence

        tmp = []
        for i in range(0, len(self.sequence_arn_str)):
            tmp.append(Nucleotide(i, self.sequence_arn_str[i]))
        self.sequence_arn_list = tmp

    def get_sequence_list(self):
        return self.sequence_arn_list

    def get_sequence_str(self):
        return self.sequence_arn_str


def arn_to_str(sequence: list):
    tmp = ""
    for i in enumerate(len(sequence)):
        tmp = tmp + sequence[i].value + str(sequence[i].original_position)
    return tmp
