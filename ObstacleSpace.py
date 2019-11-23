# -*- coding: utf-8 -*-
"""
Created on Sun Mar 24 23:59:10 2019

@author: balam
"""

import matplotlib.pyplot as plt
import numpy as np
import copy
import math
#import MapDiaplay as md

def line(pt1,pt2):
    (x1,y1) = pt1
    (x2,y2) = pt2
#    print("p1: " , pt1, " pt2: ", pt2)
    a = y2-y1
    b = -(x2-x1)
    c = y1*(x2-x1) - x1*(y2-y1)
    return(a,b,c)
    
def rightofLine(line, pt):
    (a,b,c) = line
    (x,y) = pt
    return a*x + b*y + c <= 0
    
def insideCircle(r,center,pt):
    (x1,y1) = center
    (x,y) = pt
    return (x-x1)**2 + (y-y1)**2 - r**2 <= 0

def insideElipse(axis, center, pt):
    (a,b) = axis
    (x1,y1) = center
    (x,y) = pt
    return ((x-x1)**2 / a**2) + ((y-y1)**2 / b**2) - 1 <= 0

def triangle(pts):
    pt1 = pts[0]
    pt2 = pts[1]
    pt3 = pts[2]
    lines = [];
    for pt in [(pt1,pt2,pt3),(pt2,pt3,pt1),(pt3,pt1,pt2)]:
        lines.append((line(pt[0],pt[1]),rightofLine(line(pt[0],pt[1]), pt[2])))
    return lines

def insideTriangle(lines,pt):
    return all([rightofLine(line[0],pt) == line[1] for line in lines])

def gridAdjustments(values,fntns,gSize):
    adjustedValues = copy.deepcopy(values)
    for val,fntn,ndx in zip(values,fntns,range(len(values))):
        if (isinstance(val, list)):
            for val_,fntn_,ndx_ in zip(val,fntn,range(len(val))):
                val_ = val_/gSize
                adjustedValues[ndx][ndx_] = fntn_(val_)
        else:
            val = val/gSize
            adjustedValues[ndx] = fntn(val)
    return adjustedValues

def genObstacleSpace(xMax, yMax, gridSize , botRadius, clearance):
#    gridSize = 1
    
    # Square
    t1 = [[50,67.5],[100,67.5],[100,112.5]]
    t1Adj = ((lambda x:math.floor(x),lambda x:math.floor(x)),
             (lambda x:math.ceil(x) ,lambda x:math.floor(x)),
             (lambda x:math.ceil(x) ,lambda x:math.ceil(x) ))
    t2 = [[50,67.5],[100,112.5],[50,112.5]]
    t2Adj = ((lambda x:math.floor(x),lambda x:math.floor(x)),
             (lambda x:math.ceil(x) ,lambda x:math.ceil(x) ),
             (lambda x:math.floor(x),lambda x:math.ceil(x) ))
    # convex Polygon
    t3 = [[125,56],[150,15],[163,52]]
    t3Adj = ((lambda x:math.floor(x),lambda x:math.ceil(x) ),
             (lambda x:math.floor(x),lambda x:math.floor(x)),
             (lambda x:round(x)     ,lambda x:math.ceil(x) ))
    t4 = [[150,15],[173,15],[163,52]]
    t4Adj = ((lambda x:math.floor(x),lambda x:math.floor(x)),
             (lambda x:math.ceil(x) ,lambda x:math.floor(x)),
             (lambda x:round(x)     ,lambda x:math.ceil(x) ))
    t5 = [[173,15],[193,52],[163,52]]
    t5Adj = ((lambda x:math.ceil(x) ,lambda x:math.floor(x)),
             (lambda x:math.ceil(x) ,lambda x:round(x)     ),
             (lambda x:round(x)     ,lambda x:math.ceil(x) ))
    t6 = [[193,52],[170,90],[163,52]]
    t6Adj = ((lambda x:math.ceil(x) ,lambda x:round(x)     ),
             (lambda x:round(x)     ,lambda x:math.ceil(x) ),
             (lambda x:round(x)     ,lambda x:math.ceil(x) ))
    
    c1 = [15,[190,130]]
    c1Adj = [lambda x:math.ceil(x),
             [lambda x:round(x),lambda x:round(x)]]
    c1 = gridAdjustments(c1,c1Adj,gridSize)
    
    e1 = [[15,6],[140,120]]
    e1Adj = ((lambda x:math.ceil(x) ,lambda x:math.ceil(x) ),
             (lambda x:round(x)     ,lambda x:round(x)     ))
    e1 = gridAdjustments(e1,e1Adj,gridSize)
        
    obsTri = [gridAdjustments(t,f,gridSize) for t,f in zip([t1,t2,t3,t4,t5,t6],
                                                  [t1Adj,t2Adj,t3Adj,t4Adj,t5Adj,t6Adj])]
    
