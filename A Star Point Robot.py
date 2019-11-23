# -*- coding: utf-8 -*-
"""
Created on Sat Mar 23 14:28:56 2019

@author: balam
"""

from queue import PriorityQueue
import numpy as np
from ObstacleSpace import genObstacleSpace
import MapDiaplay as md


def actions(currentNode, currentCost):
    newNodes = []
    newNodesFinal = []
    # vertical and horizontal nodes
    for i in [(0,1),(0,-1),(1,0),(-1,0)]:
        newNode = tuple(np.subtract(currentNode, i))
        if not(newNode[0]<0 or newNode[1]<0 or newNode[0]>=mapX or newNode[1]>=mapY):
            newNodes.append([currentCost + 1.0 + CtoG(goalNode,newNode),currentNode,newNode,True,currentCost + 1.0])
    # corss nodes
    for i in [(-1,-1),(-1,+1),(1,-1),(1,1)]:
        newNode = tuple(np.subtract(currentNode, i))
        if not(newNode[0]<0 or newNode[1]<0 or newNode[0]>=mapX or newNode[1]>=mapY):
            newNodes.append([currentCost + 1.414 + CtoG(goalNode,newNode),currentNode,newNode,True,currentCost + 1.414])

    for node in newNodes:
        # update cost and parent if cost is less for already visited nodes
        if node[2] in visitedNodes:
            if  nodes[np.ravel_multi_index(node[2],mapSize)][4] > node[4]:
                nodes[np.ravel_multi_index(node[2],mapSize)][4] = node[4]
                nodes[np.ravel_multi_index(node[2],mapSize)][1] = node[1]
        # remove if in obstacle or visited nodes
        if not(node[2] in obstacles.union(visitedNodes)):
            newNodesFinal.append(node)
    # update nodes map list
    for node in newNodesFinal:
        nodes[np.ravel_multi_index(node[2],mapSize)] = node
    return newNodesFinal

def CtoG(fromNode, toNode):
    return np.sqrt(np.square(fromNode[0]-toNode[0])+np.square(fromNode[1]-toNode[1]))

nodes = []
visitedNodes  = set()


print('''
    default values:
    Grid Size = 1
    Start Node = (20,20)
    Goal Naode = (230,130)
    Use Default Values?[Y/N] : 
    ''')
useDefault = str(input())
if (useDefault == 'Y' or useDefault == 'y'):
    gridSize = 1
    robotbotRad = 0
    robotbotClr = 0
    goalNodeX = 230
    goalNodeY = 130
    startNodeX = 20
    startNodeY = 20
else:
    print("Enter GridSize: ")
    gridSize = int(input())
    print("Enter Goal Node x: ")
    goalNodeX = int(input())
    print("Enter Goal Node y: ")
    goalNodeY = int(input())
    print("Enter Start Node x: ")
    startNodeX = int(input())
    print("Enter Start Node y: ")
    startNodeY = int(input())
    robotbotRad = 0
    robotbotClr = 0

print('''
      
Constructing Configuration Space

''')
mapX, mapY, obstacles, rawObs, botObs = genObstacleSpace(250, 
                                                         150, 
                                                         gridSize, 
                                                         robotbotRad, 
                                                         robotbotClr)
print('''
      
Executing Algotithm

''')
mapSize = (mapX,mapY)            

mapDisp = md.dispMap(mapSize)
mapDisp.updateObstacleClear(obstacles)
mapDisp.updateObstacleBot(botObs)
mapDisp.updateObstacleRaw(obstacles)
mapDisp.showMap()

for x in range(0,mapX):
    for y in range(0,mapY):
        nodes.append([92233720.0,(-1,-1),(x,y),False,92233720.0])  
        
startNode = (round(startNodeX/gridSize),round(startNodeY/gridSize))
goalNode = (round(goalNodeX/gridSize),round(goalNodeY/gridSize))

mapDisp.updateStartNode(startNode)
mapDisp.updateGoalNode(goalNode)
mapDisp.showMap()

nodes[np.ravel_multi_index(startNode,mapSize)] = [CtoG(startNode,goalNode),(-1,-1),startNode,True,0.0]
  
visitedNodes.add(startNode)
q = PriorityQueue()

q.put([CtoG(startNode,goalNode),(-1,-1),startNode,True,0.0])

i = 0

mapMap = np.zeros(mapSize)
updateFrequency = mapMap.size*0.005
while not q.empty():
    i = i+1
    reached = False
    nextNode = q.get()
    mapDisp.updateActiveNode(nextNode[2])
    actionNodes = actions(nextNode[2],nextNode[4])
    for actionNode in actionNodes:
        visitedNodes.add(actionNode[2])
        mapDisp.updateVisitedNode(actionNode[2])
        q.put(actionNode)
        mapMap[actionNode[2][0]][actionNode[2][1]] = actionNode[0]
        if actionNode[2] == goalNode:
            reached = True
    if reached == True:
        mapDisp.showMap()
        break
    if i > updateFrequency:
        mapDisp.showMap()
        i = 0 

if reached:
    pathNodes = []
    seedNode = goalNode
    pathNodes.append(seedNode)
    while True:
        seedNode = nodes[np.ravel_multi_index(seedNode,mapSize)][1]
        pathNodes.append(seedNode)
        mapDisp.updatePathNode(seedNode)
        mapMap[seedNode[0]][seedNode[1]] = 0
        mapDisp.showMap()
        if seedNode == startNode:
            break
else:
    print("Path Not Found")
    
mapDisp.updateStartNode(startNode)
mapDisp.updateGoalNode(goalNode)
mapDisp.showMap()
mapDisp.releaseVideo()