from .AbstractInput import AbstractInput, unpack_query_match


class FIMInput(AbstractInput):
    def __init__(self, FIM_PREFIX, FIM_SUFFIX, FIM_MIDDLE):
        self.FIM_PREFIX = FIM_PREFIX
        self.FIM_SUFFIX = FIM_SUFFIX
        self.FIM_MIDDLE = FIM_MIDDLE

    def generate(self, query_tuple):
        prefix, suffix, middle = unpack_query_match(query_tuple)
        
        text = self.FIM_PREFIX + prefix + self.FIM_SUFFIX + suffix + self.FIM_MIDDLE
        return text, middle
