import os
import tkinter as tk
from tkinter import filedialog
from Map import *
from Algorithms import Astar

# Lấy đường dẫn file input
def SelectFile():
    root = tk.Tk()
    root.withdraw()  # Ẩn cửa sổ gốc của tkinter

    filePath = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])  # Chọn file txt
    if filePath:
        print("Đường dẫn file đã chọn:", filePath)
        return filePath        
    else:
        print("Không có file nào được chọn.")
        return "Null"

# Lấy dữ liệu từ file
def ReadFile(FilePath: str):
    try:
        with open(FilePath, 'r') as file:
            map: Map
            points = [Point() for _ in range(0)]
            pickUpPoints = [Point() for _ in range(0)]
            obstacles = [Obstacle() for _ in range(0)]
            
            firstLine = file.readline().strip()  # Đọc dòng đầu tiên (kích thước bản đồ)
            MapSize = [int(x) for x in firstLine.split(',')]  # Chuyển đổi các phần từ chuỗi sang số nguyên
            
            
            secondLine = file.readline().strip()  # Đọc dòng thứ hai (các điểm S, G, điểm đón)
            pointsNumbers = [int(x) for x in secondLine.split(',')]
            k = 0
            for i in range(int(len(pointsNumbers)/2)):
                if i == 0:
                    tempStr = "start"
                elif i == 1:
                    tempStr = "end"
                else:
                    tempStr = "pickup"
                a = k
                k += 1
                b = k
                k += 1  
                points.append(Point(pointsNumbers[a], pointsNumbers[b], tempStr))
            
            for point in points:
                point.GetCoordinates()
                if (point.GetType() == "pickup"):
                    pickUpPoints.append(point)
            
            thirdLine = file.readline().strip()  # Đọc dòng thứ 3 (số lượng chướng ngại vật)
            obstacleAmount = int(thirdLine)
            for i in range(obstacleAmount):  # Mỗi lần lặp đọc 1 dòng chứa các điểm của chướng ngại vật
                obPoints = [Point() for _ in range(0)]
                tempStr = file.readline().strip()
                pointsNumbersPerObstacle = [int(x) for x in tempStr.split(',')]
                j = 0
                k = 0
                for j in range(int(len(pointsNumbersPerObstacle)/2)):  # Mỗi lần lặp đọc 1 điểm của chướng ngại vật
                    a = k
                    k += 1
                    b = k
                    k += 1
                    obPoints.append(Point(pointsNumbersPerObstacle[a], pointsNumbersPerObstacle[b], "obstacle"))
                obstacle = Obstacle(obPoints)
                obstacles.append(obstacle)
                        
            map = Map(MapSize[0], MapSize[1], points[0], points[1], pickUpPoints, obstacles)
        return map
                
            
    except FileNotFoundError:
        print("File không tồn tại.")
    except Exception as e:
        print("Đã xảy ra lỗi:", e)

if __name__ == "__main__":
    
    os.system('cls')
    
    map = ReadFile(SelectFile())
    map.Draw()
    
    path, cost, closed = Astar.findTheShortestPath(map)
    if (path == None):
        print("Không có đường đi")
    else:
        for i in range(len(path)):
            pygame.draw.rect(map.screen, (128, 0, 128), (path[i].x * map.scale, path[i].y * map.scale, map.scale, map.scale))
        # pygame.display.flip()  # Update display
        print("Cost of path: ", cost)
    
    map.Draw()
    running = True
    while running: 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False   
    pygame.quit()    