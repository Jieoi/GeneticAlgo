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

    # test the calculation of the fitness map
    def testFitmap(self):
        fits = [2.5, 1.2, 3.4]
        want = [2.5, 3.7, 7.1]
        fitmap = population.Population.get_fitness_map(fits)
        self.assertEqual(fitmap, want)

    # test if the parents selected is less than total
    def testSalPar(self):
        fits = [2.5, 1.2, 3.4]
        fitmap = population.Population.get_fitness_map(fits)
        pid = population.Population.select_parent(fitmap)
        self.assertLess(pid,3)
    
    def testSalPar2(self):
        fits = [0,1000,0.1]
        fitmap = population.Population.get_fitness_map(fits)
        pid = population.Population.select_parent(fitmap)
        self.assertEqual(pid, 1) # unlikely to be in the other range
        
unittest.main()