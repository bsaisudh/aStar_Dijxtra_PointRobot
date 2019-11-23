# -*- coding: utf-8 -*-
"""
Created on Tue Apr  2 16:34:17 2019

@author: balam
"""

import cv2
import numpy as np

class dispMap:
    
    def __init__(self, mapSize):
        self.mapSize = mapSize
        self.map = np.multiply(np.ones((mapSize[0], mapSize[1], 3)),255).astype('uint8')
        self.video = cv2.VideoWriter('video.avi',cv2.VideoWriter_fourcc(*"XVID"), -1,(1000,600))
        
    
    def updateObstacleRaw(self, obstacleSet):
        for point in obstacleSet:
            self.map[point[0],point[1],:] = [0, 0, 0] #BGR 
    
    def updateObstacleClear(self, obstacleSet):
        for point in obstacleSet:
            self.map[point[0],point[1],:] = [100, 100, 100] #BGR
            
    def updateObstacleBot(self, obstacleSet):
        for point in obstacleSet:
            self.map[point[0],point[1],:] = [50, 50, 50] #BGR
    
    def updateStartNode(self, point):
        self.map[point[0],point[1],:] = [255, 0, 0] #BGR
    
    def updateGoalNode(self, point):
        self.map[point[0],point[1],:] = [0, 0, 255] #BGR
        
    def updateVisitedNode(self, point):
        self.map[point[0],point[1],:] = [0, 255, 255] #BGR
    
    def updatePathNode(self, point):
        self.map[point[0],point[1],:] = [0, 255, 0] #BGR
    
    def updateActiveNode(self, point):
        self.map[point[0],point[1],:] = [255, 255, 0] #BGR
    
    def releaseVideo(self):
        self.video.release()
    
    def showMap(self):
        flippedMap = np.zeros((self.map.shape[1],
                               self.map.shape[0],
                               self.map.shape[2])).astype('uint8')
        flippedMap[:,:,0] = np.flipud(self.map[:,:,0].T)
        flippedMap[:,:,1] = np.flipud(self.map[:,:,1].T)
        flippedMap[:,:,2] = np.flipud(self.map[:,:,2].T)
        resizedMap = cv2.resize(flippedMap,(1000,600),interpolation = cv2.INTER_AREA)
        cv2.imshow("Map", resizedMap)
        self.video.write(resizedMap)
        cv2.waitKey(1)