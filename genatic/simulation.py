import pybullet as p
#from multiprocessing import Pool

class Simulation():
    # Creates a physics engine as far as possible without GUI
    def __init__(self, sim_id = 0):
        self.physicsClientId = p.connect(p.DIRECT)
        self.sim_id = sim_id

    def run_creature(self, cr,iterations=2400):
        #running at 240 iteration per sec in GUI 
        # (10 sec of simulation)
        pid = self.physicsClientId
        p.resetSimulation(physicsClientId = pid)
        p.setGravity(0,0,-10, physicsClientId = pid)
        # prevent caching
        p.setPhysicsEngineParameter(enableFileCaching=0, physicsClientId = pid)

        # set a floor
        plane_shape = p.createCollisionShape(p.GEOM_PLANE, physicsClientId=pid)
        floor = p.createMultiBody(plane_shape, plane_shape, physicsClientId=pid)

        # setting for the xml file
        xml_file = 'temp'+ str(self.sim_id) +".urdf"
        xml_str = cr.to_xml()
        with open(xml_file, 'w') as f:
            f.write(xml_str)
        cid = p.loadURDF(xml_file,physicsClientId=pid)
        
        # set position to slightly above ground level at origin
        p.resetBasePositionAndOrientation(cid, [0,0,3],[0,0,0,1],physicsClientId=pid)
        for step in range(iterations):
            p.stepSimulation(physicsClientId=pid)
            if step % 24 == 0:
                self.update_motors(cid=cid, cr=cr)

            # built in function for getting pos and orn
            pos, orn = p.getBasePositionAndOrientation(cid,physicsClientId=pid)
            cr.update_position(pos)
            # if step > 0:
            #     print(cr.last_position[2])



    def update_motors(self, cid,cr):
        """
        cid is the id in the physics engine
        cr is a creature object
        """
        for jid in range(p.getNumJoints(cid,
                                        physicsClientId=self.physicsClientId)):
            m = cr.get_motors()[jid]

            p.setJointMotorControl2(cid, jid, 
                    # velocity_control: changing the speed of motor
                    controlMode=p.VELOCITY_CONTROL, 
                    # velocity is output of motor
                    targetVelocity=m.get_output(), 
                    force = 5, 
                    physicsClientId=self.physicsClientId)
        
    def eval_population(self, pop, iterations):
        for cr in pop.creatures:
            self.run_creature(cr, 2400) 
        
## Multithreaded do not work
# class ThreadedSim():
#     def __init__(self, cpu):
#         self.sims = [Simulation(i) for i in range(cpu)]

#     @staticmethod
#     def static_run_creature(sim, cr, iterations):
#         sim.run_creature(cr, iterations)
#         return cr 

#     def eval_population(self, pop, iterations):
#         """
#         pop is a Population object
#         iterations is frames in pybullet to run for at 240fps
#         """
#         pool_args = [] 
#         start_ind = 0
#         pool_size = len(self.sims)
#         while start_ind < len(pop.creatures):
#             this_pool_args = []
#             for i in range(start_ind, start_ind + pool_size):
#                 if i == len(pop.creatures):# the end
#                     break
#                 # work out the sim ind
#                 sim_ind = i % len(self.sims)
#                 this_pool_args.append([
#                             self.sims[sim_ind], 
#                             pop.creatures[i], 
#                             iterations]   
#                 )
#             pool_args.append(this_pool_args)
#             start_ind = start_ind + pool_size

#         new_creatures = []
#         for pool_argset in pool_args:
#             with Pool(pool_size) as p:
#                 # it works on a copy of the creatures, so receive them
#                 creatures = p.starmap(ThreadedSim.static_run_creature, pool_argset)
#                 print("got", len(creatures),"from starmap type is", type(creatures))
#                 # and now put those creatures back into the main 
#                 # self.creatures array
#                 new_creatures.extend(creatures)
#         for cr in new_creatures:
#             print(cr.get_distance_travelled())
#         pop.creatures = new_creatures

