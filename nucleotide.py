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


def is_can_be_imbriquate(val1: str, val2: str):
    """

    :param val1:
    :param val2:
    :return:
    """
    if val1 == "A" and val2 == "U":
        is_imbricate = True
    elif val1 == "C" and val2 == "G":
        is_imbricate = True
    else:
        is_imbricate = False
    return is_imbricate


