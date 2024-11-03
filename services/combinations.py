import numpy as np

class Combinations():
    def __init__(self, entry):
        self.entry = entry
    
    def add_all_vertical(self):
        results = [''.join(secuence[i] for secuence in self.entry) for i in range(6)]
        return results
    
    def add_all_diagonals(self):
        matrix = np.array([list(row) for row in self.entry])
        diagonal_normal = [''.join(matrix.diagonal(i)) for i in range(-2, 3)]
        anti_diagonal = [''.join(np.fliplr(matrix).diagonal(i)) for i in range(-2, 3)]

        diagonals = diagonal_normal + anti_diagonal
        return diagonals
    
    def get_all_combinatios(self):
        verticals = self.add_all_vertical()
        diagonals = self.add_all_diagonals()
        
        results = verticals + diagonals
        return results
