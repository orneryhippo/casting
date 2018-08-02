
#for the red table
# Red table:
# x based on prior x, for possible range, y, z derived as usual
# x',y',z' derived as usual
# circumQ derived from prior x' and y' and radialS using only redtable x',y' and (0,0)
# Q-S: circumQ - radialS
# err: Q-S - prior impliedRadial
# abqms = abs(Q-S)
# dErr = err - priorErr
# priorErr = impliedCircum - impliedRadial - prior(R2)
# dAbs = redAbs - priorAbs
# priorAbs = abs(lag(S,1)-lag(U,-1))
cols = ['x','y','z',"x'","y'","z'","circumQ","radialS",
        'err', 'abserr', 'dErr', 'priorErr','dAbs','priorAbs']
def base_cols(r_1,x_1,y_1,gm_max):
    x = np.arange(1,gm_max+1)
    x -= r_1
    y = x - x_1
    z = y - y_1
    ae = adj_est(x,y,z,gm_max)
    return np.vstack((x,y,z,ae))

def make_red_table(r_1,x_1,y_1,gm_max):
    bc = base_cols(r_1,x_1,y_1,gm_max)

    return np.vstack(bc)


def er1(x,y,z,x1,y1,z1,gm_max):
    ae = adj_est(x,y,z,gm_max)
    rm = rotn()
    x2 = innerprod([x1,y1,z1],rm[0])
    y2 = innerprod([x1,y1,z1],rm[1])
    print(x2,y2)
    u = length2([x2,y2])
    print(u)
    s = np.zeros(len(ae))
    s.fill(u)
    qms = qms1(x,y,z,x1,y1,z1,gm_max)
    return (np.array(qms)-np.array(s))
