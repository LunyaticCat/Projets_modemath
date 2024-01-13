# This is a sample Python script.

# Press Maj+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import numpy as np
import matplotlib.pyplot as plt


def rebond(vectorNormal, vectorVitesseIni):
    """
    Renvois le vecteur vitesse du projectile après un robond sur l'obstacle

    Parameters
    ----------
    vectorVitesseIni : vecteur VE
    vectorNormal : vecteur directeur de la droite qui passe par le centre des deux objets
    """

    l = vectorVitesseIni[0] * vectorNormal[0] + vectorVitesseIni[1] * vectorNormal[1]

    vectorP = (-l * vectorNormal[0], -l * vectorNormal[1])

    vectorQ = vectorP + vectorVitesseIni

    vectorVitesseFinal = vectorQ + vectorP

    return vectorVitesseFinal


np.arange(0, 2, 0.5)
dt = 0.02
nImage = 10000

x = np.array([0, 1, 1, 0, 0])
y = np.array([0, 0, 1, 1, 0])

center = (1, 1)
centerObs1 = (4, 2)
centerObs2 = (2, 5)
centerObs3 = (6, 8)

rayon = 0.5
rayonObs = 1

teta = np.linspace(0, 2 * np.pi, 21)
circle = (center[0] + rayon * np.cos(teta), center[1] + rayon * np.sin(teta))

obstacle1 = (centerObs1[0] + rayonObs * np.cos(teta), centerObs1[1] + rayonObs * np.sin(teta))
obstacle2 = (centerObs2[0] + rayonObs * np.cos(teta), centerObs2[1] + rayonObs * np.sin(teta))
obstacle3 = (centerObs3[0] + rayonObs * np.cos(teta), centerObs3[1] + rayonObs * np.sin(teta))

vector = (9, 4)

ax = plt.gca()
ax.set_aspect('equal', adjustable='box')

for i in range(nImage):
    if i == 0:
        line, line2, line3, line4 = plt.plot(circle[0], circle[1], obstacle1[0], obstacle1[1], obstacle2[0],
                                             obstacle2[1], obstacle3[0], obstacle3[1])
        plt.axis([-1, 10, -1, 10])


    else:
        center = (center[0] + vector[0] * dt, center[1] + vector[1] * dt)
        circle = (circle[0] + vector[0] * dt, circle[1] + vector[1] * dt)

        if center[1] + rayon >= plt.axis()[1] or center[1] + rayon <= plt.axis()[2] + 1:
            vector = (vector[0], -vector[1])

        if center[0] + rayon <= plt.axis()[0] + 1 or center[0] + rayon >= plt.axis()[3]:
            vector = (-vector[0], vector[1])

        distanceReel1 = np.sqrt(np.square((centerObs1[0] - center[0])) + np.square((centerObs1[1] - center[1])))

        vectorNormal1 = ((center[0] - centerObs1[0]) / distanceReel1,
                         (center[1] - centerObs1[1]) / distanceReel1)

        distanceReel2 = np.sqrt(np.square((centerObs2[0] - center[0])) + np.square((centerObs2[1] - center[1])))

        vectorNormal2 = ((center[0] - centerObs2[0]) / distanceReel2,
                         (center[1] - centerObs2[1]) / distanceReel2)

        distanceReel3 = np.sqrt(np.square((centerObs3[0] - center[0])) + np.square((centerObs3[1] - center[1])))

        vectorNormal3 = ((center[0] - centerObs3[0]) / distanceReel3,
                         (center[1] - centerObs3[1]) / distanceReel3)

        if distanceReel1 <= rayon + rayonObs:
            vector = rebond(vectorNormal1, vector)

        if distanceReel2 <= rayon + rayonObs:
            vector = rebond(vectorNormal2, vector)

        if distanceReel3 <= rayon + rayonObs:
            vector = rebond(vectorNormal3, vector)

    line.set_data(circle)
    plt.pause(dt)
