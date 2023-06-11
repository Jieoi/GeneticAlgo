import genome
from xml.dom.minidom import getDOMImplementation

class Creature:
    def __init__(self, gene_count):
        # get gene length
        self.spec = genome.Genome.get_gene_spec()
        # get gene
        self.dna = genome.Genome.get_random_genome(len(self.spec), gene_count)
        # set flat link to None at the start
        self.flat_links = None
        # set expanded link to None at the start
        self.exp_links = None


    
    # convert dna into a set of flat link using genome
    def get_flat_links(self):
        if self.flat_links == None:
            # get gene dictionary
            gdicts =genome.Genome.get_genome_dicts(self.dna, self.spec)
            # get flat links
            self.flat_links = genome.Genome.genome_to_links(gdicts)
        return self.flat_links
    
    def get_expanded_links(self):
        # get the flat links
        self.get_flat_links()
        if self.exp_links is not None:
            return self.exp_links

        #expanded links
        exp_links = [self.flat_links[0]]
        # parent_link (first parent), uniq_parent_name, flat_links, expanded_links
        genome.Genome.expandLinks(self.flat_links[0],
                                self.flat_links[0].name,
                                self.flat_links,
                                exp_links)
        # generate and store the expanded link in creature, creature is stateful
        self.exp_links = exp_links
        return self.exp_links

    def to_xml(self):
        # make sure expanded links are available
        self.get_expanded_links()
        domimpl = getDOMImplementation()
        
        adom = domimpl.createDocument(None, "start", None)
        robot_tag = adom.createElement("robot")
        for link in self.exp_links:
            robot_tag.appendChild(link.to_link_element(adom))
            first = True
        for link in self.exp_links:
            if first:# skip the root node!
                first = False
                continue
            robot_tag.appendChild(link.to_joint_element(adom))
        robot_tag.setAttribute("name", "pepe") # choose a name!
        return robot_tag.toprettyxml()