#    xMax = 250
#    yMax = 150
    xMax = math.floor(xMax/gridSize)
    yMax = math.floor(yMax/gridSize)
    
#    mapDisp = md.dispMap((xMax,yMax))
    
    obs = np.zeros((xMax,yMax))
    triLines = [triangle(t) for t in obsTri]
    for x in range(0,xMax):
        for y in range(0,yMax):
#            triObs = any([insideTriangle(triangle(t),(x,y)) for t in obsTri])
            triObs = any([insideTriangle(triLine,(x,y)) for triLine in triLines])
            obs[x][y] = insideCircle(c1[0],c1[1],(x,y)) or insideElipse(e1[0],e1[1],(x,y)) or triObs
#    plt.matshow(np.flipud(obs.T))
#    plt.show()
    
    obsPts = np.nonzero(obs)
    obsSet = set([(x,y) for x,y in zip(obsPts[0],obsPts[1])])
    
#    botRadius = 5
#    botRadius = math.ceil(botRadius/gridSize)
    botSize = round(2*botRadius if(2*botRadius % 2 != 0) else (2*botRadius)+1)
    botCenter = round(botSize/2)
    cB = [botRadius,[botCenter,botCenter]]
    cB_adj = [lambda x:math.ceil(x),
             [lambda x:round(x),lambda x:round(x)]]
    cB = gridAdjustments(cB,cB_adj,gridSize)
#    bot = np.zeros((botSize+1,botSize+1))
    bot = np.zeros((cB[0]*2+3 , cB[0]*2+3))
    for x in range(0, bot.shape[0]):
        for y in range(0, bot.shape[1]):
            bot[x][y] = insideCircle(cB[0],cB[1],(x,y))
    #        bot[x][y] = insideTriangle(triangle(tB),(x,y))
    
    bot = bot[~np.all(bot == 0, axis=1)]
    bot = bot.T
    bot = bot[~np.all(bot == 0, axis=1)]
    bot = bot.T

#    print(f"{cB} : {bot.shape} : {botSize} : {botCenter}")
    
#    bot = np.flipud(np.fliplr(bot))
#    plt.matshow(np.flipud(bot.T))
#    plt.show()
    botPts = np.nonzero(bot)
    botSet = set([(x,y) for x,y in zip(botPts[0],botPts[1])])
    
    
    
#    clearance = 0
#    clearance = math.ceil(clearance/gridSize)
    clearanceSize = round(2*(botRadius+clearance) if(2*(botRadius+clearance) % 2 != 0) else (2*(botRadius+clearance))+1)
    clearanceCenter = round(clearanceSize/2)
    cC = [botRadius+clearance,[clearanceCenter,clearanceCenter]]
    cC_adj = [lambda x:math.ceil(x),
             [lambda x:round(x),lambda x:round(x)]]
    cC = gridAdjustments(cC,cC_adj,gridSize)
    clear = np.zeros((cC[0]*2+3,cC[0]*2+3))
    for x in range(0,clear.shape[0]):
        for y in range(0,clear.shape[1]):
            clear[x][y] = insideCircle(cC[0],cC[1],(x,y))
    
    clear = clear[~np.all(clear == 0, axis=1)]
    clear = clear.T
    clear = clear[~np.all(clear == 0, axis=1)]
    clear = clear.T

#    print(f"{cC} : {clear.shape} : {clearanceSize} : {clearanceCenter}")
    
