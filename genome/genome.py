#from xml.dom.minidom import getDOMImplementation
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
        # sibling_ind = 1

        for c in children:
            for r in range(int(c.recur)):
                c_copy = copy.copy(c) # need to know its uniq parent
                c_copy.parent_name = uniq_parent_name
                # make the name uniq by adding the len at current pos
                # link in URDF need to be unique
                uniq_name = c_copy.name + str(len(expanded_links))
                c_copy.name = uniq_name
                expanded_links.append(c_copy)
                Genome.expandLinks(c, uniq_name, flat_links, expanded_links) #parent C, start from c

    @staticmethod
    def get_gene_dict(gene, spec):
        gdict = {}
        for key in spec:
            ind = spec[key]['ind']
            scale = spec[key]["scale"]
            gdict[key] = gene[ind]*scale
        return gdict

    @staticmethod
    def get_genome_dicts(genome,spec):
        gdicts = []
        for gene in genome:
            gdicts.append(Genome.get_gene_dict(gene, spec))
        return gdicts

    # Converts scaled and labelled genome data into URDFLink objects
    @staticmethod
    def genome_to_links(gdicts):
        links = []
        link_ind = 0
        parent_names = [str(link_ind)]

        for gdict in gdicts:
            # name, parent name and recur value needed
            link_name = str(link_ind) # no increment yet
            # parent name
            # in zeroth iteration, it is linked to itself, do not add to itself below
            parent_ind = gdict["joint-parent"] * len(parent_names)
            parent_name = parent_names[int(parent_ind)]

            recur = gdict["link-recurrence"]
            link = URDFLink(name=link_name, 
                            parent_name=parent_name, 
                            recur=recur+1, # set recurrsion to at least 1, prevent recur of zero (no child)
                            link_length=gdict["link-length"], 
                            link_radius=gdict["link-radius"], 
                            link_mass=gdict["link-mass"],
                            joint_type=gdict["joint-type"],
                            joint_parent=gdict["joint-parent"],
                            joint_axis_xyz=gdict["joint-axis-xyz"],
                            joint_origin_rpy_1=gdict["joint-origin-rpy-1"],
                            joint_origin_rpy_2=gdict["joint-origin-rpy-2"],
                            joint_origin_rpy_3=gdict["joint-origin-rpy-3"],
                            joint_origin_xyz_1=gdict["joint-origin-xyz-1"],
                            joint_origin_xyz_2=gdict["joint-origin-xyz-2"],
                            joint_origin_xyz_3=gdict["joint-origin-xyz-3"],
                            control_waveform=gdict["control-waveform"],
                            control_amp=gdict["control-amp"],
                            control_freq=gdict["control-freq"])
            # append to link
            links.append(link)

            # link become avaliable parent name
            if link_ind != 0: # don't re-add the first link
                parent_names.append(link_name)
            link_ind = link_ind + 1

        # now just fix the first link so it links to nothing
        links[0].parent_name = "None" # set parent node to none for the root node
        return links

class URDFLink:
    def __init__(self, name, parent_name, recur, 
                link_length = 0.1, 
                link_radius = 0.1, 
                link_mass = 0.1,
                joint_type = 0.1,
                joint_parent = 0.1,
                joint_axis_xyz = 0.1,
                joint_origin_rpy_1 = 0.1,
                joint_origin_rpy_2 = 0.1,
                joint_origin_rpy_3 = 0.1,
                joint_origin_xyz_1 = 0.1,
                joint_origin_xyz_2 = 0.1,
                joint_origin_xyz_3 = 0.1,
                control_waveform = 0.1,
                control_amp = 0.1,
                control_freq = 0.1):
        self.name = name
        self.parent_name = parent_name
        self.recur = recur 
        self.link_length = link_length 
        self.link_radius = link_radius
        self.link_mass = link_mass
        self.joint_type = joint_type
        self.joint_parent = joint_parent
        self.joint_axis_xyz = joint_axis_xyz
        self.joint_origin_rpy_1 = joint_origin_rpy_1
        self.joint_origin_rpy_2 = joint_origin_rpy_2
        self.joint_origin_rpy_3 = joint_origin_rpy_3
        self.joint_origin_xyz_1 = joint_origin_xyz_1
        self.joint_origin_xyz_2 = joint_origin_xyz_2
        self.joint_origin_xyz_3 = joint_origin_xyz_3
        self.control_waveform = control_waveform
        self.control_amp = control_amp
        self.control_freq = control_freq
        self.sibling_ind = 1
    
    # stateful, depending on its own self.parameter
    # dom generated in test/creature
    def to_link_xml(self, adom):
        return ""