import math
import numpy as np
import pandas as pd
from math import cos, sin, sqrt,


def yaw(xy):
    m = np.zeros([3,3])
    m[0][0] = cos(xy)
    m[0][2] = sin(xy)
    m[2][0] = -sin(xy)
    m[2][2] = cos(xy)
    m[1][1] = 1
    return m


def pitch(xz):
    m = np.zeros([3,3])
    m[0][0] = 1
    m[1][1] = cos(xz)
    m[1][2] = sin(xz)
    m[2][1] = -sin(xz)
    m[2][2] = cos(xz)
    return m

def roll(yz):
    m = np.zeros([3,3])
    cyz = cos(yz)
    syz = sin(yz)
    m[0][0] = cyz
    m[0][1] = syz
    m[1][0] = -syz
    m[1][1] = cyz
    m[2][2] = 1
    return m

def innerprod(v1,v2):
    s = 0
    for i in range(len(v1)):
        s += v1[i]*v2[i]
    return s

def transpose(mat):
    t = []
    for r in range(len(mat)):
        ro = []
        for c in range(len(mat[r])):
            ro.append( mat[c][r])
        t.append(ro)
    return t

def mmult(m1,m2):
    tran = transpose(m2)
    p = []
    for r in range(len(m1)):
        p.append([])
        for c in range(len(tran)):
            p[r].append(innerprod(m1[r], tran[c]))
    return p

def rotn():
    phi = 45
    psi = -45
    y = yaw(math.radians(phi))
    p = pitch(math.radians(psi))
    return y@p

def euc2(p1,p2=[0.0,0.0]):
    return length2(p1,p2)

def euc3(p1,p2=[0.0,0.0,0.0]):
    return length3(p1,p2)

def length3(p1,p2=[0.0,0.0,0.0]):
    return math.sqrt((p1[0]-p2[0])**2 +
                     (p1[1]-p2[1])**2 +
                     (p1[2]-p2[2])**2 )

def length2(p1,p2=[0.0,0.0]):
    return math.sqrt((p1[0]-p2[0])**2 +
                     (p1[1]-p2[1])**2 )

def angle(x,y):
    return math.atan2(x,y)

# vector functions, vector(s) in, vector out
#column U implied radial length
def irl2(vect1):
    # vl = len(vect1)
    # result = []
    # for ndx in range(vl):
    #     result.append(euc2(vect1[ndx]))
    # return np.array(result)
    return np.array(list(map(euc2,vect1)))

#called column S, implied circumferential length, pass in two refs to same vect, offset
def icl2(vec1, vec2):
    # vl = min(len(vec1),len(vec2))
    # result = []
    # for ndx in range(vl):
    #     result.append(euc2(vec1[ndx],vec2[ndx]))
    # return np.array(result)
    return np.array(list(map(euc2,vec1,vec2)))


def smu(vec1,vec2):
    v1 = adj_data(vec1)
    v2 = adj_data(vec2)
    icl = icl2(v1,v2)
    irl = irl2(v1)
    return icl - irl


def absiclminusirl():
    pass

def aglessulag():
    pass

def load_data(fn ):
    game_data = pd.read_csv(fn, names=['Date','gm','b1', 'b2', 'b3', 'b4', 'b5','wc'])
    return game_data

# def adj_data1(vec, scale=1):
#     #vec = mega['b1'][::-scale] #reverse order for diffing
#     x = np.diff(vec)
#     y = np.diff(x)
#     z = np.diff(y)
#     x = x[:len(z)] #truncate to same length
#     y = y[:len(z)]
#     rotmat = rotn()
#     xyz2 = np.zeros((len(z),3))
#     for i in range(len(z)):
#         xyz2[i][0] = innerprod([x[i],y[i],z[i]],rotmat[0])
#         xyz2[i][1] = innerprod([x[i],y[i],z[i]],rotmat[1])
#         xyz2[i][2] = innerprod([x[i],y[i],z[i]],rotmat[2])
#     return xyz2

def adj_data(vec):
    rotmat=rotn()
    xyz2 = rotmat @ np.array(vec).T
    return xyz2


