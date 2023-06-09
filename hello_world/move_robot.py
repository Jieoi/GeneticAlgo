import pybullet as p
import keyboard

p.connect(p.GUI)

##do not cache the urdf so that editing will be live
p.setPhysicsEngineParameter(enableFileCaching=0)
##get rid of the panels
p.configureDebugVisualizer(p.COV_ENABLE_GUI, 0)

plane_shape = p.createCollisionShape(p.GEOM_PLANE)
floor = p.createMultiBody(plane_shape, plane_shape)
p.setGravity(0,0,-10)
###starter.py###

robot = p.loadURDF(r'C:\Users\xjie\Documents\SIM\Y3S2\genAlgo\robot\urdf\move.urdf')

p.setRealTimeSimulation(1)
p.resetBasePositionAndOrientation(robot, [0,0,0.2],[0,0,0,1])
p.setJointMotorControl2(robot, 0, controlMode=p.VELOCITY_CONTROL, targetVelocity=0.5)
# robotID, jointID, controlMode, targetPosition
p.setJointMotorControl2(robot, 0, controlMode=p.POSITION_CONTROL, targetVelocity=10, targetPosition=0.5)
p.getJointInfo(robot,0)

###terminate
while p.isConnected() and not keyboard.is_pressed('q'):
    p.stepSimulation()

p.disconnect()