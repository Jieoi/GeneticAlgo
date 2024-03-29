import unittest
import creature
import pybullet as p
import genome
 
class TestCreature(unittest.TestCase):
    def testCreateureExists(self):
        self.assertIsNotNone(creature.Creature)
    
    def testCreatureGetFlatLinks(self):
        c = creature.Creature(gene_count=4)
        # c instead of creature for 
        links = c.get_flat_links()
        self.assertEqual(len(links),4)
    
    def testExpandedLinks(self):
        # random gene generated, test multiple times
        # for i in range(100):
        c = creature.Creature(gene_count=4)
        links = c.get_flat_links()
        # above are same to get flat links
        exp_links = c.get_expanded_links()
        # print(len(exp_links))
        # expanded links have larger (rec) or equal (all rec = 1) length as flat links
        self.assertGreaterEqual(len(exp_links), len(links))

    def testToXML(self):
        c = creature.Creature(gene_count=4)
        c.get_expanded_links()
        xml_str = c.to_xml()
        # with open('102.urdf','w') as f:
        #     f.write('<?xml version="1.0"?>' + "\n" + xml_str)
        self.assertIsNotNone(xml_str)

    def testToXMLNotNone(self):
        c = creature.Creature(gene_count=2)
        xml_str = c.to_xml()
        self.assertIsNotNone(xml_str)

    def testLoadXML(self):
        c = creature.Creature(gene_count=20)
        xml_str = c.to_xml()
        with open('test.urdf', 'w') as f:
            f.write(xml_str)
        p.connect(p.DIRECT)
        cid = p.loadURDF('test.urdf')
        self.assertIsNotNone(cid)

    def testRadial(self):
        # hard codes some links
        links = [
            genome.URDFLink(name="A",parent_name=None, recur = 1),
            # test for multiple children/sibling
            genome.URDFLink(name="B",parent_name='A', recur = 6, joint_origin_rpy_1=0.75, link_length=1.0),
        ]
        c = creature.Creature(gene_count = 2)
        c.flat_links = links
        c.get_expanded_links()
        xml_str = c.to_xml()
        with open('103.urdf', 'w') as f:
            f.write('<?xml version="1.0"?>' + "\n" + xml_str)

#motor
    def testMotor(self):
        m = creature.Motor(0.1,0.5,0.5)
        self.assertIsNotNone(m)
    
    def testMotorValPulse(self):
        m = creature.Motor(0.1,0.5,0.5)
        self.assertEqual(m.get_output(),1)

    def testMotorValSine(self):
        m = creature.Motor(0.6,0.5,0.5)
        m.get_output()
        m.get_output()
        m.get_output()
        self.assertGreater(m.get_output(),0)
    
    def testCMot(self):
        c = creature.Creature(gene_count = 4)
        ls = c.get_expanded_links()
        ms = c.get_motors()
        self.assertEqual(len(ls)-1, len(ms))

unittest.main()