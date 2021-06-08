class Nucleotide:
    def __init__(self, position: int, value: str):
        self.original_position = position
        self.value = value

    def __repr__(self):
        return self.value + str(self.original_position)
