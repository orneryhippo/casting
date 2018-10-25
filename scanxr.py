def memoize(f):
    memo = {}
    def helper(x):
        if x not in memo:
            memo[x] = f(x)
        return memo[x]
    return helper

@memoize
def is_prime(n):
    """"pre-condition: n is a nonnegative integer
    post-condition: return True if n is prime and False otherwise."""
    if n < 2:
         return False;
    if n % 2 == 0:
         return n == 2  # return False
    k = 3
    while k*k <= n:
         if n % k == 0:
             return False
         k += 2
    return True


rems = []
rs = [0,2,3,5,7,10,12,17,18,23,25,28,30,32,33]
rcounts = {}
for r in rs:
    rcounts[r] = 0

def countem(ct = 100):
    for r in rs:
        rcounts[r] = 0
    for x in range(1,ct+1):
        for r in rs:
            p1 = 6*(35*x+r)-1
            p2 = 6*(35*x+r)+1
            if is_prime(p1) and is_prime(p2):
                #rems.append((r,x))
                #print(rcounts[r], rcounts[r] + 1)
                rcounts[r] += 1
    s = 0
    for i,x in rcounts.items():
        s += x
    return (ct,s)

def gendata(ct=100):
    with open('rems2.csv','w+') as rfile:
        rfile.write("X,r0,r2,r3,r5,r7,r10,r12,r17,r18,r23,r25,r28,r30,r32,r33,count\n")
        for x in range(ct):
            rfile.write(str(x) + ",")
            ps = 0
            for r in rs:
                p1 = 6*(35*x+r)-1
                p2 = 6*(35*x+r)+1
                if is_prime(p1) and is_prime(p2):
                    rfile.write(str(r)+",")
                    ps += 1
                else:
                    rfile.write(",")
            rfile.write(str(ps))
            rfile.write("\n")


# for i in range(6):
#     ct,s = countem(10**i)
#     print(s/ct,ct,s)

# with open('rems.csv','w+') as rfile:
#     for r in rems:
#         rfile.write(str(r[0]) + "," + str(r[1]))
#         rfile.write("\n")
#print(rems)
