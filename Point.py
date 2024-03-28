from math import sqrt
import pygame


class Point:
    def __init__(self, x: int, y: int, type: str):
        self.x = x
        self.y = y
        self.type = type  # start, end, pickup, obstacle
    
    def GetCoordinates(self):
        return (self.x, self.y)
    
    def GetType(self):
        return self.type
        
    def Distance(self, other):
        return sqrt(pow(self.x - other.x, 2) + pow(self.y - other.y, 2))
    
    def GoTo(self, other):
        newPoint = Point(self.x, self.y, self.type)
        
        if (self.x < other.x):
            newPoint.x += 1
        elif (self.x > other.x):
            newPoint.x -= 1
            
        if (self.y < other.y):
            newPoint.y += 1
        elif (self.y > other.y):
            newPoint.y -= 1
        
        return newPoint

    def IsAvailable(self, map, obs):
        
        # Điểm nằm ngoài map
        if (self.x >= map.width or self.x < 0):
            return False
        if (self.y >= map.height or self.y < 0):
            return False
        
        # Điểm trùng với chướng ngại vật
        for ob in obs:
            for i in range (len(ob.points)):
                if (self.GetCoordinates() == ob.points[i].GetCoordinates()):
                    return False
        
        return True
    
    def GetSurroundingPoints(self):
        surPoints = []
        surPoints.append(self.x - 1, self.y - 1)
        
        return surPoints