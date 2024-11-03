from typing import Type
from services.combinations import Combinations

class DnaTester():

    def __init__(self):
        self.dna = ["AAAA", "TTTT", "CCCC", "GGGG"]
    
    def isMutant(self, entry):
        print(entry)
        results = entry.copy()
        combination = Combinations(entry)
        results += combination.get_all_combinatios()

        mutants = list(filter(lambda x: any(substr in x for substr in self.dna), results))

        return True if len(mutants) > 0 else False

