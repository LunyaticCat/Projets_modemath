import numpy as np
import matplotlib.pyplot as plt

#-----------Partie 1-----------

M = np.array([[0, 1, 1, 2, 2, 1, 3, 3, 1.5, 0, 3, 0, 0], [0, 0, 1, 1, 0, 0, 0, 2, 3, 2, 2, 2, 0]])
#Nous transformons la matrice M en matrice homogène noté K
K = np.array([[0, 1, 1, 2, 2, 1, 3, 3, 1.5, 0, 3, 0, 0], [0, 0, 1, 1, 0, 0, 0, 2, 3, 2, 2, 2, 0], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]])

#T Matrice de translation
#1, 0, ux
#0, 1, uy
#0, 0, 1
def trans(ux, uy, K):
    T=[[1,0,ux],[0,1,uy],[0,0,1]]
    RH=np.dot(T,K)
    return RH

#Déplace le centre de la matrice en 0 0
#T Matrice de rotation
#cos(θ), -sin(θ), 0
#sin(θ), cos(θ) , 0
#0     , 0      , 1
#Ramène le centre en xc yc
def rot(xc, yc, teta, K):
    cosTeta = np.cos(teta)
    sinTeta = np.sin(teta)
    RH = trans(-xc, -yc, K)
    T=[[cosTeta,-sinTeta,0],[sinTeta,cosTeta,0],[0,0,1]]
    RH=np.dot(T,RH)
    RH = trans(xc, yc, RH)
    return RH

#Déplace le centre de la matrice en 0 0
#T Matrice d'homothetie
#θ, 0, 0
#0, θ, 0
#0, 0, 1
#Ramène le centre en xc yc
def homo(xc, yc, k, K):
    RH = trans(-xc, -yc, K)
    T=[[k,0 ,0],[0,k,0],[0,0,1]]
    RH=np.dot(T,RH)
    RH = trans(xc, yc, RH)
    return RH

#T Tentative de Matrice de dilatation
#H = u[0]*x + u[1]*y+(xa/u[0])
def dila(xc, yc, lamb, u, v, K):
    Toa = [[u[0], 0, 0],[u[1], 1, 0],[0, 0, 1]]
    Tao = [[-u[0], 0, 0],[-u[1], 1, 0],[0, 0, 1]]
    Math1 = [[u[0],v[0], 0],[u[1], v[1], 0],[0, 0, 1]]
    Homo = [[1, 0, 0], [0, lamb, 0], [0, 0, 1]]
    Math3 = [[-u[1],-v[1], 0],[u[0], v[0], 0],[0, 0, 1]]
    result = np.dot(Tao,K)
    result = np.dot(Math1,result)
    result = np.dot(Homo,result)
    result = np.dot(Math3,result)
    return np.dot(Toa,result)
#-----------Partie 2-----------

O = np.array([[0], [0], [0], [1]])
A = np.array([[1], [0], [0], [1]])
B = np.array([[1], [-1], [0], [1]])
C = np.array([[0], [-1], [0], [1]])
D = np.array([[0], [0], [1], [1]])
E = np.array([[1], [0], [1], [1]])
F = np.array([[1], [-1], [1], [1]])
G = np.array([[0], [-1], [1], [1]])
K3D=np.concatenate((O,A,B,C,O,D,E,A,E,F,B,F,G,D,O,B,A,C),axis=1)

#Converti un matrice K 3D et retourne une matrice 2D
#soit d la distance de la camera
def convertTo2D(dCamera, K):
    print(K)
    convertMat = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, -1/dCamera, 1]])
    print(convertMat)
    return np.dot(convertMat, K)

#T Matrice de translation
#1, 0, 0, ux
#0, 1, 0, uy
#0, 0, 1, uz
#0, 0, 0, 1
def trans3D(ux, uy, uz, K):
    T=[[1, 0, 0, ux],[0, 1, 0, uy],[0, 0, 1, uz], [0, 0, 0, 1]]
    RH=np.dot(T,K)
    return RH

#Déplace le centre de la matrice en 0 0 0
#T Matrice d'homothetie
#θ, 0, 0, 0
#0, θ, 0, 0
#0, 0, θ, 0
#0, 0, 0, 1
#Ramène le centre en xo yo, zo
def homo3D(xo, yo, zo, rap, K):
    K3D = trans3D(-xo, -yo, -zo, K)

    T= np.array([[rap, 0, 0, 0], [0, rap, 0, 0], [0, 0, rap, 0], [0, 0, 0, 1]])
    K3D = np.dot(T, K3D)
    return trans3D(xo, yo, zo, K3D)

