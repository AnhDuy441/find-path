import math
import heapq
from itertools import permutations
from Map import *

def findTheShortestPath(map: Map):
    perms = permutations(map.pickUps)  # Chỉnh hợp của tập các pick up points {[p1, p2,...],   [p2, p1,...],   [p1, p1,...],...}
    perms = [( *perm, map.end) for perm in perms]
    shortestPath = [Point() for _ in range(0)]
    shortestClosed = [Point() for _ in range(0)]
    minCost = math.inf
    
    for points in perms:  # Tập các pick up points có thứ tự ngẫu nhiên [p1, p2,...]
        map.Draw()
        tempPath = [Point() for _ in range(0)]
        tempClosed = [Point() for _ in range(0)]
        tempCost = 0
        
        for i in range (-1, len(points) - 1):
            if i >= 0:
                path, cost, closed = fromStartToDes(map, points[i], points[i + 1])
            elif i == -1:
                path, cost, closed = fromStartToDes(map, map.start, points[i + 1])
            
            if path == None:
                return path, cost, closed
            else:
                path.pop()
                for point in path:
                    tempPath.append(point)
                
                closed.pop()
                for point in closed:
                    tempClosed.append(point)
                
                tempCost += cost
        if minCost > tempCost:
            shortestPath = tempPath
            shortestClosed = tempClosed
            minCost = tempCost

            
            
    if minCost != math.inf:
        shortestPath.append(map.end)
        shortestClosed.append(map.end)
        return shortestPath, minCost, shortestClosed
    else:
        return fromStartToDes(map, map.start, map.end)

def fromStartToDes(map: Map, startPoint: Point, desPoint: Point):
    OPEN = [Point() for _ in range(0)]  # priority queue / OPEN set
    CLOSED = [Point() for _ in range(0)]  # CLOSED set / VISITED order
    PARENT = dict()  # recorded parent
    g = dict()  # cost to come

    PARENT[startPoint] = startPoint
    g[startPoint.GetCoordinates()] = 0
    g[desPoint.GetCoordinates()] = math.inf
    heapq.heappush(OPEN, (FValue(g, startPoint, desPoint), startPoint))
    
    while (OPEN):
        s: Point
        _, s = heapq.heappop(OPEN)
        CLOSED.append(s)
        
        if s.GetCoordinates() == desPoint.GetCoordinates():  # stop condition
            return ExtractPath(PARENT, startPoint, s), costOfPath(ExtractPath(PARENT, startPoint, s)), CLOSED
        
        for sNeighbor in s.GetNeighbor(map):
            newCost = g[s.GetCoordinates()] + s.GetDistance(sNeighbor)

            if sNeighbor.GetCoordinates() not in g:
                g[sNeighbor.GetCoordinates()] = math.inf

            if newCost < g[sNeighbor.GetCoordinates()]:  # conditions for updating Cost
                g[sNeighbor.GetCoordinates()] = newCost
                PARENT[sNeighbor] = s
                heapq.heappush(OPEN, (FValue(g, sNeighbor, desPoint), sNeighbor))
                if sNeighbor in CLOSED:
                    CLOSED.remove(sNeighbor)
        
        drawClosed(map, CLOSED)
    return None, float(0), None        
        
def drawClosed(map: Map, CLOSED: list[Point]):
    for i in range(len(CLOSED)):
        if CLOSED[i].GetCoordinates() != map.start.GetCoordinates() and CLOSED[i].GetCoordinates() != map.end.GetCoordinates():
            check = False
            for point in map.pickUps:
                if CLOSED[i].GetCoordinates() == point.GetCoordinates():
                    check = True
                    break
            if check == False:
                pygame.draw.rect(map.screen, (128, 128, 128), (CLOSED[i].x * map.scale, CLOSED[i].y * map.scale, map.scale, map.scale))
    pygame.display.flip()  # Update display
            
def ExtractPath(parent: dict, startPoint: Point, s: Point):
    path = [s]
    
    while True:
        s = parent[s]
        path.append(s)
        
        if s.GetCoordinates() == startPoint.GetCoordinates():
            break

    path.reverse()
    return list(path)

def costOfPath(path: list[Point]):
    cost = 0
    for i in range((len(path)) - 1):
        cost += path[i].GetDistance(path[i + 1])
    return float(cost)

def FValue(g: dict, currentPoint: Point, destinationPoint: Point):
    return g[currentPoint.GetCoordinates()] + currentPoint.GetDistance(destinationPoint)