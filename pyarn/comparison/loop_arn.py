import datetime
import getopt
import itertools
import multiprocessing
import os
import sys

val = os.path.dirname(sys.path[0])
sys.path.append(str(val).split("pyarn")[0])

from pyarn.log import log
from pyarn.models.arn import Arn, arn_to_str
from pyarn.models.nucleotide import can_pair


def compare_loop_one_arn(
        arn1: Arn, arn2: Arn,
        logger: log.Log = None, error_percent: int = 30
):
    """

    :param arn1: arn1
    :param arn2: arn2
    :param logger: logger
    :param error_percent:
    """
    sequence1 = arn1.get_list_nucleotides()
    sequence2 = arn2.get_list_nucleotides()

    size_sequence1 = len(sequence1)
    size_sequence2 = len(sequence2)

    min_size_sequence = size_sequence2
    if size_sequence2 > size_sequence1:
        min_size_sequence = size_sequence1

    return _compare_loop_arn_sequence_(sequence1, sequence2, min_size_sequence, logger, error_percent)


def compare_loop_arn_multiple(
        arn1: Arn, arn2: Arn,
        logger: log.Log, error_percent: int = 30,
        nb_process=1
):
    """

    :param arn1: arn1
    :param arn2: arn2
    :param logger: logger
    :param error_percent:
    :param nb_process: number of process will be use for this programm
    """
    copy_sequence_1 = arn1.get_list_nucleotides()
    copy_sequence_2 = arn2.get_list_nucleotides()

    size_sequence1 = len(copy_sequence_1)
    size_sequence2 = len(copy_sequence_2)

    min_size_sequence = size_sequence2
    if size_sequence2 > size_sequence1:
        min_size_sequence = size_sequence1

    if nb_process == 1:
        for sequence1 in __permutations__(copy_sequence_1):
            exclude_begin = None
            for sequence2 in __permutations__(copy_sequence_2):
                sequence2_str = arn_to_str(sequence2)
                if exclude_begin is not None and sequence2_str.startswith(exclude_begin):
                    continue
                s = _compare_loop_arn_sequence_(
                    sequence1, sequence2,
                    min_size_sequence, logger, error_percent
                )
                if s["begin_break_loop"] != "":
                    exclude_begin = s["begin_break_loop"]
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
    seq1_str = arn_to_str(sequence1)
    seq2_str = arn_to_str(sequence2)

    nb_imbricate = 0
    can_loop = True
    seq_1_position_history = []
    seq_2_position_history = []
    begin_break_loop = ""
    for i in range(0, min_size_sequence):
        seq_2_position_history.append(sequence2[i].original_position)
        seq_1_position_history.append(sequence1[i].original_position)
        if can_pair(sequence1[i].value, sequence2[i].value):
            if max(seq_2_position_history) > sequence2[i].original_position or \
                    max(seq_1_position_history) > sequence1[i].original_position:
                nb_imbricate = 0
                can_loop = False
                begin_break_loop = seq2_str[0:max(seq_2_position_history)]
                break
            nb_imbricate = nb_imbricate + 1

    data = {
        "arn1": seq1_str,
        "arn2": seq2_str,
        "can_loop": can_loop,
        "percent_pair": error_percent,
        "begin_break_loop": begin_break_loop
    }
    if can_loop is True:
        percent = nb_imbricate / min_size_sequence * 100
        if percent > error_percent:
            message = f'{seq1_str:26} | {seq2_str:26} | number imbricate {nb_imbricate:2d} : pair {percent:1.02f}%'
            if logger is not None:
                logger.warning(message)
            data["info_pair"] = [message]
    return data


def __permutations__(list_to_permute: list):
    return itertools.permutations(list_to_permute, len(list_to_permute))


def usage():
    help_text = """This script is used to compare sequence of nucleotides
        
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
            Variable of percentage of accepted comparison. 
            Only used for the line comparison
            Example = --percent=50
            Default value is : 30
        --verbose
            If provided : it will print in standard output logs.
            If not : it will not print logs.
            Example = --verbose
        --all_permutations
            If provided : it will generate all permutations possible and compare loop.
            If not : juste compare two arn provided
            WARNING! ALPHA VERSION => It can be dangerous for your server to use this argument because can do memory leak.
            Example = --all_permutations
        --log_output
            Specify the path where the log file will be create.
            Example = --output=/tmp/log.txt
        --nbProcess
            Specify the number of process used for treatment which need processing long time.
            Default : 1
            Example = --nbProcess=2
"""
    print(help_text)


if __name__ == "__main__":
    # execute only if run as a script
    ERROR_PERCENT = 30
    SEQUENCE_1 = "UCGUACCGUGAGUAAUAAUGCG"
    SEQUENCE_2 = "UAACACUGUCUGGUAACGAUGU"
    # jf true so it will add space before sequence 2
    # If False so it will add space before sequence 1
    PATH_LOG = ""
    IS_VERBOSE = False
    NB_PROCESS = 1
    ALL_PERMUTATIONS = False

    try:
        opts, argv = getopt.getopt(
            sys.argv[1:],
            "h",
            [
                'help', 'verbose', 'all_permutations',
                'sequence1=', 'sequence2=', 'percent=', 'log_output=', 'nbProcess=']
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
            ERROR_PERCENT = int(v)
        if k == '--log_output':
            PATH_LOG = v
        if k == '--verbose':
            IS_VERBOSE = True
        if k == '--all_permutations':
            ALL_PERMUTATIONS = True
        if k == '--nbProcess':
            NB_PROCESS = int(v)

    logger = log.Log(None, IS_VERBOSE, PATH_LOG)
    arn1 = Arn(SEQUENCE_1)
    arn2 = Arn(SEQUENCE_2)

    dateDebut = datetime.datetime.now()

    logger.debug("-------------------------------------")
    logger.debug("Check sequences Loop Method Start.")
    if ALL_PERMUTATIONS:
        compare_loop_arn_multiple(arn1, arn2, logger, ERROR_PERCENT, NB_PROCESS)
    else:
        data = compare_loop_one_arn(arn1, arn2, logger, ERROR_PERCENT)
        logger.info(data['arn1'])
        logger.info(data['arn2'])
        logger.info(data['can_loop'])
        if data.get("info_pair") :
            logger.info(data['info_pair'])
        logger.info(data['percent_pair'])
    logger.debug("Check sequences Loop Method End.")
    logger.debug("-------------------------------------")

    print(dateDebut)
    print(datetime.datetime.now())
