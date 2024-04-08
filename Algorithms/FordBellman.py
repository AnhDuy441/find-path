from Map import Map, Point

def find_shortest_path(map: Map):
    distances = {(x, y): float('inf') for x in range(map.width) for y in range(map.height)}
    distances[(map.start.x, map.start.y)] = 0

    # Xóa các điểm là chướng ngại vật ra
    for obstacle in map.obstacles:
        for point in obstacle.points:
            del distances[(point.x, point.y)]

    # Duyệt qua các điểm lân cận và cập nhật khoảng cách nếu có đường đi ngắn hơn
    for _ in range(map.height * map.width):
        for x in range(map.width):
            for y in range(map.height):
                for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, 1), (1, -1), (-1, -1)]:
                    neighbor_x, neighbor_y = x + dx, y + dy
                    if (neighbor_x, neighbor_y) in distances and (neighbor_x, neighbor_y) not in {(point.x, point.y) for obstacle in map.obstacles for point in obstacle.points}:
                        new_distance = distances.get((x, y), float('inf')) + Point(x, y, "").GetDistance(Point(neighbor_x, neighbor_y, ""))
                        if new_distance < distances.get((neighbor_x, neighbor_y), float('inf')):
                            distances[(neighbor_x, neighbor_y)] = new_distance

    # Truy vết đường đi ngắn nhất từ start đến end
    current_x, current_y = map.end.x, map.end.y
    path = []
    while (current_x, current_y) != (map.start.x, map.start.y):
        path.append(Point(current_x, current_y, ""))
        min_distance = float('inf')
        min_x, min_y = current_x, current_y
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, 1), (1, -1), (-1, -1)]:
            neighbor_x, neighbor_y = current_x + dx, current_y + dy
            if (neighbor_x, neighbor_y) in distances:
                if distances[(neighbor_x, neighbor_y)] < min_distance:
                    min_distance = distances[(neighbor_x, neighbor_y)]
                    min_x, min_y = neighbor_x, neighbor_y
        current_x, current_y = min_x, min_y

    # Đảo ngược mảng path để có thứ tự từ start đến end
    path.reverse()

    # Trả về mảng path và distances
    return path, distances[(map.end.x, map.end.y)]
