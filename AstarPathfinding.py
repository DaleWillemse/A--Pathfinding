from string import whitespace
import pygame
import math 
from queue import PriorityQueue

WIDTH = 600
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("A* Pathfinding Algorithm")

black = (0, 0, 0)   
white = (255, 255, 255) 
green = (0, 255, 0)
red = (255, 0, 0)   
blue = (0, 0, 255)  
yellow = (255, 255, 0)

class Node:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = white
        self.neighborts = []
        self.width = width
        self.total_rows = total_rows

    def get_pos(self):
        return self.row, self.col

    def closed(self):
        return self.color == red

    def open(self):
        return self.color == green

    def barrier(self):
        return self.color == black

    def start(self):
        return self.color == blue

    def end(self):
        return self.color == yellow
    
    def reset(self):
        self.color = white

    def make_closed(self):
        self.color = red
    
    def make_open(self):
        self.color = green

    def make_barrier(self):
        self.color = black
    
    def make_end(self):
        self.color = green

    def make_start(self):
        self.color = blue

    def make_path(self):
        self.color = yellow

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))