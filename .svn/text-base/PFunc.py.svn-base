# Various functions used for the PLine drawing processes

import math
import random

def RandomColor():
    R=random.random()
    G=random.random()
    B=random.random()
    tk_rgb = "#%02x%02x%02x" % (255*R/2+128, 255*G/2+128, 255*B/2+128)
    return tk_rgb

def RotateCoord(coord, angle):
    newx=coord[0]*math.cos(angle) + coord[1]*math.sin(angle)
    newy=-coord[0]*math.sin(angle) + coord[1]*math.cos(angle)
    return (newx, newy)

def PointDistance(coord0, coord1):
    return math.sqrt((coord0[0]-coord1[0])**2+(coord0[1]-coord1[1])**2)

def LineDistance(coord0, coord1, coorde):
    if coord1[0]==coord0[0]:
        if coord1[1]<coord0[1]:
            coordlow=coord1[1]
            coordhigh=coord0[1]
        elif coord0[1]<coord1[1]:
            coordlow=coord0[1]
            coordhigh=coord1[1]
        else:
            coordlow=coordhigh=coord0[1]
            
        if coorde[1]<coordlow or coorde[1]>coordhigh:
            dist=-1
        else:
            dist=abs(coorde[0]-coord0[0])
        xint=coord0[0]
        yint=coorde[1]

    elif coord1[1]==coord0[1]:
        if coord1[0]<coord0[0]:
            coordlow=coord1[0]
            coordhigh=coord0[0]
        elif coord0[0]<coord1[0]:
            coordlow=coord0[0]
            coordhigh=coord1[0]
        else:
            coordlow=coordhigh=coord0[0]

        if coorde[0]<coordlow or coorde[0]>coordhigh:
            dist=-1
        else:
            dist=abs(coorde[1]-coord0[1])
        xint=coorde[0]
        yint=coord0[1]

    else:
        m=float(coord1[1]-coord0[1])/(coord1[0]-coord0[0])
        b=coord0[1]-m*coord0[0]
        me=-1.0/m
        be=coorde[1]-me*coorde[0]
        xint=(be-b)/(m-me)
        yint=m*xint+b

        between=IsInBetween(coord0, coord1, (xint, yint))

        if between:
            dist=math.sqrt((coorde[0]-xint)**2 + (coorde[1]-yint)**2)
        else:
            dist=-1

    return dist, (xint, yint)

def IsInBetween(coord0, coord1, coord2):
    if coord1[0]<coord0[0]:
        coordxlow=coord1[0]
        coordxhigh=coord0[0]
    else:
        coordxlow=coord0[0]
        coordxhigh=coord1[0]

    if coord1[1]<coord0[1]:
        coordylow=coord1[1]
        coordyhigh=coord0[1]
    else:
        coordylow=coord0[1]
        coordyhigh=coord1[1]

    if coordxlow<=coord2[0]<=coordxhigh and coordylow<=coord2[1]<=coordyhigh:
        return True
    else:
        return False
