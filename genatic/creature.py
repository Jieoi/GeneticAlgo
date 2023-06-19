import genome
from xml.dom.minidom import getDOMImplementation
from enum import Enum
import numpy as np

class MotorType(Enum):
    PULSE = 1
    SINE = 2

class Motor:
    def __init__(self, control_waveform, control_amp, control_freq):
        if control_waveform <= 0.5:
            self.motor_type = MotorType.PULSE
        else:
            self.motor_type = MotorType.SINE
        self.amp = control_amp
        self.freq = control_freq
        self.phase = 0

    # output from the motor(set up and update speed of motor)
    def get_output(self):
        # phase modulo 2 pi to ensure it loops around 2pi
        self.phase = (self.phase + self.freq) % (np.pi * 2)
        if self.motor_type == MotorType.PULSE:
            if self.phase < np.pi:
                output = 1 # set at 1 for 0-pi
            else: 
                output = -1 # set at -1 for pi-2pi
        if self.motor_type == MotorType.SINE:
            output = np.sin(self.phase)
        
        return output 


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
        # set no motors at the start
        self.motors = None
        # make creature ready to use
        self.get_flat_links()
        self.get_expanded_links()
        # set start and last position to None
        self.start_position = None
        self.last_position = None
        # set distance to be 0 for fitness function
        self.dist = 0
    
    # regenerate the links and joints
    def set_dna(self,dna):
        # get gene
        self.dna = dna
        # reset flat link to None at the start
        self.flat_links = None
        # reset expanded link to None at the start
        self.exp_links = None
        # reset no motors at the start
        self.motors = None
        # remake creature ready to use
        self.get_flat_links()
        self.get_expanded_links()
        # reset start and last position to None
        self.start_position = None
        self.last_position = None
        # reset distance to be 0 for fitness function
        self.dist = 0

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
        robot_tag.setAttribute("name", "jiejie") # choose a name!
        return robot_tag.toprettyxml()
    
    def get_motors(self):
        # one less motor than the links
        self.get_expanded_links()
        # assert(self.exp_links != None), "creature: call get_exp_links before get_motor"
        if self.motors == None:
            motors = []
            for i in range(1, len(self.exp_links)):
                l = self.exp_links[i]
                m = Motor(l.control_waveform,l.control_amp,l.control_freq)
                motors.append(m)
            self.motors = motors
        return self.motors

    def update_position(self, pos):
        # calcuate the distance travelled since last position update
        if self.last_position !=None:
            p1 = np.array(self.last_position)
            p2 = np.array(pos)
            dist = np.linalg.norm(p1-p2)
            self.dist = self.dist + dist
        # set start position to the pos at the start
        # or set as the last position
        # use to calculate the distance moved
        if self.start_position ==None:
            self.start_position = pos
        else:
            self.last_position = pos

    def get_distance_travelled(self):
        # get distance between p1 and p2
        # update: calculated in self.dist in update_position
        return self.dist

    def update_dna(self, dna):
        self.dna = dna
        self.flat_links = None
        self.exp_links = None
        self.motors = None
        self.start_position = None
        self.last_position = None
