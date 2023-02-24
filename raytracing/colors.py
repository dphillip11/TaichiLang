import taichi.math as tm
import taichi as ti

@staticmethod
@ti.func
def GetColor(ID):
    color = tm.vec3(0,0,0)
    if ID == 0:
        color = tm.vec3(0.5,0,0)
    if ID == 1:
        color = tm.vec3(1,0,0)
    elif ID == 2:
        color = tm.vec3(0,1,0)
    elif ID == 3:
        color = tm.vec3(0,0,1)
    elif ID == 4:
        color = tm.vec3(1,1,0)
    elif ID == 5:
        color = tm.vec3(1,0,1)
    elif ID == 6:
        color = tm.vec3(0,1,1)
    elif ID == 7:
        color = tm.vec3(1,1,1)
    elif ID == 8:
        color = tm.vec3(0.5,0.5,0.5)
    return color