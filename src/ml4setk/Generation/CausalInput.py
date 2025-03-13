from .AbstractInput import AbstractInput

class CausalInput(AbstractInput):
    def __init__(self):
        pass

    def generate(self, query_tuple):
        prefix = query_tuple[0]
        suffix = query_tuple[1]
        middle = query_tuple[2]

        return prefix, middle
