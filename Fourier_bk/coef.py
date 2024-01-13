import svgpathtools
import numpy as np
import matplotlib.pyplot as plt

def svg_to_coef(path_to_file,nvec=2000,npoint=10000,npath=0,conj=True,reverse=False):
    
    path,_=svgpathtools.svg2paths(path_to_file)
    path=path[npath]

    points=np.linspace(0,1,npoint,endpoint=False)
    pathvals=np.zeros_like(points,dtype="complex")
    pathlength=path.length()
    if reverse:
        for i in range(len(points)):
            pathvals[i]=path.point(path.ilength(pathlength-pathlength*points[i]))
    else:
        for i in range(len(points)):
            pathvals[i]=path.point(path.ilength(pathlength*points[i]))
    if conj==True:
        pathvals=np.conj(pathvals).copy()
    coefs=list(range(nvec // 2, -nvec// 2, -1))
    coefs.sort(key=abs)
    fourier_coef=np.zeros(nvec,dtype="complex")
    points*=2*np.pi
    for i in range(len(coefs)):
        coef=coefs[i]
        exponent=np.exp(1j*coef*points)
        fourier_coef[i]=np.trapz(np.multiply(exponent,pathvals),points)/(2*np.pi)
    coefs=np.array(coefs)
    return coefs,fourier_coef

#Plot coef can plot coefficients as the fourier sum path
def plot_coef(coefs,fourier_coef,npoint=10000,endpoint=True):
    points=np.linspace(0,2*np.pi,npoint,endpoint=endpoint)
    vals=np.zeros_like(points,dtype="complex")
    for i in range(len(coefs)):
        vals=vals+fourier_coef[i]*np.exp(1j*coefs[i]*points)
    plt.plot(vals.real[:npoint//5],vals.imag[:npoint//5],"r-",linewidth=1,)
    plt.plot(vals.real[npoint//5:],vals.imag[npoint//5:],"b-",linewidth=1,)
    #plt.plot([vals.real[0],vals.real[100]],[vals.imag[0],vals.imag[100]],"r-")
    #plt.plot([vals.real[100],vals.real[200]],[vals.imag[100],vals.imag[200]],"g-")
    #plt.plot([vals.real[200],vals.real[300]],[vals.imag[200],vals.imag[300]],"b-")

"""
画出来的图显得有点小
可以通过调整coef_scale来放大
"""
coef_scale = 5
def save_coef(coefs,fourier_coef,file_path):
    f=open(file_path,"w")
    for i in range(len(coefs)):
        f.write("{} {}".format(coefs[i],coef_scale*fourier_coef[i]))
        if i<len(coefs)-1:
            f.write("\n")

if __name__ == "__main__":
    coefs,fourier_coef = svg_to_coef("A.svg")
    save_coef(coefs,fourier_coef,"A.txt")