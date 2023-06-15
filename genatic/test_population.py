import unittest
import population

class TestPop(unittest.TestCase):
    # check if the population exists
    def testPopExists(self):
        pop = population.Population(pop_size = 10, gene_count=4)
        self.assertIsNotNone(pop)

    # check if the population has individuals 
    def testPopHasIndes(self):
        pop = population.Population(pop_size = 10, gene_count=4)
        self.assertEqual(len(pop.creatures),10)

unittest.main()