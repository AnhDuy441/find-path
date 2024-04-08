import pygame
from Obstacle import *


class Map:
    
    # Constructor
    def __init__(self, width: int, height: int, start: Point, end: Point, pickUps: list[Point], obstacles: list[Obstacle]):
        self.width = width
        self.height = height
        self.start = start
        self.end = end
        self.pickUps = pickUps
        self.obstacles = obstacles
        self.scale = int(500 / height)
        
        pygame.init()
        self.screen = pygame.display.set_mode((width*self.scale, height*self.scale))
        pygame.display.set_caption("Pathfinding Visualizer")
        
    
    def Draw(self):
        pygame.draw.rect(self.screen, (0, 255, 0), (self.start.x * self.scale, self.start.y * self.scale, self.scale, self.scale))
        pygame.draw.rect(self.screen, (255, 0, 0), (self.end.x * self.scale, self.end.y * self.scale, self.scale, self.scale))
        
        for point in self.pickUps:
            pygame.draw.rect(self.screen, (255, 165, 0), (point.x * self.scale, point.y * self.scale, self.scale, self.scale))
        
        for obstacle in self.obstacles:
            for point in obstacle.points:
                pygame.draw.rect(self.screen, (0, 0, 255), (point.x * self.scale, point.y * self.scale, self.scale, self.scale))

        for x in range(self.width * self.scale):
            for y in range(self.height * self.scale):
                color = self.screen.get_at((x, y))
                if color == (0, 0, 0):  # Nếu pixel có màu đen, xám
                    self.screen.set_at((x, y), (255, 255, 255))  # Đổi thành màu trắng

        pygame.display.flip()  # Update display