import matplotlib.pyplot as plt
from matplotlib import style
style.use('fivethirtyeight')
from sklearn.datasets.samples_generator import make_blobs
import numpy as np
from scipy.stats import multivariate_normal

#Create dataset
X,Y = make_blobs(cluster_std=1.5,random_state=20,n_samples=500,centers=3)
X = np.dot(X,np.random.RandomState(0).randn(2,2))


class GMM:
    def __init__(self,X,number_of_sources,iterations):
        self.iterations = iterations
        self.number_of_sources = number_of_sources
        self.X = X
        self.mu = None
        self.pi = None
        self.cov = None
        self.XY = None

    def run(self):
        self.reg_cov = 1e-6*np.identity(len(self.X[0])) #región de covarianzas
        x,y = np.meshgrid(np.sort(self.X[:,0]),np.sort(self.X[:,1]))
        self.XY = np.array([x.flatten(),y.flatten()]).T

        #Valores iniciales:
        self.mu = np.random.randint(min(self.X[:,0]),max(self.X[:,0]),size=(self.number_of_sources,len(self.X[0])))
        #Dimensiones = Gaussianas (number_of_sources)*m (numero de datos len(X))
        self.cov = np.zeros((self.number_of_sources,len(X[0]),len(X[0]))) #matrices de covarianzas

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
                r_ic[:,r] = p*mn.pdf(self.X)/np.sum([pi_c*multivariate_normal(mean=mu_c,cov=cov_c).pdf(X) for pi_c,mu_c,cov_c in zip(self.pi,self.mu,self.cov+self.reg_cov)],axis=0)


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
            r_ic[:,r] = p*mn.pdf(self.X)/np.sum([pi_c*multivariate_normal(mean=mu_c,cov=cov_c).pdf(X) for pi_c,mu_c,cov_c in zip(self.pi,self.mu,self.cov+self.reg_cov)],axis=0)
        print(r_ic)



GMM = GMM(X,3,50)
GMM.run()
