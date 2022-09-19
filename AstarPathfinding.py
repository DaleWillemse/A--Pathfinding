from string import whitespace
from turtle import pos
import pygame
from queue import PriorityQueue

WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("A* Pathfinding Algorithm")

black = (0, 0, 0)
white = (255, 255, 255)
green = (0, 255, 0)
red = (255, 0, 0)
blue = (0, 0, 255)
cyan = (0, 255, 255)
yellow = (255, 255, 0)
purple = (255, 0, 255)


class Node:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = white
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows

    def get_pos(self):
        return self.row, self.col

    def barrier(self):
        return self.color == black

    def start(self):
        return self.color == blue

    def end(self):
        return self.color == cyan

    def reset(self):
        self.color = white

    def make_closed(self):
        self.color = red

    def make_open(self):
        self.color = yellow

    def make_barrier(self):
        self.color = black

    def make_end(self):
        self.color = purple

    def make_start(self):
        self.color = purple

    def make_path(self):
        self.color = cyan

    def draw(self, win):
        pygame.draw.rect(
            win, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid):
        self.neighbors = []
        # Up
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].barrier():
            self.neighbors.append(grid[self.row + 1][self.col])
        # Down
        if self.row > 0 and not grid[self.row - 1][self.col].barrier():
            self.neighbors.append(grid[self.row - 1][self.col])
        # Left
        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].barrier():
            self.neighbors.append(grid[self.row][self.col + 1])
        # Right
        if self.col > 0 and not grid[self.row][self.col - 1].barrier():
            self.neighbors.append(grid[self.row][self.col - 1])

    def __lt__(self, other):
        return False


def heuristic(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)


def reconstruct_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw()


def algorithm(draw, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    g_score = {node: float("inf") for row in grid for node in row}
    g_score[start] = 0
    f_score = {node: float("inf") for row in grid for node in row}
    f_score[start] = heuristic(start.get_pos(), end.get_pos())

    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            end.make_end()
            reconstruct_path(came_from, end, draw)
            start.make_start()
            return True

        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1
            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + \
                    heuristic(neighbor.get_pos(), end.get_pos())
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()
        draw()

        if current != start:
            current.make_closed()

    return False

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


def mouse_pos(pos, rows, width):
    gap = width // rows
    y, x = pos
    row = y // gap
    col = x // gap

    return row, col


def main(win, width):
    rows = 50
    grid = make_grid(rows, width)

    start = None
    end = None

    run = True
    started = False
    while run:
        draw(win, grid, rows, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if started:
                continue
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                row, col = mouse_pos(pos, rows, width)
                node = grid[row][col]
                if not start and node != end:
                    start = node
                    start.make_start()
                elif not end and node != start:
                    end = node
                    end.make_end()
                elif node != start and node != end:
                    node.make_barrier()

            elif pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                row, col = mouse_pos(pos, rows, width)
                node = grid[row][col]
                if node == start:
                    start = None
                elif node == end:
                    end = None
                node.reset()

            # starting the algorithm
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid)

                    algorithm(lambda: draw(win, grid, rows, width),
                              grid, start, end)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    start = None
                    end = None
                    grid = make_grid(rows, width)
    pygame.quit()


main(WIN, WIDTH)
