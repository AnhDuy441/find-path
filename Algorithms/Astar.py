import math
import heapq
from Map import *


def FindPath(map: Map):
    OPEN = [Point() for _ in range(0)]  # priority queue / OPEN set
    CLOSED = [Point() for _ in range(0)]  # CLOSED set / VISITED order
    PARENT = dict()  # recorded parent
    g = dict()  # cost to come
    
    PARENT[map.start] = map.start
    g[map.start] = 0
    g[map.end] = math.inf
    heapq.heappush(OPEN, (FValue(g, map.start, map), map.start))
    
    while (OPEN):
        s: Point
        _, s = heapq.heappop(OPEN)
        CLOSED.append(s)
        
        if s == map.end:  # stop condition
            break
        
        for sNeighbor in s.GetNeighbor(map):
            newCost = g[s] + s.GetDistance(sNeighbor)

            if sNeighbor not in g:
                g[sNeighbor] = math.inf

            if newCost < g[sNeighbor]:  # conditions for updating Cost
                g[sNeighbor] = newCost
                PARENT[sNeighbor] = s
                heapq.heappush(OPEN, (FValue(g, sNeighbor, map), sNeighbor))
    return ExtractPath(PARENT), CLOSED

def ExtractPath(map: Map, parent: dict):
    path = [map.end]
    s = map.end

    while True:
        s = parent[s]
        path.append(s)

        if s == map.start:
            break

    return list(path)

def FValue(g: dict, point: Point, map: Map):
    return g[point] + map.start.GetDistance(map.end)