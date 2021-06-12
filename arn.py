import nucleotide


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
        for i in range(0, len(self.sequence_arn_str)):
            tmp.append(nucleotide.Nucleotide(i, self.sequence_arn_str[i]))
        self.sequence_arn_list = tmp

    def get_sequence_list(self) -> list:
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
    for i in range(0, len(sequence)):
        tmp = tmp + sequence[i].value
    return tmp