#    plt.matshow(np.flipud(clear.T))
#    plt.show()
    clrPts = np.nonzero(clear)
    clrSet = set([(x,y) for x,y in zip(clrPts[0],clrPts[1])])
    
    sumBotSet = copy.deepcopy(obsSet)
    for off in obsSet:
        offsetBotSet = set([((pt[0]+off[0]-cB[1][0]),(pt[1]+off[1]-cB[1][1])) for pt in botSet])
        sumBotSet |= offsetBotSet
    
    sumClrSet = copy.deepcopy(obsSet)
    for off in obsSet:
        offsetClrSet = set([((pt[0]+off[0]-cC[1][0]),(pt[1]+off[1]-cC[1][1])) for pt in clrSet])
        sumClrSet |= offsetClrSet
    
    minkowskiBotSum = copy.deepcopy(obs)
    for pt in sumBotSet:
        if ((pt[0]<xMax and pt[1]<yMax) and (pt[0]>=0 and pt[1]>=0)):
            minkowskiBotSum[pt[0]][pt[1]] = 1.0
#    plt.matshow(np.flipud((minkowskiBotSum+obs).T))
#    plt.show()    
    
    minkowskiClrSum = copy.deepcopy(obs)
    for pt in sumClrSet:
        if ((pt[0]<xMax and pt[1]<yMax) and (pt[0]>=0 and pt[1]>=0)):
            minkowskiClrSum[pt[0]][pt[1]] = 1.0

    edgeClearance = np.zeros(minkowskiClrSum.shape)
    
    if (cC[0] > 0):
        for i in range(cC[0]):
            edgeClearance[i] = np.ones(edgeClearance.shape[1])
            edgeClearance[-i-1] = np.ones(edgeClearance.shape[1])
        edgeClearance = edgeClearance.T
        for i in range(cC[0]):
            edgeClearance[i] = np.ones(edgeClearance.shape[1])
            edgeClearance[-i-1] = np.ones(edgeClearance.shape[1])
        edgeClearance = edgeClearance.T
#        plt.matshow(np.flipud(edgeClearance.T))
#        plt.show()
    
    minkowskiClrSum = minkowskiClrSum + edgeClearance

#    plt.matshow(np.flipud((minkowskiClrSum+obs).T))
#    plt.show()
#    
#    plt.matshow(np.flipud((minkowskiClrSum+minkowskiBotSum+obs).T))
#    plt.show() 
    
            
#    obstacleSet = set()
    obstaclePoints = np.nonzero(minkowskiClrSum)
    obstacleSet = {(x,y) for x,y in zip(obstaclePoints[0],obstaclePoints[1])}
    
    
    obstacleNoClearancePoints = np.nonzero(minkowskiBotSum)
    obstacleNoClearancePoints = {(x,y) for x,y in zip(obstacleNoClearancePoints[0], obstacleNoClearancePoints[1])}
    
#    mapDisp.updateObstacleClear(obstacleSet)
#    mapDisp.updateObstacleBot(obstacleNoClearancePoints)
#    mapDisp.updateObstacleRaw(obsSet)
#    
#    mapDisp.showMap()    
    
    return xMax, yMax, obstacleSet, obsSet, obstacleNoClearancePoints

if __name__ == "__main__": 
    print("Enter GridSize(in mm): ")
    gridSize = int(input())
    print("Enter Robot Radius(in mm): ")
    robotbotRad = int(input())
    print("Enter Clearance(in mm): ")
    robotbotClr = int(input())
    xMax, yMax, obstacles, obsSet, obsNoClrPt = genObstacleSpace(250, 
                                                                 150, 
                                                                 gridSize, 
                                                                 robotbotRad, 
                                                                 robotbotClr)

#A1 = (45,62.5)
#A2 = (50,67.5)
#B1 = (100,62.5)
#B2 = (105,67.5)
#C1 = (105,112.5)
#C2 = (50,117.5)
#D1 = (100,117.5)
#D2 = (45,112.5)
#
#t11 = (A1,A2,B1)
#t12 = (B1,B2,C1)
#t13 = (C1,C2,D1)
#t14 = (D1,D2,A1)
#
#triangle(t11)
#triangle(t12)
#triangle(t13)
#triangle(t14)
