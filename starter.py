import pybullet as p
import pybullet_data as pd

p.connect(p.GUI)

plane_shape = p.createCollisionShape(p.GEOM_PLANE)
floor = p.createMultiBody(plane_shape, plane_shape)
p.setGravity(0,0,-10)
