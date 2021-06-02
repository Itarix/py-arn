from arn import Arn
from log import format_error, Log


def compare_strict_arn(arn1:Arn, arn2:Arn, logger:Log):
    logger.debug("-------------------------------------")
    logger.debug("Check sequences Start.")

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
    logger.debug("Check sequences End.")
    logger.debug("-------------------------------------")

def compare_line_arn(arn1:Arn, arn2:Arn, logger:Log, add_space_sequence_1:bool=False, error_percent:int=30):
    logger.debug("-------------------------------------")
    logger.debug("Check sequences with linear method Start.")

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

    logger.debug("Check sequences with linear method End.")
    logger.debug("-------------------------------------")

def is_can_be_imbriquate(val1, val2):
    if val1 == "A" and val2 == "U":
        is_imbricate = True
    elif val1 == "C" and val2 == "G":
        is_imbricate = True
    else:
        is_imbricate = False
    return is_imbricate
