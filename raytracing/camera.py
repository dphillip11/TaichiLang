import taichi as ti
import taichi.math as tm
import taichi_glsl as ts


class Camera:
    def __init__(self):
        self.res = (1000,750)
        self.pixels = ti.Vector.field(3, dtype=float, shape=self.res)
        self.collisions = ti.Vector.field(3, dtype=float, shape=self.res)
        self.depth = 1
        self.pos = ts.vec3(0, 5, 10)
        self.target = ts.vec3(0,0,5)
        self.right = ts.vec3(1, 0, 0)
        self.up = ts.vec3(0, 1, 0)
        self.forward = ts.vec3(0, 0, 1)

    def lookat(self, target):
        self.target = target
        self.forward = tm.normalize(target - self.pos)
        self.right = tm.normalize(tm.cross( ts.vec3(0, 1, 0), self.forward))
        self.up = tm.normalize(tm.cross(self.forward, self.right))

    def getRayDir(self, u,v):
        raydir = tm.normalize((self.forward * self.depth) + (u * self.right) + (v * self.up))
        return raydir

