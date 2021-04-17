class Nucleotide:
    def __init__(self, position, value):
        self.original_position = position
        self.value = value


def str_to_nucleotides(sequence):
    list = []
    for i in range(0, len(sequence)):
        list.append(Nucleotide(i, sequence[i]))
    return list

def nucleotides_to_str(sequence:list):
    str = ""
    for i in range(0, len(sequence)):
        str = str + sequence[i].value
    return str


