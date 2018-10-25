
#for the blue table
# x = 0
# y = x - red.X vector
# z = y - red.Y vector
# x',y',z' rotated as usual
# circumQ derived from prior x' and y' and redtable x',y'
# radialS using only bluetable x',y' and (0,0)
# Q-S: circumQ - radialS (blue)
# err: Q-S - redtable.radialS
# abqms = abs(Q-S)
# dErr = err - redtable.err
# dAbs = blueAbs - redAbs
# extras: blueAbs - dAbs
# abs(dAbs)
# abs(dErr)
# dE-E+const blue.dE - blue.Err + 5
# 1/2(ERR+dERR)
# Abs - dAbs
# Abs(1/2(ERR-dERR))
# abswav = abs(1/2(ABS+dABS))
# looking for argmins of the x column on absfns
cols = ['x','y','z',"x'","y'","z'","circumQ","radialS",
        'err', 'abserr', 'dErr', 'priorErr','dAbs','priorAbs',
        'absdabs', 'absderr', 'dEE', 'midErrdErr', 'absmdabs', 'abswav']

def er0(x,y,z,gm_max):
    ae = adj_est(x,y,z,gm_max)
    r0 = length2(ae[0])
    qms = qminuss1(x,y,z,gm_max)
    rs = np.zeros(len(qms))
    rs.fill(r0)
    return qms - rs
