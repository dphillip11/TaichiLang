import taichi as ti
import taichi.math as tm

# check if ray intersects with sphere
@ti.func
def raySphereIntersect(ro, rd, centre, radius):
    oc = ro - centre
    a = tm.dot(rd, rd)
    b = 2 * tm.dot(oc, rd)
    c = tm.dot(oc, oc) - radius * radius
    discriminant = b * b - 4 * a * c
    distance = -1
    if (discriminant >= 0):
        distance = (-b - tm.sqrt(discriminant)) / (2.0 * a)
    return distance

@ti.func
def rayPlaneIntersect(ro, rd, normal, distance):
    denom = tm.dot(-normal, rd)
    d = -1
    if (denom > 1e-6):
        d = (denom - distance) / denom
    return d


@ti.func
def rayBoxIntersect(ro, rd, position, size):
    m = 1.0 / rd
    n = m * (ro - position)
    k = abs(m) * size
    t1 = -n - k
    t2 = -n + k
    tN = tm.max(tm.max(t1.x, t1.y), t1.z)
    tF = tm.min(tm.min(t2.x, t2.y), t2.z)
    if (tN > tF or tF < 0.0):
        tN = -1
    outNormal = tm.vec3(0,0,0)
    if tN > 0.0:
        outNormal = tm.step(tm.vec3(tN), t1)
    else: 
        outNormal = tm.step(t2, tm.vec3(tF))
    outNormal *= -tm.sign(rd)
    return tN


@ti.func
def capsuleIntersect(ro, rd, pa, pb, ra):
    ba = pb - pa
    oa = ro - pa
    baba = tm.dot(ba, ba)
    bard = tm.dot(ba, rd)
    baoa = tm.dot(ba, oa)
    rdoa = tm.dot(rd, oa)
    oaoa = tm.dot(oa, oa)
    a = baba - bard * bard
    b = baba * rdoa - baoa * bard
    c = baba * oaoa - baoa * baoa - ra * ra * baba
    h = b * b - a * c
    t = -1
    finalT = 0
    if (h >= 0.0):
        t = (-b - tm.sqrt(h)) / a
        y = baoa + t * bard
        # body
        if (y > 0.0 and y < baba):
            finalT = t
        # caps
        oc = tm.vec3(0)
        if (y <= 0.0):
            oc = oa
        else:
            oc = ro - pb
        b = tm.dot(rd, oc)
        c = tm.dot(oc, oc) - ra * ra
        h = b * b - c
        if (h > 0.0):
            t = -b - tm.sqrt(h)
    if finalT != 0:
        t = finalT
    return t
        