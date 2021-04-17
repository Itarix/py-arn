import getopt, sys

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

    def analyse_sequence(self, file=None):
        self._check_sequences_(file)
        self._check_nucleotides_lines_(file)
        self._check_nucleotides_loop_(file)

    def _check_nucleotides_loop_(self, file=None):
        write("-------------------------------------", self.verbose, file)
        write("Check sequences Loop Method Start.", self.verbose, file)

        nucleotide_sequences1 = str_to_nucleotides("AGCUACCCCGGGUUUAGVF")
        nucleotide_sequences2 = str_to_nucleotides("AGCUACCCCGGGUUUAGVF")

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

    def _check_sequences_(self, file=None):
        write("-------------------------------------", self.verbose, file)
        write("Check sequences Start.", self.verbose, file)
        nb_error = 0
        for i in range(0, self.size_sequence_1):
            if self.size_sequence_1 != self.size_sequence_2 and (
                    i == self.size_sequence_1 or i == self.size_sequence_2):
                write(format_error("Bad size sequences", sequence_1[i], " ", i), self.verbose, file)
                nb_error = nb_error + 1
                break

            if sequence_1[i] != sequence_2[i]:
                write(format_error("Bad value", sequence_1[i], sequence_2[i], i), self.verbose, file)
                nb_error = nb_error + 1

        if nb_error > 0:
            write(f'Number of errors while analyse sequences =>  {nb_error:1d}', self.verbose, file)
        write("Check sequences End.", self.verbose, file)
        write("-------------------------------------", self.verbose, file)

    def _check_nucleotides_lines_(self, file=None):
        copy_sequence_2 = self.sequence2
        copy_sequence_1 = self.sequence1
        write("-------------------------------------", self.verbose, file)
        write("Check sequences with linear method Start.", self.verbose, file)
        for j in range(0, self.size_sequence_1):
            if j > 0:
                if add_space_sequence1:
                    copy_sequence_1 = " " + copy_sequence_1
                else:
                    copy_sequence_2 = " " + copy_sequence_2

            size_sequence_1 = len(copy_sequence_1)
            size_sequence_2 = len(copy_sequence_2)

            nb_error_imbricate = 0
            write(f'Analyse => sequence 1 : {copy_sequence_1:1} vs sequence 2 : {copy_sequence_2:1}', self.verbose,
                  file)
            for i in range(0, size_sequence_2):
                if size_sequence_1 != size_sequence_2 and (i + 1 == size_sequence_1 or i + 1 == size_sequence_2):
                    write("end of sequences", self.verbose, file)
                    break
                if is_can_be_imbriquate(copy_sequence_1[i], copy_sequence_2[i]):
                    write(format_error("Can be imbricate", copy_sequence_1[i], copy_sequence_2[i], i), self.verbose,
                          file)
                    nb_error_imbricate = nb_error_imbricate + 1

            percent = nb_error_imbricate / self.min_size_sequence * 100
            write(f'We have found : {nb_error_imbricate:1d} error. Percent {percent:1.02f}', self.verbose, file)
            if percent > error_percent:
                write(f'Bad combination : {percent:1.02f}%', self.verbose, file)
        write("Check sequences with linear method End.", self.verbose, file)
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


def usage():
    helpText = """This script is used to compare sequence of nucleotides
        
        This script accept parameters of this list. 
        
        --help (shortcut: -h)
            Show the way how use the script
        --sequence1
            First Sequence to be compare.
            Example = --sequence1=UCGA
            Default value is : UCGUACCGUGAGUAAUAAUGCGB
        --sequence2
            Second Sequence to be compare. 
            Example = --sequence1=UCGA
            Default value is : UAACACUGUCUGGUAACGAUGU
        --percent
            Variable of percentage of accepted comparison. 
            Example = --percent=50
            Default value is : 30
        --decalSeq1
            If Not Provided : it will add space to sequence 1.
            If yes: it will add space to sequence 2.
            Example = --decalSeq1
        --verbose
            If provided ; it will print in standard output logs.
            If not : it will not print logs.
            Example = --verbose
        --output
            Specify the file where the file of result will be create.
            Example = --output=/tmp/resultFile.txt
            Default value is : /tmp/result.txt
"""
    print(helpText)


if __name__ == "__main__":
    # execute only if run as a script
    error_percent = 30
    sequence_1 = "UCGUACCGUGAGUAAUAAUGCGB"
    sequence_2 = "UAACACUGUCUGGUAACGAUGQ"
    # jf true so it will add space before sequence 2
    # If False so it will add space before sequence 1
    add_space_sequence1 = True
    filename_output = "/tmp/result.txt"
    is_verbose = False

    try:
        opts, argv = getopt.getopt(
            sys.argv[1:],
            "h",
            ['help', 'sequence1=', 'sequence2=', 'percent=', 'output=', 'decalSeq2', 'verbose']
        )
    except getopt.GetoptError as err:
        # print help information and exit:
        usage()
        print(err)  # will print something like "option -a not recognized"
        sys.exit(2)

    for k, v in opts:
        if k == '-h' or k == '--help':
            usage()
            sys.exit(0)
        if k == '--sequence1':
            sequence_1 = v
        if k == '--sequence2':
            sequence_2 = v
        if k == '--percent':
            error_percent = v
        if k == '--output':
            filename_output = v
        if k == '--decalSeq1':
            add_space_sequence1 = False
        if k == '--verbose':
            is_verbose = True

    file_output = open(filename_output, "w")
    compare_nucl = CompareNucleotide(
        sequence_1, sequence_2, error_percent, add_space_sequence1, is_verbose
    )
    compare_nucl.analyse_sequence(file_output)
    file_output.close()
