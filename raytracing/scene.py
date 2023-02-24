import taichi as ti
import taichi.math as tm
from RayIntersections import *

class Scene:
    def __init__(self):
        self.ballPos = ti.Vector.field(3, dtype=float, shape=(5, ))
        self.ballPos[0] = [-4,2,5]
        self.ballPos[1] = [-2,2,5]
        self.ballPos[2] = [0,2,5]
        self.ballPos[3] = [2,2,5]
        self.ballPos[4] = [4,2,5]

        self.boxPos = ti.Vector.field(3, dtype=float, shape=(6, ))
        self.boxPos[0] = [-5,4,2]
        self.boxPos[1] = [5,4,2]
        self.boxPos[2] = [5,4,8]
        self.boxPos[3] = [-5,4,8]
        self.boxPos[4] = [0,8,8]
        self.boxPos[5] = [0,8,2]

        self.boxSize = ti.Vector.field(3, dtype=float, shape=(6, ))
        self.boxSize[0] = [0.25,4,0.25]
        self.boxSize[1] = [0.25,4,0.25]
        self.boxSize[2] = [0.25,4,0.25]
        self.boxSize[3] = [0.25,4,0.25]
        self.boxSize[4] = [5.25,0.25,0.25]
        self.boxSize[5] = [5.25,0.25,0.25]

    @ti.func
    def GetHit(self, ro, raydir): 
        distance = 1000
        ID = -1 
        # check balls
        for i in range(5):
            d = raySphereIntersect(ro, raydir, self.ballPos[i], 1)
            if d > 0 and d < distance:
                distance = d
                ID = i
        # check boxes
        for i in range(6):
            d = rayBoxIntersect(ro, raydir, self.boxPos[i], self.boxSize[i])
            if d > 0 and d < distance:
                distance = d
                ID = 6
        # check floor
        d = rayPlaneIntersect(ro, raydir, tm.vec3(0,1,0), -ro.y)
        if d > 0 and d < distance:
            distance = d
            ID = 7
        return distance, ID