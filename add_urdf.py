import pybullet as p
import pybullet_data as pd

p.connect(p.GUI)

##do not cache the urdf so that editing will be live
p.setPhysicsEngineParameter(enableFileCaching=0)
##
plane_shape = p.createCollisionShape(p.GEOM_PLANE)
floor = p.createMultiBody(plane_shape, plane_shape)
p.setGravity(0,0,-10)
###starter.py###

#robot = p.loadURDF('C:\Users\xjie\anaconda3\envs\genAlgo\Lib\site-packages\pybullet_data\r2d2.urdf')
robot = p.loadURDF('C:\Users\xjie\Documents\SIM\Y3S2\genAlgo\robot\urdf\101.urdf')
