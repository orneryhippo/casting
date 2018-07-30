import math
import numpy as np
import pandas as pd
from random import random, randint
from math import cos, sin, sqrt, radians, atan2

#yaw matrix
def xy(angle):
    m = np.zeros([3,3])
    c = cos(radians(angle))
    s = sin(radians(angle))
    m[0][0] = m[1][1] = c
    m[1][0] = -s
    m[0][1] = s
    m[2][2] = 1
    return m

#pitch matrix
def yz(angle):
    m = np.zeros([3,3])
    c = cos(radians(angle))
    s = sin(radians(angle))
    m[2][2] = m[1][1] = c
    m[2][1] = -s
    m[1][2] = s
    m[0][0] = 1
    return m

#roll matrix
def xz(angle):
    m = np.zeros([3,3])
    c = cos(radians(angle))
    s = sin(radians(angle))
    m[2][2] = m[0][0] = c
    m[2][0] = -s
    m[0][2] = s
    m[1][1] = 1
    return m


def rotn(y=45,p=-45,r=0):
    yaw   = xz(y)
    pitch = yz(p)
    roll  = xy(r)
    return ((xz(y)@yz(p))@xy(r)).T

def randrot():
    return rotn(random()*360,rand()*360,rand()*360)

def euc(p1,p2=None):
    if type(p2)==type(None):
        p2 = np.zeros(len(p1))
    v = p1-p2
    return sqrt(v@v)

def euc2(p1,p2=None):
    if type(p2)==type(None):
        p2 = np.zeros(len(p1))
    v = p1[:2]-p2[:2]
    return sqrt(v@v)

def angle(x,y):
    return atan2(x,y)

# vector functions, vector(s) in, vector out
#column U implied radial length
def irl2(vec):
    return np.array(list(map(euc2,vec)))

#called column S, implied circumferential length, pass in two refs to same vect, offset
def icl2(vec1, vec2):
    return np.array(list(map(euc2,vec1,vec2)))

#column S minus column U
# ||Circum|| - ||Radial||
def smu(vec1,vec2):
    v1 = adj_data(vec1)
    v2 = adj_data(vec2)
    icl = icl2(v1,v2)
    irl = irl2(v1)
    return icl - irl


def load_data(fn ):
    game_data = pd.read_csv(fn, names=['Date','gm','b1', 'b2', 'b3', 'b4', 'b5','wc'])
    return game_data


def adj_data(vec):
    rotmat=rotn()
    xyz2 = rotmat @ np.array(vec)
    return xyz2.T

def raw2xyz(raw, scale=1):
    data = raw[::scale]
    x = np.diff(data)
    y = np.diff(x)
    z = np.diff(y)
    return np.vstack((x[:len(z)],y[:len(z)],z)).T

def mag(vec):
    return np.array(list(map(euc2,vec)))

def magR3(vec):
    return np.array(list(map(euc,vec)))

##### for estimates ################################################
# red box
def est1(xf,yf,zf, gm = 70):
    x = np.arange(1-xf,gm+1-xf)
    y = x - yf
    z = y - zf
    e1xyzp = np.vstack((x[:len(z)],y[:len(z)],z))
    return e1xyzp.T
    #e1xyzpr = e1xyzp @ rotn().T
    #return e1xyzpr

# red box
def est1r(xf,yf,zf, gm = 70):
    e1 = est1(xf,yf,zf, gm = 70)
    return e1 @ rotn().T

# blue box
def est2(e1):
    x = np.zeros(len(e1))
    y = x - e1.T[0]
    z = y - e1.T[1]
    e2xyzp = np.vstack((x[:len(z)],y[:len(z)],z))
    return e2xyzp.T
    #e2xyzpr = e2xyzp @ rotn().T
    #return e2xyzpr

# blue box
def q1(j,k,e1):
    x = np.ones(len(e1))*j
    y = np.ones(len(e1))*k
    z = np.ones(len(e1))
    vec2 = np.vstack((x,y,z)).T
    e1a = e1 @ rotn().T
    return np.array(list(map(euc2,e1a,vec2)))



def s1(e1):
    e1a = e1 @ rotn().T
    return np.array(list(map(euc2,e1a)))

def qms1(q,s):
    return q-s

def er1(u, qms):
    uvec = np.ones(len(qms))*u
    return qms - uvec
    #return est_sub_x(qms,u)

def derr1(er,af):
    #af_vec = np.ones(len(er))*af
    #return er-af_vec
    return est_sub_x(er,af)

def est_sub_x(vec,val):
    val_vec = np.ones(len(vec))*val
    return vec - val_vec

def est_sub_y(vec,val):
    val_vec = np.ones(len(vec))*val
    return val_vec - vec



##### testing ########################################################
def test_adj(eps = 10**-12):
    g = load_data('.\\data\\mega.csv')
    b = g['b1']
    raw = raw2xyz(b)
    adj = adj_data(xyz.T).T
    for ndx in range(len(raw)):
        assert(abs(euc(raw[ndx]) - euc(adj[ndx])) < eps), "failed on index %d" % (ndx)

def test_size_invariance():
    testr(vec=np.array([1.,0.,0.]))
    testr(vec=np.array([0.,1.,0.]))
    testr(vec=np.array([0.,0.,1.]))
    for i in range(100):
        testr(ntimes=100,vec=np.random.random([3]))

def testr(ntimes=10000, vec=np.array([1.,0.,0.])):
    eps = 10**-15
    x = np.array([1,0,0])
    mx = euc(x)+eps
    mn = euc(x)-eps
    for i in range(ntimes):
        r = randrot()
        xp = r.T@x
        norm = euc(xp)
        assert(norm < mx),'too big %d, %f, %s' % (i,norm,str(vec))
        assert(norm > mn), 'too small %d, %f, %s' % (i,norm,str(vec))

def test_unrot():
    for i in range(10000):
        test_unroty()
        test_unrotp()
        test_unrotr()


def test_unrotr():
    eps = 10**-15
    angle = 360*np.random.random()
    v = np.random.random([3])
    v1 = rotn(r=angle,p=0,y=0)@v
    v2 = rotn(r=-angle,p=0,y=0)@v1
    assert(euc3(v-v2) < eps)

def test_unroty():
    eps = 10**-15
    angle = 360*np.random.random()
    v = np.random.random([3])
    v1 = rotn(y=angle,p=0,r=0)@v
    v2 = rotn(y=-angle,p=0,r=0)@v1
    assert(euc3(v-v2) < eps)

def test_unrotp():
    eps = 10**-15
    angle = 360*np.random.random()
    v = np.random.random([3])
    v1 = rotn(p=angle,y=0,r=0)@v
    v2 = rotn(p=-angle,y=0,r=0)@v1
    assert(euc3(v-v2) < eps)
