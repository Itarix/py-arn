class Nucleotide:
    """
        Class Nucleotide
    """

    def __init__(self, position: int, value: str):
        """

        :rtype: object
        """
        self.original_position = position
        self.value = value

    def __repr__(self):
        return self.value + str(self.original_position)


def can_pair(val1: str, val2: str):
    """

    :param val1:
    :param val2:
    :return:
    """
    if val1 == "A" and val2 == "U":
        is_pair = True
    elif val1 == "C" and val2 == "G":
        is_pair = True
    else:
        is_pair = False
    return is_pair


