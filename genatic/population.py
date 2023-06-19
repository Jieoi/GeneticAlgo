import creature
import numpy as np

class Population():
    def __init__(self, pop_size, gene_count):
        self.creatures = [creature.Creature(gene_count=gene_count) for i in range(pop_size)]

    # Roulette wheel selection of the creatures for next genertion
    # generate a float between 0 and 1, works out which 
    # interval it's in and selects the appropriate parent
    @staticmethod
    def get_fitness_map(fits):
        fitmap = []
        total = 0
        for f in fits:
            total = total + f
            fitmap.append(total)
        return fitmap

    # Select the parents for roulette wheel
    @staticmethod
    def select_parent(fitmap):
        # create random number
        r = np.random.rand() # 0-1
        r = r * fitmap[-1]
        for i in range(len(fitmap)):
            if r <= fitmap[i]:
                return i
