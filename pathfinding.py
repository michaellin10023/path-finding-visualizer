import pygame
import pygame_menu
import math
from queue import PriorityQueue

WIDTH = 800 
WIN = pygame.display.set_mode((WIDTH,WIDTH))
pygame.display.set_caption("Pathfinding algorithm")

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

class Spot:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows
        self.visited = False

    def get_pos(self):
        return self.row, self.col
    
    def is_closed(self):
        return self.color == RED

    def is_open(self):
        return self.color == GREEN

    def is_barrier(self):
        return self.color == BLACK

    def is_start(self):
        return self.color == ORANGE
    
    def is_end(self):
        return self.color == TURQUOISE

    def reset(self):
        self.color = WHITE

    def make_closed(self):
        self.color = RED

    def make_open(self):
        self.color = GREEN

    def make_barrier(self):
        self.color = BLACK

    def make_start(self):
        self.color = ORANGE
    
    def make_end(self):
        self.color = TURQUOISE

    def make_path(self):
        self.color = PURPLE

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid):
        self.neighbors = []
        if self.row < self.total_rows - 1 and not grid[self.row+1][self.col].is_barrier(): ## down
            self.neighbors.append(grid[self.row+1][self.col])
        if self.row > 0 and not grid[self.row-1][self.col].is_barrier(): ## up
            self.neighbors.append(grid[self.row-1][self.col])
        if self.col > 0 and not grid[self.row][self.col-1].is_barrier(): ## left
            self.neighbors.append(grid[self.row][self.col-1])
        if self.col < self.total_rows - 1 and not grid[self.row][self.col+1].is_barrier(): ## right
            self.neighbors.append(grid[self.row][self.col+1])
            
    
    def __lt__(self, other):
        return False

def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)

def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            spot = Spot(i, j, gap, rows)
            grid[i].append(spot)

    return grid

def draw_grid(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))

def draw(win, grid, rows, width):
    win.fill(WHITE)

    for row in grid:
        for spot in row:
            spot.draw(win)

    draw_grid(win, rows, width)
    pygame.display.update()

def get_clicked_pos(pos, rows, width):
    gap = width // rows
    y, x = pos

    row = y // gap
    col = x // gap
    return row, col

def reconstruct_path(cameFrom, current, draw):
    while current in cameFrom:
        current = cameFrom[current]
        current.make_path()
        draw()
    

def a_star(draw, grid, start, end):
    count = 0
    # The set of discovered nodes that may need to be (re-)expanded.
    # Initially, only the start node is known.
    # This is usually implemented as a min-heap or priority queue rather than a hash-set.
    openSet = PriorityQueue()
    openSet.put((0, count, start))

    # For node n, cameFrom[n] is the node immediately preceding it on the cheapest path from start
    # to n currently known.
    cameFrom = {}

    # For node n, gScore[n] is the cost of the cheapest path from start to n currently known.
    gScore = {spot: float("inf") for row in grid for spot in row}
    gScore[start] = 0

    # For node n, fScore[n] := gScore[n] + h(n). fScore[n] represents our current best guess as to
    # how short a path from start to finish can be if it goes through n.
    fScore = {spot: float("inf") for row in grid for spot in row}
    fScore[start] = h(start.get_pos(), end.get_pos())

    # Check if node exist in openSet
    openSet_hash = {start}

    while not openSet.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        # This operation can occur in O(1) time if openSet is a min-heap or a priority queue
        current = openSet.get()[2]
        openSet_hash.remove(current)

        if current == end:
            reconstruct_path(cameFrom, current, draw)
            end.make_end()
            return True

        for neighbor in current.neighbors:
            # 1 is the distance from current to their neighbors
            # temp_gScore is the distance from start to the neighbor through current
            temp_gScore = gScore[current] + 1
            if temp_gScore < gScore[neighbor]:
                # This path to neighbor is better than any previous one. Record it!
                cameFrom[neighbor] = current
                gScore[neighbor] = temp_gScore
                fScore[neighbor] = gScore[neighbor] + h(neighbor.get_pos(), end.get_pos())
                if neighbor not in openSet_hash:
                    count += 1
                    openSet.put((fScore[neighbor], count, neighbor))
                    openSet_hash.add(neighbor)
                    neighbor.make_open()
        draw()

        if current != start:
            current.make_closed()

    return False

def bfs(draw, grid, start, end):
    queue = []
    cameFrom = {}
    queue.append(start)
    start.visited = True

    while queue:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = queue.pop(0)
        if current == end:
            reconstruct_path(cameFrom, current, draw)
            end.make_end()
            return True
    
        for neighbor in current.neighbors:
            if neighbor.visited == False:
                cameFrom[neighbor] = current
                queue.append(neighbor)
                neighbor.visited = True
                neighbor.make_open()        

        draw()

        if current != start:
            current.make_closed()

    return False
    
def main(win, width, algo):
    ROWS = 50
    grid = make_grid(ROWS, width)
     
    start = None
    end = None
    run = True
    # pygame.draw.rect(pygame.display.set_mode((400, 300)), BLACK, pygame.Rect(10, 10, 100, 100))
                                             
    while run:
        draw(win, grid, ROWS, width)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if pygame.mouse.get_pressed()[0]: ## left
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                spot = grid[row][col]
                if not start and spot != end:
                    start = spot
                    start.make_start()

                elif not end and spot != start:
                    end = spot
                    end.make_end()

                elif spot != start and spot != end:
                    spot.make_barrier()

            elif pygame.mouse.get_pressed()[2]: ## right
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                spot = grid[row][col]
                spot.reset()
                if spot == start:
                    start = None
                if spot == end:
                    end = None
                    
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for spot in row:
                            spot.update_neighbors(grid)

                    if algo == 1:
                        a_star(lambda: draw(win, grid, ROWS, width), grid, start, end)
                    elif algo == 2:
                        bfs(lambda: draw(win, grid, ROWS, width), grid, start, end)

                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = make_grid(ROWS, width)

                if event.key == pygame.K_r:
                    return
                
    pygame.quit()


    
        
    
