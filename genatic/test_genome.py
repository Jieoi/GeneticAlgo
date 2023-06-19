import unittest
import genome
import numpy as np
import os

class GenomeTest(unittest.TestCase):

    def testClassExists(self):
        self.assertIsNotNone(genome.Genome)

    def testRandomGene(self):
        self.assertIsNotNone(genome.Genome.get_random_gene)

    def testRandomGeneNotNone(self):
        self.assertIsNotNone(genome.Genome.get_random_gene(5))

    def testRandomGeneHasValue(self):
        gene = genome.Genome.get_random_gene(5)
        #print(gene)
        self.assertIsNotNone(gene[0])

    def testRandomGeneLength(self):
        gene = genome.Genome.get_random_gene(20)
        #print(gene)
        self.assertEqual(len(gene),20)

    def testRandomGeneIsNumpyArrays(self):
        gene = genome.Genome.get_random_gene(20)
        self.assertEqual(type(gene), np.ndarray)

    def testRandomGenemeExists(self):
        data = genome.Genome.get_random_genome(20,5)
        self.assertIsNotNone(data)
    
    def testGeneSpecExist(self):
        spec = genome.Genome.get_gene_spec()
        self.assertIsNotNone(spec)
    
    def testGeneSpecHasLinkLength(self):
        spec = genome.Genome.get_gene_spec()
        self.assertIsNotNone(spec['link-length'])
    
    def testGeneSpecHasLinkID(self):
        spec = genome.Genome.get_gene_spec()
        #print(spec)
        self.assertIsNotNone(spec['link-length']['ind'])
    
    def testGeneSpecScale(self):
        spec = genome.Genome.get_gene_spec()
        gene = genome.Genome.get_random_gene(20)
        self.assertGreater(gene[spec['link-length']['ind']],0)

    def testFlatLinks(self):
        links = [
            genome.URDFLink(name="A",parent_name=None, recur=1),
            genome.URDFLink(name="B",parent_name='A', recur=1),
            genome.URDFLink(name="C",parent_name='B', recur=2),
            genome.URDFLink(name="D",parent_name='C', recur=1)
            
        ]
        self.assertIsNotNone(links)
    
    def testExpandLinks(self):
        links = [
            genome.URDFLink(name="A",parent_name=None, recur=1),
            genome.URDFLink(name="B",parent_name='A', recur=1),
            genome.URDFLink(name="C",parent_name='B', recur=2),
            genome.URDFLink(name="D",parent_name='C', recur=1)
            
        ];
        exp_links = [links[0]]
        genome.Genome.expandLinks(links[0], links[0].name, links, exp_links)
        # test code for the parents:
        # names = [l.name +'-parent is-' + str(l.parent_name) for l in exp_links]
        # print(names)
        self.assertEqual(len(exp_links),6) #ABCDCD

    def testGeneToDeneDict_linkrec(self):
        spec =genome.Genome.get_gene_spec()
        gene = genome.Genome.get_random_gene(len(spec))
        gene_dict =genome.Genome.get_gene_dict(gene,spec)
        self.assertIn('link-recurrence', gene_dict.keys()) #first is the thing to be found

    def testGenomeToDict(self):
        spec =genome.Genome.get_gene_spec()
        # attr: len of gen and gene counts
        dna = genome.Genome.get_random_genome(len(spec),3)
        # list of dict, each from each gene
        genome_dicts = genome.Genome.get_genome_dicts(dna, spec)
        self.assertEqual(len(genome_dicts),3)

    def testGetLinks(self):
        spec =genome.Genome.get_gene_spec()
        # attr: len of gen and gene counts
        dna = genome.Genome.get_random_genome(len(spec),3)
        # list of dict, each from each gene
        genome_dicts = genome.Genome.get_genome_dicts(dna, spec)
        links = genome.Genome.genome_to_links(genome_dicts)
        self.assertEqual(len(links),3)

    # More challenging test
    def testGetLinksUniqueNames(self):
        spec = genome.Genome.get_gene_spec()
        dna = genome.Genome.get_random_genome(len(spec), 3)
        gdicts = genome.Genome.get_genome_dicts(dna, spec)
        links = genome.Genome.genome_to_links(gdicts)
        # check that each link's name only appears once
        for l in links:
            names = [link.name for
                link in links
                if link.name == l.name]
            self.assertEqual(len(names), 1)
    
    # Cross over test
    def testCross(self):
        g1 = np.array([[1,2,3], [4,5,6], [7,8,9]])
        g2 = np.array([[10,11,12], [13,14,15], [16,17,18]])
        for i in range(100): #stress test
            g3 = genome.Genome.crossover(g1, g2)
        # print(g1, g2, g3)
        self.assertEqual(len(g3), len(g1))

    # Point mutation test
    def test_point(self):
        g1 = np.array([[1.0,2.0,3.0],[4.0,5.0,6.0],[7.0,8.0,9.0]])
        #print(g1)
        genome.Genome.point_mutation(g1,rate=0.5, amount=0.25)
        #print("mutated: "+str(g1))
        # test for point mutation
        #self.assertNotEqual(g1, g2)

    # Test for removing gene
    def test_shrink(self):
        g1 = np.array([[1.0,2.0,3.0],[4.0,5.0,6.0],[7.0,8.0,9.0]])
        g2 = genome.Genome.shrink_mutation(g1,rate=1)
        #print(g1,g2)
        self.assertNotEqual(len(g1),len(g2))
    
    # Test for new added gene
    def test_grow(self):
        g1 = np.array([[1.0,2.0,3.0],[4.0,5.0,6.0],[7.0,8.0,9.0]])
        g2 = genome.Genome.grow_mutation(g1,rate=1)
        #print(g1,g2)
        self.assertGreater(len(g2),len(g1))

    # Test for writing to csv file to save the gene
    def test_tocsv(self):
        g1 = [[1,2,3]]
        genome.Genome.to_csv(g1, 'test.csv')
        self.assertTrue(os.path.exists('test.csv'))
        
    # Test to for the csv file content
    def test_tocsv_content(self):
        g1 = [[1,2,3]]
        genome.Genome.to_csv(g1, 'test.csv')
        expect = "1,2,3,\n"
        with open('test.csv') as f:
            csv_str = f.read() 
        self.assertEqual(csv_str, expect)

    # Test CSV has multiple line
    def test_tocsv_content2(self):
        g1 = [[1,2,3], [4,5,6]]
        genome.Genome.to_csv(g1, 'test.csv')
        expect = "1,2,3,\n4,5,6,\n"
        with open('test.csv') as f:
            csv_str = f.read() 
        self.assertEqual(csv_str, expect)
    
    # Test if the file is readed from the csv
    def test_from_csv(self):
        g1 = [[1,2,3]]
        genome.Genome.to_csv(g1, 'test.csv')
        g2 = genome.Genome.from_csv('test.csv')
        # print(g1, g2)
        self.assertTrue(np.array_equal(g1, g2))
    
    # Test if the imported file has two lines
    def test_from_csv2(self):
        g1 = [[1,2,3], [4,5,6]]
        genome.Genome.to_csv(g1, 'test.csv')
        g2 = genome.Genome.from_csv('test.csv')
        print(g1, g2)
        self.assertTrue(np.array_equal(g1, g2))

if __name__ == '__main__':
    unittest.main()
