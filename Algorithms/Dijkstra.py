import math 
import heapq
from itertools import permutations
from Map import *
# Apply the dijkstra algorithm to find the shortest path

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
    OPEN = []  # priority queue / OPEN set
    CLOSED = []  # CLOSED set / VISITED order

    all_points = map.get_all_points()

    distances = {point.GetCoordinates(): math.inf for point in all_points}
    previous_points = {point.GetCoordinates(): None for point in all_points}

    distances[startPoint.GetCoordinates()] = 0
    heapq.heappush(OPEN, (0, startPoint))

    while OPEN:
        current_distance, current_point = heapq.heappop(OPEN)

        if current_point.GetCoordinates() in CLOSED:
            continue

        CLOSED.append(current_point)
        drawClosed(map, CLOSED)

        if current_point.GetCoordinates() == desPoint.GetCoordinates():
            break
        
        #Check all neighbors of current point, if the distance from start to neighbor is shorter than the current distance, update the distance
        for neighbor in current_point.GetNeighbor(map):
            new_distance = current_distance + current_point.GetDistance(neighbor)

            if new_distance < distances[neighbor.GetCoordinates()]:
                distances[neighbor.GetCoordinates()] = new_distance
                previous_points[neighbor.GetCoordinates()] = current_point
                heapq.heappush(OPEN, (new_distance, neighbor))

    path = []
    cost = 0
    current_point = desPoint

    while current_point is not None:
        path.append(current_point)
        current_point = previous_points[current_point.GetCoordinates()]

    path = path[::-1]  # Reverse the path

    if path:
        cost = distances[desPoint.GetCoordinates()]

    return path, cost, CLOSED
        
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