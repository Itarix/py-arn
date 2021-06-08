import itertools
import multiprocessing
import os

import psutil as psutil

from arn import Arn, arn_to_str
from log import format_error, Log


def compare_strict_arn(arn1: Arn, arn2: Arn, logger: Log):
    sequence_1 = arn1.get_sequence_str()
    sequence_2 = arn2.get_sequence_str()

    size_sequence_1 = len(sequence_1)
    size_sequence_2 = len(sequence_2)

    nb_error = 0
    for i in range(0, size_sequence_1):
        if size_sequence_1 != size_sequence_2 and (i == size_sequence_1 or i == size_sequence_2):
            logger.warning(format_error("Bad size sequences", sequence_1[i], " ", i))
            nb_error = nb_error + 1
            break

        if sequence_1[i] != sequence_2[i]:
            logger.warning(format_error("Bad value", sequence_1[i], sequence_2[i], i))
            nb_error = nb_error + 1

    if nb_error > 0:
        logger.warning(f'Number of errors while analyse sequences =>  {nb_error:1d}')


def compare_line_arn(arn1: Arn, arn2: Arn, logger: Log, add_space_sequence_1: bool = False, error_percent: int = 30):
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
        logger.debug(f'Analyse => sequence 1 : {copy_sequence_1:1} vs sequence 2 : {copy_sequence_2:1}')
        for i in range(0, size_sequence_2):
            if size_sequence_1 != size_sequence_2 and (i + 1 == size_sequence_1 or i + 1 == size_sequence_2):
                logger.debug("end of sequences")
                break
            if is_can_be_imbriquate(copy_sequence_1[i], copy_sequence_2[i]):
                logger.warning(format_error("Can be imbricate", copy_sequence_1[i], copy_sequence_2[i], i))
                nb_error_imbricate = nb_error_imbricate + 1

        percent = nb_error_imbricate / min_size_sequence * 100
        logger.info(f'We have found : {nb_error_imbricate:1d} error. Percent {percent:1.02f}')
        if percent > error_percent:
            logger.error(f'Bad combination : {percent:1.02f}%')


def limit_cpu():
    "is called at every process start"
    p = psutil.Process(os.getpid())
    # set to lowest priority, this is windows only, on Unix use ps.nice(19)
    priority = 19
    if os.name == 'nt':
        priority = psutil.BELOW_NORMAL_PRIORITY_CLASS

    p.nice(priority)


def compare_loop_arn(arn1: Arn, arn2: Arn, logger: Log, error_percent: int = 30):
    copy_sequence_1 = arn1.get_sequence_list()
    copy_sequence_2 = arn2.get_sequence_list()

    size_sequence1 = len(copy_sequence_1)
    size_sequence2 = len(copy_sequence_1)

    min_size_sequence = size_sequence2
    if size_sequence2 > size_sequence1:
        min_size_sequence = size_sequence1

    p = multiprocessing.Pool(None, limit_cpu)
    for sequence1 in permutations(copy_sequence_1):
        print("ha")
        for sequence2 in permutations(copy_sequence_2):
            print("hoho")
            p.apply_async(__compare_loop_arn_sequence__, [sequence1, sequence2, min_size_sequence, logger, error_percent])

    p.close()
    p.join()


def __compare_loop_arn_sequence__(sequence1, sequence2, min_size_sequence, logger, error_percent):
    seq_1_position_history = []

    for k in range(0, len(sequence1)):
        seq_1_position_history.append(sequence1[k].original_position)
        nb_error_imbricate = 0
        seq_2_position_history = []
        for l in range(0, len(sequence2)):
            seq_2_position_history.append(sequence2[l].original_position)

            if is_can_be_imbriquate(sequence1[k].value, sequence2[l].value):
                if max(seq_2_position_history) > sequence2[l].original_position or \
                        max(seq_1_position_history) > sequence1[k].original_position:
                    return
                logger.debug(
                    f'Can be imbricate : {sequence1[k].value:1} at {k:1d} position ===> {sequence2[l].value:1} at {l:1d} position')
                nb_error_imbricate = nb_error_imbricate + 1

        percent = nb_error_imbricate / min_size_sequence * 100
        logger.debug(f'We have found : {nb_error_imbricate:1d} error. Percent {percent:1.02f}')

        if percent > error_percent:
            logger.debug(f'Bad combination : {percent:1.02f}%')


# def compare_loop_arn(arn1: Arn, arn2: Arn, logger: Log, error_percent: int = 30):
#     for seq_1 in permutations(copy_sequence_1):
#         for seq_2 in permutations(copy_sequence_2):
#     seq_1_position = []
#     loop_broken = False
#
#     for k in range(0, len(seq_1)):
#         seq_1_position.append(seq_1[k].original_position)
#         nb_error_imbricate = 0
#         seq_2_position = []
#         for l in range(0, len(seq_2)):
#             seq_2_position.append(seq_2[l].original_position)
#
#             if is_can_be_imbriquate(seq_1[k].value, seq_2[l].value):
#                 if max(seq_2_position) > seq_2[l].original_position or \
#                         max(seq_1_position) > seq_1[k].original_position:
#                     loop_broken = True
#                     break
#                 logger.debug(
#                     f'Can be imbricate : {seq_1[k].value:1} at {k:1d} position ===> {seq_2[l].value:1} at {l:1d} position')
#                 nb_error_imbricate = nb_error_imbricate + 1
#
#         if loop_broken:
#             break
#
#         percent = nb_error_imbricate / min_size_sequence * 100
#         logger.debug(f'We have found : {nb_error_imbricate:1d} error. Percent {percent:1.02f}')
#
#         if percent > error_percent:
#             logger.debug(f'Bad combination : {percent:1.02f}%')
#
#     if loop_broken:
#         logger.debug(f'Broken loop : Sequence 1 : {seq_1} ==> Sequence 2 : {seq_2}')
#         break


def is_can_be_imbriquate(val1: str, val2: str):
    if val1 == "A" and val2 == "U":
        is_imbricate = True
    elif val1 == "C" and val2 == "G":
        is_imbricate = True
    else:
        is_imbricate = False
    return is_imbricate


def permutations(list_to_permute: list):
    return itertools.permutations(list_to_permute, len(list_to_permute))
