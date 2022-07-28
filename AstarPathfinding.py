from string import whitespace
import pygame
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

    def update_neighbors(self, grid):
        self.neighborts = []
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].barrier():
            self.neighborts.append(grid[self.row + 1][self.col])
        if self.row > 0 and not grid[self.row - 1][self.col].barrier():
            self.neighborts.append(grid[self.row - 1][self.col])
        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].barrier():
            self.neighborts.append(grid[self.row][self.col + 1])
        if self.col > 0 and not grid[self.row][self.col - 1].barrier():
            self.neighborts.append(grid[self.row][self.col - 1])

    def __lt__(self, other):
        return False


def herostic(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)

# making the grid
def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(i, j, gap, rows)
            grid[i].append(node)
    return grid

# drawing the grid
def draw_grid(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, black, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, black, (j * gap, 0), (j * gap, width))
    
def draw(win, grid, rows, width):
    win.fill(white)
    for row in grid:
        for node in row:
            node.draw(win)
    draw_grid(win, rows, width)
    pygame.display.update()

