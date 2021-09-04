"""arn module for arn class."""

from . import nucleotide


class Arn:
    """
        Class Arn
    """

    def __init__(self, sequence: str) -> object:
        """

        :param sequence:
        """
        self.sequence_arn_str = sequence

        tmp = []
        for position, val in enumerate(self.sequence_arn_str):
            tmp.append(nucleotide.Nucleotide(position, val))
        self.sequence_arn_list = tmp

    def get_size(self) -> int:
        """

        :return: int
        """
        return len(self.sequence_arn_str)

    def get_list_nucleotides(self) -> list:
        """

        :return:
        """
        return self.sequence_arn_list

    def get_sequence_str(self) -> str:
        """

        :return:
        """
        return self.sequence_arn_str


def arn_to_str(sequence: list) -> str:
    """

    :param sequence:
    :rtype: object
    """
    tmp = ""
    for i in sequence:
        tmp = tmp + i.value
    return tmp


def arn_to_str_with_position(sequence: list) -> str:
    """

    :param sequence:
    :rtype: object
    """
    tmp = ""
    for position, val in enumerate(sequence):
        tmp = tmp + val + str(position)
    return tmp
