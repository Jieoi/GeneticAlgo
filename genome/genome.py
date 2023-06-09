import numpy as np

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

