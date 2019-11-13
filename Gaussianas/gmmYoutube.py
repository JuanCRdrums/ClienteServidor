import pandas as pd
import numpy as np
from scipy.stats import multivariate_normal
from sklearn import preprocessing
import time

path = "youtube-new/DEvideos.csv"

colnames = ['category_id','views','likes','dislikes','comment_count']
data = pd.read_csv(path,usecols=colnames,nrows=9000)
#data = pd.read_csv(path)

dataGMM = []
cont = 0
for category_id,views,likes,dislikes,comment_count in zip(data.category_id,data.views,data.likes,data.dislikes,data.comment_count):
    dataGMM.append([cont,category_id,views,likes,dislikes,comment_count])
    cont += 1

scaler = preprocessing.StandardScaler()
scaler.fit(dataGMM)
z = df_scaled_array = scaler.transform(dataGMM)


dataGMMnp = np.array(df_scaled_array)



class GMM:
    def __init__(self,X,number_of_sources,iterations):
        self.iterations = iterations
        self.number_of_sources = number_of_sources
        self.X = X
        self.mu = None
        self.pi = None
        self.cov = None
        self.dim = None
        self.ri_c = None

    def run(self):
        self.reg_cov = 1e-6*np.identity(len(self.X[0])) #región de covarianzas
        #x,y,z,w,a,b = np.meshgrid(np.sort(self.X[:,0]),np.sort(self.X[:,1]),np.sort(self.X[:,2]),np.sort(self.X[:,3]),np.sort(self.X[:,4]),np.sort(self.X[:,5]))
        self.mu = np.random.randint(min(self.X[:,0]),max(self.X[:,0]),size=(self.number_of_sources,len(self.X[0])))
        #Dimensiones = Gaussianas (number_of_sources)*m (numero de datos len(X))
        self.cov = np.zeros((self.number_of_sources,len(self.X[0]),len(self.X[0]))) #matrices de covarianzas
        for dim in range(len(self.cov)):
            np.fill_diagonal(self.cov[dim],5)

        self.pi = np.ones(self.number_of_sources)/self.number_of_sources
        #se inicializan como fracciones


        #E - Step
        for i in range(self.iterations):
            r_ic = np.zeros((len(self.X),len(self.cov)))
            for m,co,p,r in zip(self.mu,self.cov,self.pi,range(len(r_ic[0]))):
                co += self.reg_cov
                mn = multivariate_normal(mean = m,cov = co)
                #print(np.sum([pi_c*multivariate_normal(mean=mu_c,cov=cov_c).pdf(self.X) for pi_c,mu_c,cov_c in zip(self.pi,self.mu,self.cov+self.reg_cov)]))
                r_ic[:,r] = p*mn.pdf(self.X)/np.sum([pi_c*multivariate_normal(mean=mu_c,cov=cov_c).pdf(self.X) for pi_c,mu_c,cov_c in zip(self.pi,self.mu,self.cov+self.reg_cov)],axis=0)


            #M Step
            self.mu = []
            self.cov = []
            self.pi = []
            for c in range(len(r_ic[0])): #itera sobre cada gaussiana
                m_c = np.sum(r_ic[:,c],axis = 0)
                mu_c = (1/m_c)*np.sum(self.X*r_ic[:,c].reshape(len(self.X),1),axis=0)
                self.mu.append(mu_c)
                #según la media nueva, calcular la matriz de covarianzas
                self.cov.append(((1/m_c)*np.dot((np.array(r_ic[:,c]).reshape(len(self.X),1)*(self.X-mu_c)).T,(self.X-mu_c)))+self.reg_cov)
                self.pi.append(m_c/np.sum(r_ic))

        #calculo final:
        for m,co,p,r in zip(self.mu,self.cov,self.pi,range(len(r_ic[0]))):
            co += self.reg_cov
            mn = multivariate_normal(mean = m,cov = co)
            r_ic[:,r] = p*mn.pdf(self.X)/np.sum([pi_c*multivariate_normal(mean=mu_c,cov=cov_c).pdf(self.X) for pi_c,mu_c,cov_c in zip(self.pi,self.mu,self.cov+self.reg_cov)],axis=0)
        self.ri_c = r_ic

tstart = time.time()
nclusters = 6
GMM = GMM(dataGMMnp,nclusters,50)
GMM.run()
tend = time.time()
print("\nTotal elapsed time: %d msec" % ((tend-tstart)*1000))


result = {}
for i in range(nclusters):
    result[i] = []
cont = 0
for row in GMM.ri_c:
    may = -1
    contb = 0
    for cell in row:
        if cell > may:
            may = cell
            pos = contb
            contb += 1

    result[pos].append(cont)
    cont += 1


for k,v in result.items():
    print("Cluster ",k, " = ", v)

print(GMM.ri_c)
