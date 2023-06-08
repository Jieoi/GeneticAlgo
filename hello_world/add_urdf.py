import pybullet as p
import keyboard

p.connect(p.GUI)

##do not cache the urdf so that editing will be live
p.setPhysicsEngineParameter(enableFileCaching=0)
##
plane_shape = p.createCollisionShape(p.GEOM_PLANE)
floor = p.createMultiBody(plane_shape, plane_shape)
p.setGravity(0,0,-10)
###starter.py###

robot = p.loadURDF(r'C:\Users\xjie\Documents\SIM\Y3S2\genAlgo\robot\urdf\101.urdf')

while p.isConnected() and not keyboard.is_pressed('q'):
    p.stepSimulation()

p.disconnect()