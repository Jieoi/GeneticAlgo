import pybullet as p
import pybullet_data as pd
import creature 
import time
import genome as genlib

# starter code
p.connect(p.GUI)

##do not cache the urdf so that editing will be live
p.setPhysicsEngineParameter(enableFileCaching=0)
##get rid of the panels
p.configureDebugVisualizer(p.COV_ENABLE_GUI, 0)
plane_shape = p.createCollisionShape(p.GEOM_PLANE)
floor = p.createMultiBody(plane_shape, plane_shape)
p.setGravity(0,0,-10)

# Create creature with gene from csv
c = creature.Creature(gene_count = 5)
dna = genlib.Genome.from_csv('9_elite.csv')
c.set_dna(dna)
# save to XML
with open('test.urdf','w') as f:
    c.get_expanded_links()
    f.write(c.to_xml())

# load the urdf file
cid = p.loadURDF('test.urdf')

# set real time simulation to true
p.setRealTimeSimulation(1)

# set the original position to be origin
c.update_position([0,0,0])

# set position to slightly above ground level at origin
p.resetBasePositionAndOrientation(cid, [0,0,3],[0,0,0,1])
# infinite loop to iterate
while True:
    for jid in range(p.getNumJoints(cid)):
        m =c.get_motors()[jid]
        # id of creature:cid
        p.setJointMotorControl2(cid,jid,
            controlMode = p.VELOCITY_CONTROL,
            targetVelocity = m.get_output(),
            force = 5)
    pos, orn = p.getBasePositionAndOrientation(cid)
    c.update_position([pos])
    print(c.get_distance_travelled())
    time.sleep(0.1) # update the motor every 0.1 sec
