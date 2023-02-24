import taichi as ti
import taichi.math as tm

# raymarching function
@ti.func
def RayMarch(ro, rd):
    hit = -1
    distance = 0
    position = ro
    for i in range(100):
        radius = 1000
        radius = min(sdfSphere(position, tm.vec3(0,2,5), 3), radius)
        radius = min(sdfBox(position,tm.vec3(0,0,2.5),tm.vec3(0.8)), radius)
        radius = min(sdfCapsule(position, tm.vec3(-5,4,10), tm.vec3(5,4,10), 1), radius)
        radius = min(sdfPlane(position, tm.vec3(0,1,0), 1), radius)
        if (radius < 0.4):
            hit = 1
            break
        if (distance > 1000):
            hit = 0
            break
        distance += radius
        position += radius * rd
    return hit
# signed distance functions for primitives

@ti.func
def sdfSphere(point, centre, radius):
    return tm.length(point - centre) - radius

@ti.func
def sdfPlane(point, normal, distance):
    return tm.dot(point, normal) + distance

@ti.func
def sdfCapsule(point, a, b, radius):
    pa = point - a
    ba = b - a
    h = tm.clamp(tm.dot(pa, ba) / tm.dot(ba, ba), 0.0, 1.0)
    return tm.length(pa - ba * h) - radius

@ti.func
def sdfBox(point, position, size):
    q = abs(point - position) - size
    return tm.length(tm.max(q, 0)) + tm.min(tm.max(q.x, tm.max(q.y, q.z)), 0)

@ti.func
def sdfCone(point, position, height, radius):
    q = tm.vec3(tm.length(point.xy - position.xy), point.z - position.z, 0)
    return tm.length(tm.max(q * tm.vec3(1, 1 / height, 0), 0)) + tm.min(tm.max(q.x, q.y), 0) - radius

