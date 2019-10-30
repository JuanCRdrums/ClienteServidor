import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt
from matplotlib import style
style.use('fivethirtyeight')

np.random.seed(0)
x = np.linspace(-5,5,num = 20)
x0 = x*np.random.rand(len(x)) + 10 # Create data cluster 1
x1 = x*np.random.rand(len(x)) - 10 # Create data cluster 2
x2 = x*np.random.rand(len(x)) # Create data cluster 3

x_tot = np.stack((x0,x1,x2)).flatten() #total dataset

c = 3 #number of clusters
r = np.zeros((len(x_tot),c)) #dimmensions: nxc
'''
n = total of points (data)
c = total of clusters (groups or gaussians)
'''

#initial gaussians:
gauss_1 = norm(loc = -5,scale = 5)
gauss_2 = norm(loc = 0,scale = 3)
gauss_3 = norm(loc = 1.5,scale = 1)

for c,g in zip(range(c),[gauss_1,gauss_2,gauss_3]):
    r[:,c] = g.pdf(x_tot) #probabilidad de que los puntos pertenezcan a cada gaussiana



#hace que el total de probabilidades de cada punto dé 1
for i in range(len(r)):
    r[i] = r[i] / np.sum(r,axis = 1)[i]


# M - STEP
m_c = [] #suma de probabilidades de los puntos de cada gaussiana
for c in range(len(r[0])):
    m = np.sum(r[:,c])
    m_c.append(m)

pi_c = [] #la fracción del total de puntos que pertenecen a cada gaussiana
for m in m_c:
    pi_c.append(m/np.sum(m_c))

mu_c = np.sum(x_tot.reshape(len(x_tot),1)*r,axis = 0)/m_c

var_c = [] #nueva matriz de covarianzas
for c in range(len(r[0])):
    var_c.append((1/m_c[c])*np.dot(((np.array(r[:,c]).reshape(60,1))*(x_tot.reshape(len(x_tot),1)-mu_c[c])).T,(x_tot.reshape(len(x_tot),1)-mu_c[c])))
print(var_c)

#ACTUALIZAR LAS GAUSSIANAS
gauss_1 = norm(loc = mu_c[0],scale = var_c[0])
gauss_2 = norm(loc = mu_c[1],scale = var_c[1])
gauss_3 = norm(loc = mu_c[2],scale = var_c[2])


"""Plot the data"""
fig = plt.figure(figsize=(10,10))
ax0 = fig.add_subplot(111)
for i in range(len(r)):
    ax0.scatter(x_tot[i],0,c=np.array([r[i][0],r[i][1],r[i][2]]),s=100)
"""Plot the gaussians"""
for g,c in zip([gauss_1.pdf(np.sort(x_tot).reshape(60,1)),gauss_2.pdf(np.sort(x_tot).reshape(60,1)),gauss_3.pdf(np.sort(x_tot).reshape(60,1))],['r','g','b']):
    ax0.plot(np.sort(x_tot),g,c=c)


plt.show()
