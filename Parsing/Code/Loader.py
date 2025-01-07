import torch
from Parsing.Code.TreeQuery import getQuery, getQueryString
from Parsing.Code.LanguageParser import getLanguage, getParser
class IterableQueryLoader(torch.utils.data.IterableDataset):
    def __init__(self, hf_dataset, query_name, max_samples, max_length, lang, model):
        super(IterableQueryLoader).__init__()
        self.hf_dataset = hf_dataset
        self.model = model
        self.lang = lang
        self.max_length = max_length
        self.query_name = query_name
        self.max_samples = max_samples

        if query_name != 'noise':
            self.query = getQuery(query_name, self.lang)

    def __iter__(self):
        i = 0
        if self.query_name == 'noise':
            while i < self.max_samples:
                returnable = self.process(None)
                i += 1
                yield returnable, self.query_name
        else:
            iterator = iter(self.hf_dataset)
            while i < self.max_samples:
                try:
                    file = next(iterator)
                except StopIteration:
                    iterator = iter(self.hf_dataset)
                    file = next(iterator)
                try:
                    returnable = self.process(file)
                    i += 1
                    yield returnable, self.query_name
                except ValueError:
                    continue

    def __len__(self):
        return len(self.hf_dataset)

    def process(self, sample):
        if self.query_name == 'noise':
            return self.gen_noise()
        elif "gpt" in self.model.lower():
            return self.gen_subsample_gpt(sample['content'])
        else:
            raise ValueError

    def gen_noise(self):
        noise = torch.randint(0, 100, (self.max_length,))
        sample = {'input': {'input_ids': noise, 'attention_mask': torch.ones_like(noise)}}
        return sample

    def gen_subsample_gpt(self, content):
        return {"content": content}


class IterableScenarioLoader(torch.utils.data.IterableDataset):
    def __init__(self, hf_dataset, query_name, max_samples, max_length, lang, model, min_length=16):
        super(IterableScenarioLoader).__init__()
        self.hf_dataset = hf_dataset
        self.model = model
        self.lang = lang
        self.max_length = max_length
        self.min_length = min_length
        self.query_name = query_name
        self.max_samples = max_samples

        if query_name != "random" and 'starcoder' in self.model:
            self.query = getLanguage(self.lang).query(getQueryString(self.lang, query_name))
            self.parser = getParser(self.lang)

    def __iter__(self):
        i = 0
        iterator = iter(self.hf_dataset)
        while i < self.max_samples:
            try:
                file = next(iterator)
            except StopIteration:
                iterator = iter(self.hf_dataset)
                file = next(iterator)
            try:
                returnable = self.process(file)
                i += 1
                yield returnable, self.query_name
            except ValueError:
                continue

    def __len__(self):
        return len(self.hf_dataset)

    def process(self, sample):
        if "starcoder" in self.model.lower():
            return {"content": sample['content']}
        elif "gpt" in self.model.lower():
            return {"content": sample['content']}
        else:
            raise ValueError