def raw_est(x,y,z, gm_max):
    rotmat = rotn()
    est_x = np.arange(x,gm_max+x)
    est_y = np.arange(y,gm_max+y)
    est_z = np.arange(z,gm_max+z)
    return [est_x,est_y,est_z]

def adj_est(x,y,z,gm_max):
    rotmat = rotn()
    xyz2 = np.zeros((gm_max,3))
    est_x,est_y,est_z = raw_est(x,y,z,gm_max)
    for i in range(gm_max):
        xyz2[i][0] = innerprod([est_x[i], est_y[i], est_z[i]], rotmat[0])
        xyz2[i][1] = innerprod([est_x[i], est_y[i], est_z[i]], rotmat[1])
        xyz2[i][2] = innerprod([est_x[i], est_y[i], est_z[i]], rotmat[2])
    return xyz2
#
# def adj_est2(x,y,z,gm_max):
#     rotmat = rotn()
#     xyz3 = np.zeros((gm_max,3))
#     ex,ey,ez = raw_est(x,y,z,gm_max)
#     ez = -ex - ey
#     ey = -ex
#     ex = np.zeros((len(ey)))
#     #return [ex,ey,ez]
#     for i in range(gm_max):
#          xyz3[i][0] = innerprod([ex[i], ey[i], ez[i]], rotmat[0])
#          xyz3[i][1] = innerprod([ex[i], ey[i], ez[i]], rotmat[1])
#          xyz3[i][2] = innerprod([ex[i], ey[i], ez[i]], rotmat[2])
#     return xyz3

def circum(x,y,z,gm_max):
    ae = adj_est(x,y,z,gm_max)
    ae2 = adj_est2(x,y,z,gm_max)
    q = []
    for ndx in range(len(ae)):
        q.append(length2(ae[ndx], ae2[ndx]))
    return q

def circum_pt(x,y,z,x1,y1,z1,gm_max):
    rm = rotn()
    pt = []
    pt.append(innerprod([x1,y1,z1],rm[0]))
    pt.append(innerprod([x1,y1,z1],rm[1]))
    pt.append(innerprod([x1,y1,z1],rm[2]))
    print(pt)
    ae = adj_est(x,y,z,gm_max)
    print(ae[0])
    q = []
    for ndx in range(len(ae)):
        q.append(length2([pt[0],pt[1]], ae[ndx]))
    return q

def radial1(x,y,z,gm_max):
    ae = adj_est(x,y,z,gm_max)
    q = []
    for ndx in range(len(ae)):
        q.append(length2(ae[ndx]))
    return q

def radial(x,y,z,gm_max):
    #ae = adj_est(x,y,z,gm_max)
    ae2 = adj_est2(x,y,z,gm_max)
    q = []
    for ndx in range(len(ae2)):
        q.append(length2(ae2[ndx]))
    return q

def c2r(x,y,z,gm_max):
    q = circum(x,y,z,gm_max)
    r = radial(x,y,z,gm_max)
    result = []
    for ndx in range(len(r)):
        result.append(q[ndx]/r[ndx])
    return result

#legacy
def qminuss(x,y,z,gm_max):
    q = circum(x,y,z,gm_max)
    r = radial(x,y,z,gm_max)
    result = []
    for ndx in range(len(r)):
        result.append(q[ndx] - r[ndx])
    return np.array(result)

def qms1(x,y,z,x1,y1,z1,gm_max):
    q = circum_pt(x,y,z,x1,y1,z1,gm_max)
    s = radial1(x,y,z,gm_max)
    return np.array(q)-np.array(s)

def absqminuss(x,y,z,gm_max):
    q = circum(x,y,z,gm_max)
    r = radial(x,y,z,gm_max)
    result = []
    for ndx in range(len(r)):
        result.append(abs(q[ndx] - r[ndx]))
    return np.array(result)






#extimators
gm_max = 70
ex_max = 25
fn = '.\\data\\mega.csv'
mega = load_data(fn)
actuals = mega['b1'][::-1]
x = np.diff(actuals)
y = np.diff(x)
z = np.diff(y)


xyz2 = adj_est(x[0],y[0],z[0],gm_max)
xyz3 = adj_est2(x[0],y[0],z[0],gm_max)
