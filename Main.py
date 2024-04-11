import os
import sys
import tkinter as tk
from tkinter import filedialog
from Map import *
from Algorithms import Astar, Bellman_ford, Dijkstra

# Get the path of the input file
def SelectFile():
    root = tk.Tk()
    root.withdraw()   # Hide the root window of tkinter

    filePath = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])  # Select txt file
    if filePath:
        print("Đường dẫn file đã chọn:", filePath)
        return filePath        
    else:
        print("Không có file nào được chọn.")
        return "Null"

# Get data from file
def ReadFile(FilePath: str):
    try:
        with open(FilePath, 'r') as file:
            map: Map
            points = [Point() for _ in range(0)]
            pickUpPoints = [Point() for _ in range(0)]
            obstacles = [Obstacle() for _ in range(0)]
            
            firstLine = file.readline().strip()  # Read the first line (map size)
            MapSize = [int(x) for x in firstLine.split(',')]  # Convert string elements to integers
            
            
            secondLine = file.readline().strip() # Read the second line (S, G points, pick-up points)
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
            
            thirdLine = file.readline().strip()  # Read the third line (number of obstacles)
            obstacleAmount = int(thirdLine)
            for i in range(obstacleAmount):  # Each loop reads a line containing the points of the obstacle
                obPoints = [Point() for _ in range(0)]
                tempStr = file.readline().strip()
                pointsNumbersPerObstacle = [int(x) for x in tempStr.split(',')]
                j = 0
                k = 0
                for j in range(int(len(pointsNumbersPerObstacle)/2)): # Each loop reads a point of the obstacle
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

# Create a window to receive requests
def Menu():
    # Create a window
    window = tk.Toplevel()
    window.title("Tìm đường đi ngắn nhất")
    window.geometry("300x200")  # Set window size

    numbers = [0, 1, 2]
    selectedValue = int(0)  # Variable to store the selected number value
    
    def HandleChoice(choice):
        nonlocal selectedValue
        selectedValue = choice
        window.destroy()  # Close the window after selection
    
    buttonText = []
    buttonText.append("Thuật toán Dijkstra")
    buttonText.append("Thuật toán A star")
    buttonText.append("Thuật toán Bellman-Ford")

    # Create input box
    for number in numbers:
        button = tk.Button(window, text=buttonText[number], command=lambda num=number: HandleChoice(num), width=25, height=2, font=("Arial", 12))
        button.pack(pady=5)

    # Display the window and wait for the user to enter a value
    window.wait_window(window)
    return selectedValue

if __name__ == "__main__":
    
    os.system('cls')
    
    map = ReadFile(SelectFile())
    map.Draw()
    
    method = Menu()
    if method == 0:
        path, cost, closed = Dijkstra.findTheShortestPath(map)
    elif method == 1:
        path, cost, closed = Astar.findTheShortestPath(map)
    elif method == 2:
        path, cost = Bellman_ford.Bellman_ford(map)
    
    if (path == None):
        print("Không có đường đi")
    else:
        for i in range(len(path)):
            pygame.draw.rect(map.screen, (128, 0, 128), (path[i].x * map.scale, path[i].y * map.scale, map.scale, map.scale))
        print("Chi phí đường đi: ", cost)
    
    map.Draw()
    running = True
    while running: 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
    pygame.quit()