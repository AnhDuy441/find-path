from Point import *


class Obstacle:
    # Constructor
    def __init__(self, points: list[Point]):
        self.points = [Point() for _ in range(0)]
        points = ConvexHull(points)
        
        for i in range(len(points)):
            for j in range(i + 1, len(points)):
                while(points[i].Distance(points[j]) != 0):
                    self.points.append(points[i])
                    points[i] = points[i].GoTo(points[j])
                self.points.append(points[i])
        tempPoint = self.points[len(self.points) - 1]
        while(self.points[0].Distance(tempPoint) != 0):
                    tempPoint = tempPoint.GoTo(self.points[0])
                    self.points.append(tempPoint) 

def orientation(p: Point, q: Point, r: Point):
# Hàm tính hướng của ba điểm
    val = (q.y - p.y) * (r.x - q.x) - (q.x - p.x) * (r.y - q.y)
    if val == 0:
        return 0  # Các điểm thẳng hàng
    return 1 if val > 0 else 2  # Ngược chiều kim đồng hồ hoặc cùng chiều kim đồng hồ

def ConvexHull(points: list[Point]):
    n = len(points)
    if n < 3:
        return []  # Không đủ điểm để tạo ra đa giác lỗi

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