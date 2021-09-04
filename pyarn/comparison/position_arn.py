import getopt
import os
import sys
from datetime import datetime

val = os.path.dirname(sys.path[0])
sys.path.append(str(val).split("pyarn")[0])
from pyarn.log import log
from pyarn.models.arn import Arn


def compare_position_arn(arn1: Arn, arn2: Arn, logger: log.Log = None) -> dict:
    """

    :rtype: int
    """
    sequence_1 = arn1.get_sequence_str()
    sequence_2 = arn2.get_sequence_str()

    size_sequence_1 = len(sequence_1)
    size_sequence_2 = len(sequence_2)

    data_bad_sizes = []
    data_bad_values = []
    nb_mismatch: int = 0
    for i in range(0, size_sequence_1):
        if size_sequence_1 != size_sequence_2 and (i in (size_sequence_1, size_sequence_2)):
            message = f'Nucleotide from Arn 1: {sequence_1[i]:1} vs Nucleotide from Arn 2 : {" ":1} ==> at position {i:10d}'
            if logger is not None:
                logger.warning(message)
            data_bad_sizes.append(message)
            nb_mismatch += 1
            break

        if sequence_1[i] != sequence_2[i]:
            message = f'Nucleotide from Arn 1 : {sequence_1[i]:1} vs Nucleotide from Arn 2 : {sequence_2[i]:1} ==> at position {i:10d}'
            if logger is not None:
                logger.warning(message)
            data_bad_values.append(message)
            nb_mismatch += 1

    data = {
        "arn1": sequence_1,
        "size_arn1": size_sequence_1,
        "size_arn2": size_sequence_2,
        "arn2": sequence_2,
        "bad_sizes": data_bad_sizes,
        "bad_values": data_bad_values,
        "nb_mismatch": nb_mismatch
    }
    return data


def usage():
    help_text = """This script is used to compare positions of two arns
        
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
        --log_output
            Specify the path where the log file will be create.
            Example = --output=/tmp/log.txt
"""
    print(help_text)


if __name__ == "__main__":
    # execute only if run as a script
    SEQUENCE_1 = "UCGUACCGUGAGUAAUAAUGCGB"
    SEQUENCE_2 = "UAACACUGUCUGGUAACGAUGQ"
    # jf true so it will add space before sequence 2
    # If False so it will add space before sequence 1
    PATH_LOG = ""
    IS_VERBOSE = False

    try:
        opts, argv = getopt.getopt(
            sys.argv[1:],
            "h",
            [
                'help', 'verbose',
                'sequence1=', 'sequence2=', 'log_output=']
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
        if k == '--log_output':
            PATH_LOG = v
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
    logger.debug("Check sequences Start.")
    data = compare_position_arn(arn1, arn2)
    logger.info(data['arn1'])
    logger.info(data['arn2'])
    logger.info(data['bad_sizes'])
    logger.info(data['bad_values'])
    logger.info(data['nb_mismatch'])
    logger.debug("Check sequences End.")
    logger.debug("-------------------------------------")
    logger.debug("date end : " + str(datetime.now()))
    logger.debug("process time : " + str(datetime.now() - dateDebut))
