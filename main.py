import datetime
import getopt
import sys

import log
from arn import Arn
from compare_arn import compare_loop_arn


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
    ADD_SPACE_SEQUENCE_1 = True
    FILENAME_OUTPUT = ""
    IS_VERBOSE = False
    NB_PROCESS = 1

    try:
        opts, argv = getopt.getopt(
            sys.argv[1:],
            "h",
            [
                'help', 'decalSeq1', 'verbose',
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
        if k == '--decalSeq1':
            ADD_SPACE_SEQUENCE_1 = False
        if k == '--verbose':
            IS_VERBOSE = True
        if k == '--nbProcess':
            NB_PROCESS = int(v)

    if len(SEQUENCE_1) > 30 or len(SEQUENCE_2) > 30:
        print("Arn sequences max size is 26")
        exit(1)

    logger = log.Log(None, IS_VERBOSE, FILENAME_OUTPUT)
    arn1 = Arn(SEQUENCE_1)
    arn2 = Arn(SEQUENCE_2)

    dateDebut = datetime.datetime.now()

    # logger.debug("-------------------------------------")
    # logger.debug("Check sequences Start.")
    # compare_strict_arn(arn1, arn2, logger)
    # logger.debug("Check sequences End.")
    # logger.debug("-------------------------------------")

    # logger.debug("-------------------------------------")
    # logger.debug("Check sequences with linear method Start.")
    # compare_line_arn(arn1, arn2, logger, ADD_SPACE_SEQUENCE_1, ERROR_PERCENT)
    # logger.debug("Check sequences with linear method End.")
    # logger.debug("-------------------------------------")

    logger.debug("-------------------------------------")
    logger.debug("Check sequences Loop Method Start.")
    compare_loop_arn(arn1, arn2, logger, ERROR_PERCENT, NB_PROCESS)
    logger.debug("Check sequences Loop Method End.")
    logger.debug("-------------------------------------")

    print(dateDebut)
    print(datetime.datetime.now())
