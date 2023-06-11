import unittest
import genome
import numpy as np
from xml.dom.minidom import getDOMImplementation

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
            
        ];
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
        names = [l.name +'-parent is-' + str(l.parent_name) for l in exp_links]
        print(names)
        self.assertEqual(len(exp_links),6) #ABCDCD
##
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

    def testLinkToXML(self):
        link = genome.URDFLink(name="A",parent_name="None", recur=1)

        domimpl = getDOMImplementation()
        adom = domimpl.createDocument(None,"starter",None)

        xml_str = link.to_link_element(adom)
        print(xml_str)
        self.assertIsNotNone(xml_str)

# more challenging test
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


if __name__ == '__main__':
    unittest.main()
