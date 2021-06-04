from nucleotide import str_to_nucleotides
from nucleotide import nucleotides_to_str
import itertools

class CompareNucleotide:
    def __init__(self, sequence1, sequence2, percent_error, add_space_sequence_1, verbose=False):
        self.sequence1 = sequence1
        self.sequence2 = sequence2
        self.size_sequence_1 = len(sequence_1)
        self.size_sequence_2 = len(sequence_2)
        self.percent_error = percent_error
        self.add_space_sequence_1 = add_space_sequence_1
        self.verbose = verbose

        self.min_size_sequence = self.size_sequence_2
        self.max_size_sequence = self.size_sequence_1
        if self.size_sequence_2 > self.size_sequence_1:
            self.min_size_sequence = self.size_sequence_1
            self.max_size_sequence = self.size_sequence_2

    def _check_nucleotides_loop_(self, file=None):
        # write("-------------------------------------", self.verbose, file)
        # write("Check sequences Loop Method Start.", self.verbose, file)
        #
        # nucleotide_sequences1 = str_to_nucleotides(self.sequence1)
        # nucleotide_sequences2 = str_to_nucleotides(self.sequence2)

        # copy all object
        cp_nucleotide1 = nucleotide_sequences1
        cp_nucleotide2 = nucleotide_sequences2

        for seq_1 in permutations(cp_nucleotide1):
            for seq_2 in permutations(cp_nucleotide2):
                seq_1_position = []
                loop_broken = False
                write(f'Sequence 1 : {nucleotides_to_str(seq_1)} ==> Sequence 2 : {nucleotides_to_str(seq_2)}',
                      self.verbose, file)
                for k in range(0, len(seq_1)):
                    seq_1_position.append(seq_1[k].original_position)
                    nb_error_imbricate = 0
                    seq_2_position = []
                    for l in range(0, len(seq_2)):
                        seq_2_position.append(seq_2[l].original_position)

                        if is_can_be_imbriquate(seq_1[k].value, seq_2[l].value):
                            if max(seq_2_position) > seq_2[l].original_position or \
                                    max(seq_1_position) > seq_1[k].original_position:
                                loop_broken = True
                                break

                            write(
                                f'Can be imbricate : {seq_1[k].value:1} at {k:1d} position ===> {seq_2[l].value:1} at {l:1d} position',
                                self.verbose, file
                            )
                            nb_error_imbricate = nb_error_imbricate + 1
                    if loop_broken:
                        break
                    percent = nb_error_imbricate / self.min_size_sequence * 100
                    write(f'We have found : {nb_error_imbricate:1d} error. Percent {percent:1.02f}', self.verbose, file)
                    if percent > error_percent:
                        write(f'Bad combination : {percent:1.02f}%', self.verbose, file)
                if loop_broken:
                    write(f'Broken loop : Sequence 1 : {nucleotides_to_str(seq_1)} ==> Sequence 2 : {nucleotides_to_str(seq_2)}',
                          self.verbose,
                          file)
                    break

        write("Check sequences Loop Method End.", self.verbose, file)
        write("-------------------------------------", self.verbose, file)

def permutations(list_to_permute: list):
    return itertools.permutations(list_to_permute, len(list_to_permute))


def is_can_be_imbriquate(val1, val2):
    if val1 == "A" and val2 == "U":
        is_imbricate = True
    elif val1 == "C" and val2 == "G":
        is_imbricate = True
    else:
        is_imbricate = False
    return is_imbricate


def format_error(error_message, val1, val2, index):
    return f'Error: {error_message:30} => sequence 1 : {val1:1} vs sequence 2 : {val2:1} ==> at position {index:10d}'


def write(string_to_write, verbose, file=None):
    if verbose:
        print(string_to_write)
    if file is not None:
        file.write(string_to_write + "\n")
