#overall test for the genetic algorithm

import unittest
import population as poplib
import simulation as simlib
import creature as crlib
import genome as gnlib
import creature

import numpy as np

class TestGA(unittest.TestCase):

    def testGA(self):
        # generate a random population with population class
        pop = poplib.Population(pop_size=10, gene_count=3)
        # evaluate the population using the simulation class
        # no multi threading
        sim = simlib.Simulation()

        # call run creature to test instead of eval_population
        for iteration in range(10):
            for cr in pop.creatures:
                sim.run_creature(cr, 2400)            
            fits = [cr.get_distance_travelled() 
                    for cr in pop.creatures]
            links = [len(cr.get_expanded_links()) 
                    for cr in pop.creatures]
            print(iteration, "fittest:", np.round(np.max(fits), 3), "mean:", np.round(np.mean(fits), 3), "mean links", np.round(np.mean(links)), "max links", np.round(np.max(links)))       
            fit_map = poplib.Population.get_fitness_map(fits)
            new_creatures = []
            for i in range(len(pop.creatures)):
                p1_ind = poplib.Population.select_parent(fit_map)
                p2_ind = poplib.Population.select_parent(fit_map)
                p1 = pop.creatures[p1_ind]
                p2 = pop.creatures[p2_ind]
                # now we have the parents!
                dna = gnlib.Genome.crossover(p1.dna, p2.dna)
                dna = gnlib.Genome.point_mutation(dna, rate=0.1, amount=0.25)
                # shrink than grow
                dna = gnlib.Genome.shrink_mutation(dna, rate=0.25)
                dna = gnlib.Genome.grow_mutation(dna, rate=0.1)
                cr = creature.Creature(1)
                cr.set_dna(dna)
                new_creatures.append(cr)
            # # elitism
            # max_fit = np.max(fits)
            # for cr in pop.creatures:
            #     if cr.get_distance_travelled() == max_fit:
            #         new_cr = creature.Creature(1)
            #         new_cr.update_dna(cr.dna)
            #         new_creatures[0] = new_cr
            #         filename = "elite_"+str(iteration)+".csv"
            #         gnlib.Genome.to_csv(cr.dna, filename)
            #         break
            
            # replace creature with prev gen with new ones
            pop.creatures = new_creatures
                            
        self.assertNotEqual(fits[0], 0)
unittest.main()
