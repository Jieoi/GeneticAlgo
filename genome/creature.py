import genome

class Creature:
    def __init__(self, gene_count):
        # get gene length
        self.spec = genome.Genome.get_gene_spec()
        # get gene
        self.dna = genome.Genome.get_random_genome(len(self.spec), gene_count)
    
    # convert dna into a set of flat link using genome
    def get_flat_links(self):
        # get gene dictionary
        gdicts =genome.Genome.get_genome_dicts(self.dna, self.spec)
        # get flat links
        self.flat_links = genome.Genome.genome_to_links(gdicts)
        return self.flat_links
    
    def get_expanded_links(self):
        # get the flat links
        self.get_flat_links()
        #expanded links
        exp_links = []
        # parent_link (first parent), uniq_parent_name, flat_links, expanded_links
        genome.Genome.expandLinks(self.flat_links[0],
                                self.flat_links[0].name,
                                self.flat_links,
                                exp_links)
        # generate and store the expanded link in creature, creature is stateful
        self.exp_links = exp_links
        return self.exp_links