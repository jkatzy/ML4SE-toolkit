'''
Iterable dataset that generates samples based on a query.
'''
class IterableQueryLoader(torch.utils.data.IterableDataset):
    def __init__(self, source_dataset, query, max_samples):
        super(IterableQueryLoader).__init__()
        self.source_dataset = source_dataset
        self.query = query
        self.max_samples = max_samples

        self.iterator = iter(self.source_dataset)

        self.i = 0
   
    def __iter__(self):
        return self

    def __next__(self):
        if self.i <= self.max_samples:

            returnable = None
            while returnable == None:
                file = next(self.iterator)
                returnable = self.process(file, self.query)

            self.i += 1
            return returnable
        else:
            raise StopIteration

    def __len__(self):
        return len(self.source_dataset) - self.i

    def process(self, file, query):
        pass
