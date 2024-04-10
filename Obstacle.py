import pygame
from Point import *


class Obstacle:
    # Constructor
    def __init__(self, newPoints: list[Point]):
        self.points = [Point() for _ in range(0)]
        newPoints = ConvexHull(newPoints)
        # Draw the outer edge of the obstacle
        i = 0
        for j in range(1, len(newPoints)):
            while(newPoints[i].GetDistance(newPoints[j]) != 0):
                self.points.append(newPoints[i])
                newPoints[i] = newPoints[i].GoTo(newPoints[j])
        self.points.append(newPoints[i])
        endPoint = self.points[len(self.points) - 1]
        while(self.points[0].GetDistance(endPoint) != 0):
                    endPoint = endPoint.GoTo(self.points[0])
                    self.points.append(endPoint)
        # Delete the duplicate points
        for i in range(len(self.points) - 2):
            for j in range(i + 1, len(self.points) - 1):
                if self.points[i].GetCoordinates() == self.points[j].GetCoordinates():
                    self.points.remove(self.points[j])
        self.points.pop()
        
        # Topmost and bottommost points of the obstacle
        top = self.points[0]
        for point in self.points:
            if (top.y >= point.y):
                top = point
                bot = top
            elif (point.y > bot.y):
                bot = point
                
        # Fill the inside of the obstacle
        skip = True
        for point in self.points:
            if (point.GetCoordinates() == top.GetCoordinates()):
                skip = False
                continue
            elif (skip == True):
                continue
            elif (point.GetCoordinates() == bot.GetCoordinates()):
                break
            
            i = 1
            while (True):
                tempPoint = Point(point.x - i, point.y, "obstacle")
                if(contain(self.points, tempPoint) == False):
                    self.points.append(tempPoint)
                    i += 1
                else:
                    break
                      
def contain(points: list[Point], checkPoint: Point):
    for point in points:
        if (point.GetCoordinates() == checkPoint.GetCoordinates()):
            return True
    return False
                
def orientation(p: Point, q: Point, r: Point):
# Function to find the orientation of three points
    val = (q.y - p.y) * (r.x - q.x) - (q.x - p.x) * (r.y - q.y)
    if val == 0:
        return 0  # Points are colinear
    return 1 if val > 0 else 2  # Clockwise orientation

def ConvexHull(points: list[Point]):
    n = len(points)
    if n < 3:
        return []  # Not enough points to create a convex hull

    hull = []
    l = 0
    for i in range(1, n):
        if points[i].x < points[l].x:
            l = i

    p = l
    while True:
        hull.append(points[p])
        q = (p + 1) % n
        for i in range(n):
            if orientation(points[p], points[i], points[q]) == 2:
                q = i
        p = q
        if p == l:
            break

    return hull