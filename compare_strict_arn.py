import getopt
import sys
import log
from arn import Arn
from log import Log


def compare_strict_arn(arn1: Arn, arn2: Arn, logger: Log):
    """

    :rtype: object
    """
    sequence_1 = arn1.get_sequence_str()
    sequence_2 = arn2.get_sequence_str()

    size_sequence_1 = len(sequence_1)
    size_sequence_2 = len(sequence_2)

    nb_error: int = 0
    for i in range(0, size_sequence_1):
        if size_sequence_1 != size_sequence_2 and (i in (size_sequence_1, size_sequence_2)):
            # logger.warning(f'{sequence_1:26} | {sequence_2:26} ===> '
            #                f'Error: {"Bad size sequences":30} => '
            #                f'sequence val 1 : {sequence_1[i]:1} vs '
            #                f'sequence val 2 : {" ":1} ==> at position {i:10d}')
            nb_error += 1
            break

        if sequence_1[i] != sequence_2[i]:
            # logger.warning(f'{sequence_1:26} | {sequence_2:26} ===> '
            #                f'Error: {"Bad value":30} =>'
            #                f'sequence val 1 : {sequence_1[i]:1} vs '
            #                f'sequence val 2 : {sequence_2[i]:1} ==> at position {i:10d}')
            nb_error += 1

    if nb_error > 0:
        logger.warning(f'{sequence_1:26} | {sequence_2:26} ===> '
                       f'Number of errors while analyse sequences => nb error {nb_error:2d}')


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
    SEQUENCE_1 = "UCGUACCGUGAGUAAUAAUGCGB"
    SEQUENCE_2 = "UAACACUGUCUGGUAACGAUGQ"
    # jf true so it will add space before sequence 2
    # If False so it will add space before sequence 1
    FILENAME_OUTPUT = ""
    IS_VERBOSE = False

    try:
        opts, argv = getopt.getopt(
            sys.argv[1:],
            "h",
            [
                'help', 'verbose',
                'sequence1=', 'sequence2=', 'output=']
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
        if k == '--output':
            FILENAME_OUTPUT = v
        if k == '--verbose':
            IS_VERBOSE = True

    if len(SEQUENCE_1) > 30 or len(SEQUENCE_2) > 30:
        print("Arn sequences max size is 30")
        exit(1)

    logger = log.Log(None, IS_VERBOSE, FILENAME_OUTPUT)
    arn1 = Arn(SEQUENCE_1)
    arn2 = Arn(SEQUENCE_2)

    logger.debug("-------------------------------------")
    logger.debug("Check sequences Start.")
    compare_strict_arn(arn1, arn2, logger)
    logger.debug("Check sequences End.")
    logger.debug("-------------------------------------")
