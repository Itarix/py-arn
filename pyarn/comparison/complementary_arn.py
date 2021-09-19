import getopt
import os
import sys
from datetime import datetime

val = os.path.dirname(sys.path[0])
sys.path.append(str(val).split("pyarn")[0])

from pyarn.log import log
from pyarn.models.arn import Arn
from pyarn.models.nucleotide import can_pair


def compare_complementary_arn(
        arn1: Arn, arn2: Arn,
        logger: log.Log = None, add_space_sequence_1: bool = False,
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

    info_percent_pair_all = []
    info_can_pair_all = []
    for j in range(0, original_size_sequence_1):
        if j > 0:
            if add_space_sequence_1:
                copy_sequence_1 = " " + copy_sequence_1
            else:
                copy_sequence_2 = " " + copy_sequence_2

        size_sequence_1 = len(copy_sequence_1)
        size_sequence_2 = len(copy_sequence_2)

        tmp_sequence_1 = copy_sequence_1.replace(" ", "-")
        tmp_sequence_2 = copy_sequence_2.replace(" ", "-")
        nb_pair = 0
        for i in range(0, size_sequence_2):
            if size_sequence_1 != size_sequence_2 and \
                    (i == size_sequence_1 or i == size_sequence_2):
                break
            if can_pair(copy_sequence_1[i], copy_sequence_2[i]):
                message = f'{tmp_sequence_1:26} | {tmp_sequence_2:26} ===> Nucleotide 1 : {copy_sequence_1[i]:1} can pair with Nucleotide 2 : {copy_sequence_2[i]:1} ==> at position {i:10d}'
                if logger is not None:
                    logger.warning(message)
                info_can_pair_all.append(message)
                nb_pair = nb_pair + 1

        percent = nb_pair / min_size_sequence * 100

        if percent > pairing_percent:
            message = f'{tmp_sequence_1:26} | {tmp_sequence_2:26} | number imbricate {nb_pair:2d} : pair {percent:1.02f}%'
            if logger is not None:
                logger.warning(message)
            info_percent_pair_all.append(message)

    data = {
        "arn1": copy_sequence_1,
        "arn2": copy_sequence_2,
        "percent_pair": pairing_percent,
        "add_space_sequence_1": add_space_sequence_1,
        "add_space_sequence_2": not add_space_sequence_1,
        "info_percent_pairing": info_percent_pair_all,
        "info_can_pair": info_can_pair_all
    }
    return data


def usage():
    help_text = """This script is used to compare sequence of nucleotides with complementary method
        
        This script accept parameters of this list. 
        
        --help (shortcut: -h)
            Show the way how use the script
        --sequence1
            First Sequence to be compare.
            Example = --sequence1=UCGA
            Default value is : UCGUACCGUGAGUAAUAAUGCG
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
    SEQUENCE_1 = "UCGUACCGUGAGUAAUAAUGCG"
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
            PAIRING_PERCENT = int(v)
        if k == '--log_output':
            PATH_LOG = v
        if k == '--decalSeq1':
            ADD_SPACE_SEQUENCE_1 = False
        if k == '--verbose':
            IS_VERBOSE = True

    logger = log.Log(None, IS_VERBOSE, PATH_LOG)
    arn1 = Arn(SEQUENCE_1)
    arn2 = Arn(SEQUENCE_2)

    dateDebut = datetime.now()
    logger.debug("date start : " + str(dateDebut))
    logger.debug("-------------------------------------")
    logger.debug("Check sequences with complementary method Start.")
    data = compare_complementary_arn(arn1, arn2, logger, ADD_SPACE_SEQUENCE_1, PAIRING_PERCENT)
    logger.info(data['arn1'])
    logger.info(data['arn2'])
    logger.info(data['percent_pair'])
    logger.info(data['add_space_sequence_1'])
    logger.info(data['add_space_sequence_2'])
    logger.info(data['info_percent_pairing'])
    logger.info(data['info_can_pair'])
    logger.debug("Check sequences with linear method End.")
    logger.debug("-------------------------------------")
    logger.debug("date end : " + str(datetime.now()))
    logger.debug("process time : " + str(datetime.now() - dateDebut))
