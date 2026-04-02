from .AbstractInput import AbstractInput, unpack_query_match


class CausalInput(AbstractInput):
    def __init__(self):
        pass

    def generate(self, query_tuple):
        prefix, _suffix, middle = unpack_query_match(query_tuple)

        return prefix, middle
