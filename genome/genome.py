import numpy as np
import copy

class Genome():
    # static function -> 
    # not rely on the state of the class no object required
    @staticmethod
    def get_random_gene(length):
        gene = np.array([np.random.random() for i in range(length)])
        return gene
    
    @staticmethod
    def get_random_genome(gene_length, gene_count):
        genome = [Genome.get_random_gene(gene_length) for _ in range(gene_count)]
        return genome

    @staticmethod
    def get_gene_spec():
        gene_spec = {"link-shape":{"scale":1},
            "link-length": {"scale":1},
            "link-radius": {"scale":1},
            "link-recurrence": {"scale":4},
            "link-mass": {"scale":1},
            "joint-type": {"scale":1},
            "joint-parent":{"scale":1},
            "joint-axis-xyz": {"scale":1},
            "joint-origin-rpy-1":{"scale":np.pi * 2},
            "joint-origin-rpy-2":{"scale":np.pi * 2},
            "joint-origin-rpy-3":{"scale":np.pi * 2},
            "joint-origin-xyz-1":{"scale":1},
            "joint-origin-xyz-2":{"scale":1},
            "joint-origin-xyz-3":{"scale":1},
            "control-waveform":{"scale":1},
            "control-amp":{"scale":0.25},
            "control-freq":{"scale":1}
            }
        ind = 0
        for key in gene_spec.keys():
            gene_spec[key]["ind"]=ind
            ind = ind + 1

        return gene_spec

    @staticmethod
    def expandLinks(parent_link, uniq_parent_name, flat_links, expanded_links):
        children = [l for l in flat_links if l.parent_name == parent_link.name] #finding all links with parent name the same as parent link
        
        for c in children:
            for r in range(c.recur):
                c_copy = copy.copy(c) # need to know its uniq parent
                c_copy.parent_name = uniq_parent_name
                # make the name uniq by adding the len at current pos
                # link in URDF need to be unique
                uniq_name = c_copy.name + str(len(expanded_links))
                c_copy.name = uniq_name
                expanded_links.append(c_copy)
                Genome.expandLinks(c, uniq_name, flat_links, expanded_links) #parent C, start from c


class URDFLink:
    def __init__(self, name, parent_name, recur):
        self.name = name
        self.parent_name = parent_name
        self.recur = recur