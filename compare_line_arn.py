import log
import getopt
import sys

from nucleotide import is_can_be_imbriquate
from arn import Arn
from log import Log


def compare_line_arn(
        arn1: Arn, arn2: Arn,
        logger: Log, add_space_sequence_1: bool = False,
        error_percent: int = 30
):
    """

    :param arn1:
    :param arn2:
    :param logger:
    :param add_space_sequence_1:
    :param error_percent:
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

        nb_error_imbricate = 0
        for i in range(0, size_sequence_2):
            if size_sequence_1 != size_sequence_2 and \
                    (i + 1 == size_sequence_1 or i + 1 == size_sequence_2):
                break
            if is_can_be_imbriquate(copy_sequence_1[i], copy_sequence_2[i]):
                # logger.warning(f'{copy_sequence_1:26} | {copy_sequence_2:26} ===> '
                #                f'Error: {"Bad value":30} =>'
                #                f'sequence val 1 : {copy_sequence_1[i]:1} vs '
                #                f'sequence val 2 : {copy_sequence_2[i]:1} ==> at position {i:10d}')
                nb_error_imbricate = nb_error_imbricate + 1

        percent = nb_error_imbricate / min_size_sequence * 100

        if percent > error_percent:
            logger.error(f'{copy_sequence_1:26} | {copy_sequence_2:26} ===> '
                         f'number imbricate {nb_error_imbricate:2d} : error {percent:1.02f}%')


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
            Warning. The output file can be huge. At least 60GB
            Example = --output=/tmp/resultFile.txt
"""
    print(help_text)


if __name__ == "__main__":
    # execute only if run as a script
    ERROR_PERCENT = 30
    SEQUENCE_1 = "UCGUACCGUGAGUAAUAAUGCGB"
    SEQUENCE_2 = "UAACACUGUCUGGUAACGAUGQ"
    # jf true so it will add space before sequence 2
    # If False so it will add space before sequence 1
    ADD_SPACE_SEQUENCE_1 = True
    FILENAME_OUTPUT = ""
    IS_VERBOSE = False

    try:
        opts, argv = getopt.getopt(
            sys.argv[1:],
            "h",
            [
                'help', 'decalSeq1', 'verbose',
                'sequence1=', 'sequence2=', 'percent=', 'output=']
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
        if k == '--decalSeq1':
            ADD_SPACE_SEQUENCE_1 = False
        if k == '--verbose':
            IS_VERBOSE = True

    if len(SEQUENCE_1) > 30 or len(SEQUENCE_2) > 30:
        print("Arn sequences max size is 30")
        exit(1)

    logger = log.Log(None, IS_VERBOSE, FILENAME_OUTPUT)
    arn1 = Arn(SEQUENCE_1)
    arn2 = Arn(SEQUENCE_2)

    logger.debug("-------------------------------------")
    logger.debug("Check sequences with linear method Start.")
    compare_line_arn(arn1, arn2, logger, ADD_SPACE_SEQUENCE_1, ERROR_PERCENT)
    logger.debug("Check sequences with linear method End.")
    logger.debug("-------------------------------------")

