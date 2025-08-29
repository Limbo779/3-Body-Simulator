import numpy as np
from matplotlib import pyplot as plt

# body 1
p1=np.array([1,1])
m1=1
v1=np.array([0,0])

# body 2
p2=np.array([5,1])
m2=1
v2=np.array([0,0])

# body 3
p3=np.array([3,4])
m3=1
v3=np.array([0,0])

# G Const
G=6.67430*(10**(-11))

# managing collision
def collision(x):
    global v1,v2,v3
    # a means v1 and v2
    # b means v1 and v3
    # c means v2 and v3
    if x == "a":
        v1=v1*(-1)
        v2=v2*(-1)   
    elif x == "b":
        v1=v1*(-1)
        v3=v3*(-1)
    else:
        v3=v3*(-1)
        v2=v2*(-1)

