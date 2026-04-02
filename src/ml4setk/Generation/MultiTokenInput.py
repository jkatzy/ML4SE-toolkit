from .AbstractInput import AbstractInput


class MultiTokenInput(AbstractInput):
    def __init__(self, tokenizer):
        self.tokenizer = tokenizer
    
    def generate(self, context, target):
        #List of integers, each integer is a token
        targets = self.tokenizer.encode(target)
        #List of integers, each integer is a token
        context_tokens = self.tokenizer.encode(context)
        
        model_inputs = []
        for t in targets:
            model_inputs.append((context_tokens.copy(), t))
            context_tokens.append(t)
        return model_inputs
