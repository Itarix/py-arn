import getopt
import sys
from datetime import datetime

import log
from arn import Arn, arn_to_str_with_position
from compare_loop_arn import _compare_loop_arn_sequence_, __permutations__


def generate_all_permutations(
        arn1: Arn, filename: str, logger: log
) -> int:
    """

    :rtype: int
    :param arn1: arn which we will generate all permutations
    :param filename: filename where all permutations will be put
    :param logger: logger
    """
    copy_sequence_1 = arn1.get_list_nucleotides()
    nb_sequences_generated: int = 0
    with open(filename, "w") as file:
        for sequence1 in __permutations__(copy_sequence_1):
            nb_sequences_generated = nb_sequences_generated + 1
            file.write(arn_to_str_with_position(sequence1) + "\n")
    logger.info(f'{nb_sequences_generated:10d} sequences generated')
    return nb_sequences_generated


def usage():
    help_text = """This script is used to generate all permutations for arn.
        
        This script accept parameters of this list. 
        
        --help (shortcut: -h)
            Show the way how use the script
        --sequence
            First Sequence to be compare.
            Example = --sequence=UCGA
            Default value is : UCGUACCGUGAGUAAUAAUGCG
        --verbose
            If provided ; it will print in standard output logs.
            If not : it will not print logs.
            Example = --verbose
        --log_output
            Specify the path where the log file will be create.
            Example = --output=/tmp/log.txt
        --output
            Specify the path where the log with permutations will be create.
            Default Value => permutations.txt
            Warning: this file can be very huge. (Can be higher than 150GB, not tested with higher because slow memory)
            Example = --output=/tmp/resultFile.txt
            The result file had the sequence permuted with value and position.
            C1G3A2

"""
    print(help_text)


if __name__ == "__main__":
    # execute only if run as a script
    SEQUENCE = "UCGUACCGUGAGUAAUAAUGCG"
    PATH_LOG = ""
    IS_VERBOSE = False
    LOG_FILE = "permutations.txt"

    try:
        opts, argv = getopt.getopt(
            sys.argv[1:],
            "h",
            [
                'help', 'verbose',
                'sequence=', 'log_output=', "output="]
        )
    except getopt.GetoptError as err:
        usage()
        print(err)  # will print something like "option -a not recognized"
        sys.exit(2)

    for k, v in opts:
        if k in ('-h', '--help'):
            usage()
            sys.exit(0)
        if k == '--sequence':
            SEQUENCE = v
        if k == '--log_output':
            PATH_LOG = v
        if k == '--verbose':
            IS_VERBOSE = True
        if k == '--output':
            LOG_FILE = v

    if len(SEQUENCE) > 30:
        print("Error: Arn sequences max size is 30")
        exit(1)

    logger = log.Log(None, IS_VERBOSE, PATH_LOG)
    arn = Arn(SEQUENCE)

    dateDebut = datetime.now()

    logger.debug("date start : " + str(dateDebut))
    logger.info("-------------------------------------")
    logger.info("Check sequences Loop Method Start.")
    generate_all_permutations(arn, LOG_FILE, logger)
    logger.info("Check sequences Loop Method End.")
    logger.info("-------------------------------------")
    logger.debug("date end : " + str(datetime.now()))
    logger.debug("process time : " + str(datetime.now() - dateDebut))
