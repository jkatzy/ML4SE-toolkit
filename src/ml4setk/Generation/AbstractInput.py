from abc import ABC, abstractmethod

class AbstractInput(ABC):

    '''
    Generates the input to give to a model, returns a tuple, (model_input, ground_truth)
    '''
    @abstractmethod
    def generate(self, prefix, suffix, middle):
        pass
