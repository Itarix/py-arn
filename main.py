import getopt, sys

import log
from arn import Arn
from compare_arn import compare_strict_arn, compare_line_arn


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
            Example = --output=/tmp/resultFile.txt
"""
    print(help_text)


if __name__ == "__main__":
    # execute only if run as a script
    error_percent = 30
    sequence_1 = "UCGUACCGUGAGUAAUAAUGCGB"
    sequence_2 = "UAACACUGUCUGGUAACGAUGQ"
    # jf true so it will add space before sequence 2
    # If False so it will add space before sequence 1
    add_space_sequence1 = True
    filename_output = None
    is_verbose = False

    try:
        opts, argv = getopt.getopt(
            sys.argv[1:],
            "h",
            ['help', 'sequence1=', 'sequence2=', 'percent=', 'output=', 'decalSeq2', 'verbose']
        )
    except getopt.GetoptError as err:
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

    logger = log.Log(filename_output, is_verbose)

    arn1 = Arn(sequence_1)
    arn2 = Arn(sequence_2)

    compare_strict_arn(arn1, arn2, logger)
    compare_line_arn(arn1, arn2, logger, add_space_sequence1, error_percent)
