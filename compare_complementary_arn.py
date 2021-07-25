from datetime import datetime

import log
import getopt
import sys

from nucleotide import can_pair
from arn import Arn
from log import Log


def compare_complementary_arn(
        arn1: Arn, arn2: Arn,
        logger: Log, add_space_sequence_1: bool = False,
        pairing_percent: int = 30
):
    """

    :param arn1: arn1
    :param arn2: arn2
    :param logger: logger
    :param add_space_sequence_1: if True, add space to sequence 1 else add space sequence 2
    :param pairing_percent: the pairing percent accepted
    """
    copy_sequence_1 = arn1.get_sequence_str()
    copy_sequence_2 = arn2.get_sequence_str()

    original_size_sequence_1 = len(copy_sequence_1)
    original_size_sequence_2 = len(copy_sequence_2)

    min_size_sequence = original_size_sequence_2
    if original_size_sequence_2 > original_size_sequence_1:
        min_size_sequence = original_size_sequence_1

    for j in range(0, original_size_sequence_1):
        if j > 0:
            if add_space_sequence_1:
                copy_sequence_1 = " " + copy_sequence_1
            else:
                copy_sequence_2 = " " + copy_sequence_2

        size_sequence_1 = len(copy_sequence_1)
        size_sequence_2 = len(copy_sequence_2)

        nb_pair = 0
        for i in range(0, size_sequence_2):
            if size_sequence_1 != size_sequence_2 and \
                    (i + 1 == size_sequence_1 or i + 1 == size_sequence_2):
                break
            if can_pair(copy_sequence_1[i], copy_sequence_2[i]):
                # logger.warning(f'{copy_sequence_1:26} | {copy_sequence_2:26} ===> '
                #                f'Error: {"Bad value":30} =>'
                #                f'sequence val 1 : {copy_sequence_1[i]:1} vs '
                #                f'sequence val 2 : {copy_sequence_2[i]:1} ==> at position {i:10d}')
                nb_pair = nb_pair + 1

        percent = nb_pair / min_size_sequence * 100

        if percent > pairing_percent:
            logger.error(f'{copy_sequence_1:26} | {copy_sequence_2:26} | '
                         f'number imbricate {nb_pair:2d} : error {percent:1.02f}%')


def usage():
    help_text = """This script is used to compare sequence of nucleotides with complementary method
        
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
            Variable of percentage of pairing accepted. 
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
        --log_output
            Specify the path where the log file will be create.
            Example = --output=/tmp/log.txt
"""
    print(help_text)


if __name__ == "__main__":
    # execute only if run as a script
    PAIRING_PERCENT = 30
    SEQUENCE_1 = "UCGUACCGUGAGUAAUAAUGCGB"
    SEQUENCE_2 = "UAACACUGUCUGGUAACGAUGQ"
    # jf true so it will add space before sequence 2
    # If False so it will add space before sequence 1
    ADD_SPACE_SEQUENCE_1 = True
    PATH_LOG = ""
    IS_VERBOSE = False
    ESTIMATE = False

    try:
        opts, argv = getopt.getopt(
            sys.argv[1:],
            "h",
            [
                'help', 'decalSeq1', 'verbose',
                'sequence1=', 'sequence2=', 'percent=', 'log_output=']
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
            PAIRING_PERCENT = v
        if k == '--log_output':
            PATH_LOG = v
        if k == '--decalSeq1':
            ADD_SPACE_SEQUENCE_1 = False
        if k == '--verbose':
            IS_VERBOSE = True

    if len(SEQUENCE_1) > 30 or len(SEQUENCE_2) > 30:
        print("Error: Arn sequences max size is 30")
        exit(1)

    logger = log.Log(None, IS_VERBOSE, PATH_LOG)
    arn1 = Arn(SEQUENCE_1)
    arn2 = Arn(SEQUENCE_2)

    dateDebut = datetime.now()
    logger.debug("date start : " + str(dateDebut))
    logger.debug("-------------------------------------")
    logger.debug("Check sequences with linear method Start.")
    compare_complementary_arn(arn1, arn2, logger, ADD_SPACE_SEQUENCE_1, PAIRING_PERCENT)
    logger.debug("Check sequences with linear method End.")
    logger.debug("-------------------------------------")
    logger.debug("date end : " + str(datetime.now()))
    logger.debug("process time : " + str(datetime.now() - dateDebut))

