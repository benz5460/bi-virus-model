import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint, solve_ivp
from mpl_toolkits import mplot3d
import math

import random

#calculate strengths and critical value
def calc(n,b1,d1,b2,d2):
    str1 = n*b1/d1
    str2 = n*b2/d2
    print(n,b1,d1,b2,d2)
    print(str1,str2)
    if str1 < str2:
        temp2 = str2
        str2 = str1
        str1 = temp2

    if str1+str2 >=2:
        ecrit = (str1-str2)/(str2*(str1-1))
    if str1+str2 < 2:
        ecrit = 2*(1+(1-str1*str2)**.5)/(str1*str2)
    
    return ecrit

#differential equation function
def si12s(category,t, n, heal_rate, atk_rate, virus_interact):
    i1 = category[0]
    i2 = category[1]
    i12 = category[2]
    s = n - i1 - i2 - i12
    d1 = heal_rate[0]
    d2 = heal_rate[1]
    b1 = atk_rate[0]
    b2 = atk_rate[1]
    e1 = virus_interact[0]
    e2 = virus_interact[1]

    di1dt = b1*s*(i1+i12) + d2*i12 - d1*i1 - e2*b2*i1*(i2+i12)
    di2dt = b2*s*(i2+i12) + d1*i12 - d2*i2 - e1*b1*i2*(i1+i12)
    di12dt = e1*b1*i2*(i1+i12) + e2*b2*i1*(i2+i12) - (d1 + d2)*i12

    return [di1dt, di2dt, di12dt]

b1 = .0006
b2 = .0008
d1 = .2
d2 = .3
n = 300
str1 = n*b1/d1
str2 = n*b2/d2
e_crit = calc(n,b1,d1,b2,d2)

init_category = [50,50,0]
t = np.linspace(0,5000,5001)
vary_e1 = np.array([])
vary_e2 = np.array([])
virus_1 = np.array([])
virus_2 = np.array([])

min_e1_pair = [100,100]
min_e2_pair = [100,100]

curve = set()

for e1 in range(0,151):
    new_row = True
    
    for e2 in range(0,151):

        y = odeint(si12s,init_category,t,args=(n,[d1,d2],[b1,b2],[e1/10,e2/10]))
        virus_1 = np.append(virus_1,(y[5000,0]+y[5000,2]))
        virus_2 = np.append(virus_2,(y[5000,1]+y[5000,2]))
        vary_e1 = np.append(vary_e1,e1/10)
        vary_e2 = np.append(vary_e2,e2/10)


fig = plt.figure()

ax = fig.add_subplot(projection='3d')


ax.scatter(e_crit,e_crit,0,marker='o')
ax.scatter(vary_e1,vary_e2,virus_1,facecolor="r")
ax.scatter(vary_e1,vary_e2,virus_2,facecolor="b")
ax.set_xlabel("e1")
ax.set_ylabel("e2")
ax.set_zlabel("Infected")


plt.show()
