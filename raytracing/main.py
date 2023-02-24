import taichi as ti
import numpy as np
import taichi_glsl as ts
import taichi.math as tm
from SDF import *
from colors import *
from camera import *
from scene import *

ti.init(arch = ti.x86_64)

scene = Scene()
cam = Camera()
iTime = 0
FPSTarget = 60
dt = 4e-2/FPSTarget


@ti.kernel
def paint():
    cam.lookat(scene.ballPos[2])
    for i, j in cam.pixels:
        u = (i - (0.5 * cam.res[0]))/cam.res[1]
        v = (j - (0.5 * cam.res[1]))/cam.res[1]
        raydir = cam.getRayDir(u,v)
        distance, ID = scene.GetHit(cam.pos, raydir)
        cam.collisions[i, j] = tm.vec3(distance, ID, 0)
        cam.pixels[i, j] = GetColor(ID)



# pass variables from python to taichi via a kernel, parameters must be type annotated
@ti.kernel
def updateBallPos(iTime: float):
    scene.ballPos[0] = ts.vec3(-4 - max(tm.sin(100 * iTime),0),2,5) 
    scene.ballPos[4] = ts.vec3(4 - min(tm.sin(100 * iTime),0),2,5) 


# this is the main loop, note that it is globally scoped
gui = ti.GUI('UV', cam.res)
while not gui.get_event(ti.GUI.ESCAPE):
    iTime += dt
    updateBallPos(iTime)
    cam.pos = ts.vec3(10, 5, -20)
    paint()
    gui.set_image(cam.pixels)
    gui.show()

