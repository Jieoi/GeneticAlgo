import unittest
import simulation
import creature
import os
import population

class TestSim(unittest.TestCase):
    # check if the simulation exists
    def testSimExists(self):
        sim = simulation.Simulation()
        self.assertIsNotNone(sim)
    
    # check if the physics engine exists
    def testSimId(self):
        sim = simulation.Simulation()
        self.assertIsNotNone(sim.physicsClientId) 
    
    # test if creature can run inside the simulation
    def testRun(self):
        sim = simulation.Simulation()
        self.assertIsNotNone(sim.run_creature)

    # check if creature written to disk in temp.urdf
    def testRunXML(self):
        sim = simulation.Simulation()
        cr = creature.Creature(gene_count = 3)
        sim.run_creature(cr)
        self.assertTrue(os.path.exists("temp.urdf"))

    # check if creature has moved
    def testPosChanged(self):
        sim = simulation.Simulation()
        cr = creature.Creature(gene_count = 3)
        sim.run_creature(cr)
        # # print the start and end position
        # print(cr.start_position, cr.last_position)
        self.assertNotEqual(cr.start_position, cr.last_position)

    # check if the robot is travalling
    def testDitsance(self):
        sim = simulation.Simulation()
        cr = creature.Creature(gene_count = 3)
        sim.run_creature(cr)
        dist = cr.get_distance_travelled()
        print(dist)
        self.assertGreater(dist, 0)
    
    # check the population exists
    def testPop(self):
        pop = population.Population(pop_size = 5, gene_count=3)
        sim = simulation.Simulation()
        for cr in pop.creatures:
            sim.run_creature(cr)
        dists = [cr.get_distance_travelled() for cr in pop.creatures]
        print(dists)
        self.assertIsNotNone(dists)

    # multi threaded not working, testing without it
    def testProcNoThread(self):
        pop = population.Population(pop_size=20, gene_count=3)
        sim = simulation.Simulation()
        sim.eval_population(pop, 2400)
        dists = [cr.get_distance_travelled() for cr in pop.creatures]
        print(dists)
        self.assertIsNotNone(dists)

unittest.main()

# eng divide distance by motor for fairness or competition?