import unittest
import simulation
import creature
import os

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

unittest.main()