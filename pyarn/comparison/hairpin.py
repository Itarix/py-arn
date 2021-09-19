import getopt
import os
import sys
from datetime import datetime

from pyarn.models import nucleotide

val = os.path.dirname(sys.path[0])
sys.path.append(str(val).split("pyarn")[0])
from pyarn.log import log
from pyarn.models.arn import Arn


def calcul_hairpin(arn1: Arn, percent : int = 30, logger: log.Log = None) -> dict:
    """

    :rtype: int
    """
    sequence_1 = arn1.get_sequence_str()

    size_sequence_1 = len(sequence_1)

    infos_pair = []
    for i in range(0, size_sequence_1):

        # generate sub arn with last chars
        sub_arn1 = sequence_1[size_sequence_1 - i:]
        sub_arn1 = sub_arn1[::-1]

        # generate sub arn with firsts chars
        sub_arn2 = sequence_1[:size_sequence_1-i]
        nb_pair = 0

        for j in range(0, len(sub_arn1)):
            if len(sub_arn1) == 0 or len(sub_arn2) == 0:
                break

            size_arn1 = len(sub_arn1)
            tmp = size_arn1 - j

            position_sub_arn2 = len(sub_arn2)-tmp
            if position_sub_arn2 < 0:
                continue

            print("-------------")
            print(sub_arn1[j])
            print(sub_arn2[len(sub_arn2)-tmp])
            if nucleotide.can_pair(sub_arn1[j], sub_arn2[position_sub_arn2]):
                nb_pair = nb_pair + 1

        percent_pair = nb_pair / len(sub_arn2) * 100
        if percent_pair > percent:
            message = f'{sub_arn1:26} | {sub_arn2:26} | number pair {nb_pair:2d} : pair {percent_pair:1.02f}%'
            if logger is not None:
                logger.warning(message)

            if len(sub_arn1) < len(sub_arn2):
                for l in range(0, len(sub_arn2)):
                    if len(sub_arn1) >= len(sub_arn2):
                        break

                    sub_arn1 = "-" + sub_arn1

            dico_infos = {
                "sub_arn1": sub_arn1,
                "sub_arn2": sub_arn2,
                "nb_pair": f'{nb_pair:2d}',
                "percent_pair": f'{percent_pair:1.02f}',
            }
            infos_pair.append(dico_infos)

    data = {
        "arn1": sequence_1,
        "size_arn1": size_sequence_1,
        "percent_pair": percent,
        "info_percent_pairing": infos_pair,
    }
    return data


def usage():
    help_text = """This script is used to calcul hairpin of one arn
        
        This script accept parameters of this list. 
        
        --help (shortcut: -h)
            Show the way how use the script
        --sequence1
            First Sequence to be compare.
            Example = --sequence1=UCGA
            Default value is : UCGUACCGUGAGUAAUAAUGCG
        --verbose
            If provided ; it will print in standard output logs.
            If not : it will not print logs.
            Example = --verbose
        --percent
            Variable of percentage of accepted comparison. 
            Only used for the line comparison
            Example = --percent=50
            Default value is : 30
        --log_output
            Specify the path where the log file will be create.
            Example = --output=/tmp/log.txt
"""
    print(help_text)


if __name__ == "__main__":
    # execute only if run as a script
    SEQUENCE_1 = "UCGUACCGUGAGUAAUAAUGCG"
    # jf true so it will add space before sequence 2
    # If False so it will add space before sequence 1
    PATH_LOG = ""
    IS_VERBOSE = False
    PERCENT_PAIR = 30

    try:
        opts, argv = getopt.getopt(
            sys.argv[1:],
            "h",
            [
                'help', 'verbose', "percent=",
                'sequence1=', 'log_output=']
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
        if k == '--percent':
            PERCENT_PAIR = int(v)
        if k == '--log_output':
            PATH_LOG = v
        if k == '--verbose':
            IS_VERBOSE = True

    logger = log.Log(None, IS_VERBOSE, PATH_LOG)
    arn1 = Arn(SEQUENCE_1)

    dateDebut = datetime.now()

    logger.debug("date start : " + str(dateDebut))
    logger.debug("-------------------------------------")
    logger.debug("Check sequences Start.")
    data = calcul_hairpin(arn1, PERCENT_PAIR)
    logger.info(data['arn1'])
    logger.info(data['size_arn1'])
    logger.info(data['percent_pair'])
    logger.info(data['info_percent_pairing'])

    logger.debug("Check sequences End.")
    logger.debug("-------------------------------------")
    logger.debug("date end : " + str(datetime.now()))
    logger.debug("process time : " + str(datetime.now() - dateDebut))