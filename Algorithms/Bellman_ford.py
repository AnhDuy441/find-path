import pygame
import heapq
from Map import Map, Point

def find_path(map: Map, start: Point, end: Point):
    distances = {(x, y): float('inf') for x in range(map.width) for y in range(map.height)}
    distances[(start.x, start.y)] = 0
    path = []
    CLOSED = []

    open_set = []
    heapq.heappush(open_set, (0, start))

    for obstacle in map.obstacles:
        for point in obstacle.points:
            del distances[(point.x, point.y)]

    while open_set:
        current = heapq.heappop(open_set)[1]
        CLOSED.append(current)

        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, 1), (1, -1), (-1, -1)]:
            neighbor_x, neighbor_y = current.x + dx, current.y + dy
            if (neighbor_x, neighbor_y) in distances and (neighbor_x, neighbor_y) not in {(point.x, point.y)
                                                                                          for obstacle in
                                                                                          map.obstacles for
                                                                                          point in
                                                                                          obstacle.points}:
                new_distance = distances.get((current.x, current.y), float('inf')) + Point(current.x, current.y,
                                                                                           "").GetDistance(
                    Point(neighbor_x, neighbor_y, ""))
                if new_distance < distances.get((neighbor_x, neighbor_y), float('inf')):
                    distances[(neighbor_x, neighbor_y)] = new_distance
                    heapq.heappush(open_set, (distances[(neighbor_x, neighbor_y)], Point(neighbor_x, neighbor_y, "")))

    current_x, current_y = end.x, end.y
    i = 0
    # Trace the shortest path from start to end
    while (current_x, current_y) != (start.x, start.y):
        i += 1
        path.append(Point(current_x, current_y, ""))
        min_distance = float('inf')
        min_x, min_y = current_x, current_y
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, 1), (1, -1), (-1, -1)]:
            neighbor_x, neighbor_y = current_x + dx, current_y + dy
            if (neighbor_x, neighbor_y) in distances:
                CLOSED.append(Point(neighbor_x, neighbor_y, ""))
                if distances[(neighbor_x, neighbor_y)] < min_distance:
                    min_distance = distances[(neighbor_x, neighbor_y)]
                    min_x, min_y = neighbor_x, neighbor_y
        current_x, current_y = min_x, min_y
        if i == 100:
            CLOSED.clear()
            break

    path.reverse()
    drawClosed(map, CLOSED)

    return path, distances[(end.x, end.y)], Point(current_x, current_y, "")

def find_shortest_path(map: Map):
    path = []
    total = 0.0
    start = map.start
    map.pickUps.append(map.end)
    n = len(map.pickUps)
    for i in range(n):
        end = map.pickUps[i]
        new_path, new_distance, cur = find_path(map, start, end)
        if (cur.x, cur.y) != (start.x, start.y):
            path.clear()
            total = float("inf")
            break
        else:
            path = path + new_path
            total += new_distance
            start = end

    return path, total

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

def Bellman_ford(map: Map):
    return find_shortest_path(map)