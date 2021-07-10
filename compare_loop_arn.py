import datetime
import itertools
import multiprocessing
import getopt
import sys
import log
from arn import Arn, arn_to_str
from log import Log
from nucleotide import is_can_be_imbriquate


def compare_loop_arn(
        arn1: Arn, arn2: Arn,
        logger: Log, error_percent: int = 30,
        nb_process=1
):
    """

    :param arn1:
    :param arn2:
    :param logger:
    :param error_percent:
    :param nb_process:
    """
    copy_sequence_1 = arn1.get_sequence_list()
    copy_sequence_2 = arn2.get_sequence_list()

    size_sequence1 = len(copy_sequence_1)
    size_sequence2 = len(copy_sequence_2)

    min_size_sequence = size_sequence2
    if size_sequence2 > size_sequence1:
        min_size_sequence = size_sequence1

    if nb_process == 1:
        for sequence1 in __permutations__(copy_sequence_1):
            for sequence2 in __permutations__(copy_sequence_2):
                _compare_loop_arn_sequence_(
                    sequence1, sequence2,
                    min_size_sequence, logger, error_percent
                )
    else:
        nb_stock = 1000

        tab_sequence1 = []
        for sequence1 in __permutations__(copy_sequence_1):
            tab_sequence1.append(sequence1)

            if len(tab_sequence1) > nb_stock:
                with multiprocessing.Pool(processes=nb_process, maxtasksperchild=nb_stock) as pool_process:
                    for sequence1_process in tab_sequence1:
                        for sequence2 in __permutations__(copy_sequence_2):
                            pool_process.apply_async(
                                _compare_loop_arn_sequence_,
                                [sequence1_process, sequence2, min_size_sequence, logger, error_percent]
                            )
                    pool_process.close()
                    pool_process.join()
                tab_sequence1.clear()

        if len(tab_sequence1) > 0:
            with multiprocessing.Pool(processes=nb_process, maxtasksperchild=nb_stock) as pool_process:
                for sequence1 in tab_sequence1:
                    for sequence2 in __permutations__(copy_sequence_2):
                        pool_process.apply_async(
                            _compare_loop_arn_sequence_,
                            [sequence1, sequence2, min_size_sequence, logger, error_percent]
                        )
                pool_process.close()
                pool_process.join()
                tab_sequence1.clear()


def _compare_loop_arn_sequence_(sequence1, sequence2, min_size_sequence, logger, error_percent):
    seq_1_position_history = []

    seq1_str = arn_to_str(sequence1)
    seq2_str = arn_to_str(sequence2)

    for k in range(0, len(sequence1)):
        seq_1_position_history.append(sequence1[k].original_position)
        nb_imbricate = 0
        seq_2_position_history = []
        for l in range(0, len(sequence2)):
            # logger.debug(f'Process {seq1_str:26} | {seq2_str:26}')
            seq_2_position_history.append(sequence2[l].original_position)

            if is_can_be_imbriquate(sequence1[k].value, sequence2[l].value):
                if max(seq_2_position_history) > sequence2[l].original_position or \
                        max(seq_1_position_history) > sequence1[k].original_position:
                    return
                nb_imbricate = nb_imbricate + 1

        percent = (nb_imbricate / min_size_sequence) * 100

        if percent > error_percent:
            logger.warning(f'{seq1_str:26} | {seq2_str:26} ===> ' +
                           f'number imbricate {nb_imbricate:2d} : error {percent:1.02f}%')


def __permutations__(list_to_permute: list) -> object:
    return itertools.permutations(list_to_permute, len(list_to_permute))


def usage():
    help_text = """This script is used to compare sequence of nucleotides
        
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
            Only used for the line comparison
            Example = --percent=50
            Default value is : 30
        --verbose
            If provided ; it will print in standard output logs.
            If not : it will not print logs.
            Example = --verbose
        --output
            Specify the file where the file of result will be create.
            Warning. The output file can be huge. At least 60GB
            Example = --output=/tmp/resultFile.txt
        --nbProcess
            Specify the number of process used for treatment which need processing long time.
            Default : 1
            Example = --nbProcess=2
"""
    print(help_text)


if __name__ == "__main__":
    # execute only if run as a script
    ERROR_PERCENT = 30
    SEQUENCE_1 = "UCGUACCGUGAGUAAUAAUGCGB"
    SEQUENCE_2 = "UAACACUGUCUGGUAACGAUGQ"
    # jf true so it will add space before sequence 2
    # If False so it will add space before sequence 1
    FILENAME_OUTPUT = ""
    IS_VERBOSE = False
    NB_PROCESS = 1

    try:
        opts, argv = getopt.getopt(
            sys.argv[1:],
            "h",
            [
                'help', 'verbose',
                'sequence1=', 'sequence2=', 'percent=', 'output=', 'nbProcess=']
        )
    except getopt.GetoptError as err:
        usage()
        print(err)  # will print something like "option -a not recognized"
        sys.exit(2)

    for k, v in opts:
        if k in ('-h', '--help'):
            usage()
            sys.exit(0)
        if k == '--sequence1':
            SEQUENCE_1 = v
        if k == '--sequence2':
            SEQUENCE_2 = v
        if k == '--percent':
            ERROR_PERCENT = v
        if k == '--output':
            FILENAME_OUTPUT = v
        if k == '--verbose':
            IS_VERBOSE = True
        if k == '--nbProcess':
            NB_PROCESS = int(v)

    if len(SEQUENCE_1) > 30 or len(SEQUENCE_2) > 30:
        print("Arn sequences max size is 30")
        exit(1)

    logger = log.Log(None, IS_VERBOSE, FILENAME_OUTPUT)
    arn1 = Arn(SEQUENCE_1)
    arn2 = Arn(SEQUENCE_2)

    dateDebut = datetime.datetime.now()

    logger.debug("-------------------------------------")
    logger.debug("Check sequences Loop Method Start.")
    compare_loop_arn(arn1, arn2, logger, ERROR_PERCENT, NB_PROCESS)
    logger.debug("Check sequences Loop Method End.")
    logger.debug("-------------------------------------")

    print(dateDebut)
    print(datetime.datetime.now())