#Déplace le centre de la matrice en 0 0 0
#T Matrice de rotation en Z
#cos(θ), -sin(θ), 0, 0
#sin(θ), cos(θ) , 0 ,0
#0     , 0      , 1, 0
#0     , 0      , 0, 1
#Ramène le centre en xo yo zo
def rotateZ3D(xo, yo, zo, teta, K):
    cosT = np.cos(teta)
    sinT = np.sin(teta)

    KH = trans3D(-xo, -yo, -zo, K)
    
    T= np.array([[cosT, -sinT, 0, 0], [sinT, cosT, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
    
    KH = np.dot(T, KH)

    return trans3D(xo, yo, zo, KH)

#Déplace le centre de la matrice en 0 0 0
#T Matrice de rotation en Y
#cos(θ) , 0        , sin(θ), 0
#0      , 1        , 0     , 0
#-sin(θ), 0        , cos(θ), 0
#0      , 0        , 0     , 1
#Ramène le centre en xo yo zo
def rotateY3D(xo, yo, zo, teta, K):
    cosT = np.cos(teta)
    sinT = np.sin(teta)

    KH = trans3D(-xo, -yo, -zo, K)
    
    T= np.array([[cosT, 0, sinT, 0], [0, 1, 0, 0], [-sinT, 0, cosT, 0], [0, 0, 0, 1]])
    
    KH = np.dot(T, KH)

    return trans3D(xo, yo, zo, KH)

#Déplace le centre de la matrice en 0 0 0
#T Matrice de rotation en X
#1      , 0     , 0      , 0
#0      , cos(θ), -sin(θ), 0
#0      , sin(θ), cos(θ) , 0
#0      , 0     , 0      , 1
#Ramène le centre en xo yo zo
def rotateX3D(xo, yo, zo, teta, K):
    cosT = np.cos(teta)
    sinT = np.sin(teta)

    KH = trans3D(-xo, -yo, -zo, K)
    
    T= np.array([[1, 0, 0, 0], [0, cosT, -sinT, 0], [0, sinT, cosT, 0], [0, 0, 0, 1]])
    
    KH = np.dot(T, KH)

    return trans3D(xo, yo, zo, KH)

#-----------Rendering2D-----------    

#Render une transformation
def renderer(title, RH):
    #Rend le repère orthonormé
    ax = plt.gca()
    ax.set_aspect('equal', adjustable='box')

    plt.title(title)
    plt.plot(K[0,:],K[1,:],RH[0,:],RH[1,:])
    plt.axis([-8,8,-8,8])
    plt.show()

#Affiche la matrice M ainsi que sa translation RH de -3 -3
RH = trans(-3, -3, K)
renderer('Translation de la Matrice M', RH)

#Affiche la matrice M ainsi que sa rotation RH de pi/3 et de centre de rotation 1.5, 1.5
RH = rot(1.5, 1.5, np.pi/3, K)
renderer('Rotation de la Matrice M', RH)

#Affiche la matrice M ainsi que son homothetie de centre 1.5, 1.5 et de rapport 2
RH = homo(1.5, 1.5, 2, K)
renderer('Homothétie de la Matrice M', RH)

#Affiche la matrice M ainsi qu'une tententative de dilatation RH
RH = dila(1.5, 1.5, 2, (1,0), (0,1), K)
renderer('Tentative de Dilatation de la Matrice M', RH)

#-----------Rendering 3D-----------

def renderer3D(title, RH3D):
    #Rend le repère orthonormé
    ax = plt.gca()
    ax.set_aspect('equal', adjustable='box')

    plt.title(title)
    plt.plot(K3D[0,:],K3D[1,:],RH3D[0,:],RH3D[1,:])
    plt.axis([-8,8,-8,8])
    plt.show()

#Affiche la matrice K ainsi que son homothetie de centre 0, 0, 0 et de rapport 2
RH3D = homo3D(0, 0, 0, 2, K3D)
renderer3D("Homothétie de la Matrice K", RH3D)

#Affiche la matrice K ainsi que sa translation de 4, 4, 0
RH3D = trans3D(4, 4, 0, K3D)
renderer3D("Translation de la Matrice K", RH3D)

#Pour les rotations, une translation 4, 4, 0 a étais effectué pour aider à la lisibilité.
#Affiche la matrice K ainsi que sa rotation de centre 0, 0, 0 et d'axe X
RH3D = trans3D(4, 4, 0, K3D)
RH3D = rotateX3D(0, 0, 0, np.pi/6, RH3D)
renderer3D("Rotation de la Matrice K sur l'axe X", RH3D)

#Affiche la matrice K ainsi que sa rotation de centre 0, 0, 0 et d'axe Y
RH3D = trans3D(4, 4, 0, K3D)
RH3D = rotateY3D(0, 0, 0, np.pi/6, RH3D)
renderer3D("Rotation de la Matrice K sur l'axe Y", RH3D)

#Affiche la matrice K ainsi que sa rotation de centre 0, 0, 0 et d'axe Z
RH3D = trans3D(4, 4, 0, K3D)
RH3D = rotateZ3D(0, 0, 0, np.pi/6, RH3D)
renderer3D("Rotation de la Matrice K sur l'axe Z", RH3D)