import unittest
import creature

class TestCreature(unittest.TestCase):
    def testCreateureExists(self):
        self.assertIsNotNone(creature.Creature)
    
    def testCreatureGetFlatLinks(self):
        c = creature.Creature(gene_count=4)
        #####AttributeError: module 'creature' has no attribute 'get_flat_links'####### replaced creature with C
        # c instead of creature for 
        links = c.get_flat_links()
        self.assertEqual(len(links),4)
    
    def testExpandedLinks(self):
        # random gene generated, test multiple times
        for i in range(100):
            c = creature.Creature(gene_count=4)
            links = c.get_flat_links()
            # above are same to get flat links
            exp_links = c.get_expanded_links()
            print(len(exp_links))
            # expanded links have larger (rec) or equal (all rec = 1) length as flat links
            self.assertGreaterEqual(len(exp_links), len(links))

unittest.main()