from math import sqrt


class Point:
    def __init__(self, x: int, y: int, type: str):
        self.x = x
        self.y = y
        self.type = type  # start, end, pickup, obstacle
    
    def __lt__(self, other):
        # Define how to compare two Point instances
        if self.x == other.x:
            return self.y < other.y
        return self.x < other.x
    
    def GetCoordinates(self):
        return (self.x, self.y)
    
    def GetType(self):
        return self.type
        
    def GetDistance(self, other):
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

    def IsAvailable(self, map):
        
        # Điểm nằm ngoài map
        if (self.x >= map.width or self.x < 0):
            return False
        if (self.y >= map.height or self.y < 0):
            return False
        
        # Điểm trùng với chướng ngại vật
        for ob in map.obstacles:
            for i in range (len(ob.points)):
                if (self.GetCoordinates() == ob.points[i].GetCoordinates()):
                    return False
        
        # Điểm trùng với các điểm đặc biệt
        if (self.GetCoordinates() == map.start.GetCoordinates()):# or self.GetCoordinates() == map.end.GetCoordinates()):
            return False
        # for point in map.pickUps:
        #     if (self.GetCoordinates() == point.GetCoordinates()):
        #         return False
        
        return True
    
    def GetNeighbor(self, map):
        tempPoints = [Point() for _ in range(0)]
        tempPoints.append(Point(self.x - 1, self.y - 1, "neighbor"))
        tempPoints.append(Point(self.x, self.y - 1, "neighbor"))
        tempPoints.append(Point(self.x + 1, self.y - 1, "neighbor"))
        tempPoints.append(Point(self.x - 1, self.y, "neighbor"))
        tempPoints.append(Point(self.x + 1, self.y, "neighbor"))
        tempPoints.append(Point(self.x - 1, self.y + 1, "neighbor"))
        tempPoints.append(Point(self.x, self.y + 1, "neighbor"))
        tempPoints.append(Point(self.x + 1, self.y + 1, "neighbor"))
        
        neighbor = [Point() for _ in range(0)]
        for point in tempPoints:
            if (point.IsAvailable(map)):
                neighbor.append(point)
                
        return neighbor