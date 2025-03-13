from .AbstractInput import AbstractInput

class CausalInput(AbstractInput):
    def __init__(self):
        pass

    def generate(self, prefix, suffix, middle):
        return prefix, middle
