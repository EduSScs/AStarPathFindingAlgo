"""
Eduardo Saldana Suarez
A Star Maze Program using Pygame
"""

# Imports
import pygame
from queue import PriorityQueue

# Start Color
PINK = (255, 102, 255)

# End Color
CYAN = (51, 255, 255)

# Empty Path
WHITE = (255, 255, 255)

# Wall
GREY = (170, 170, 170)

# Lines
BLACK = (0, 0, 0)

# Checking
ORANGE = (255, 102, 0)

# Checked
BLUE = (51, 51, 255)

# Path Found
GOLD = (255, 255, 51)

SCREEN_SIZE = 900
WINDOW = pygame.display.set_mode((SCREEN_SIZE,SCREEN_SIZE))
NUM_ROWS = 50

class Square:

    def __init__ (self, row, column, height, width):
        self.x = row*width
        self.y = column*height
        self.nexts = []
        self.color = WHITE
        self.row = row
        self.column = column
        self.height = height
        self.width = width

    # Check if a square is still able to continue
    def check_open(self):
        return self.color == ORANGE

    # Check if we have already visited a square
    def check_closed(self):
        return self.color == BLUE

    # Check if its a wall
    def check_wall(self):
        return self.color == GREY

    # Returns the row and column the square is in
    def location(self):
        return self.row, self.column

    # Marks the block as checked
    def mark_checked(self):
        self.color = BLUE

    # Marks the block as a possible path
    def mark_open(self):
        self.color = ORANGE
    
    # Marks a block as a wall
    def mark_wall(self):
        self.color = GREY

    # Marks the path found
    def mark_path(self):
        self.color = GOLD

    # Marks the start
    def mark_start(self):
        self.color = PINK

    # Marks the end
    def mark_end(self):
        self.color = CYAN

    def mark_empty(self):
        self.color = WHITE
    
    # Paints the square into the screen
    def paint(self):
        pygame.draw.rect(WINDOW, self.color, (self.x, self.y, self.width, self.height))

    def contiguous_squares(self, squares):
        self.nexts = []

        # Checks square on the left
        if self.column > 0 and not squares[self.row][self.column-1].check_wall():
            self.nexts.append(squares[self.row][self.column-1])

        # Checks square on the right
        if self.column < NUM_ROWS-1 and not squares[self.row][self.column+1].check_wall():
            self.nexts.append(squares[self.row][self.column+1])

        # Checks square above
        if self.row > 0 and not squares[self.row-1][self.column].check_wall():
            self.nexts.append(squares[self.row-1][self.column])

        # Checks square below
        if self.row < NUM_ROWS-1 and not squares[self.row+1][self.column].check_wall():
            self.nexts.append(squares[self.row+1][self.column])

def heuristic(place1, place2):
    # This is a way to quickly assign variables with the values we passed
    a, b = place1
    x, y = place2
    horizontal = a-x
    vertical = b-y
    return abs(horizontal)+abs(vertical)

def obtain_point(click, r, w):
    x, y = click
    space = w//r
    column = x//space
    row = y//space
    # We return the coordiantes in a y, x order
    return row, column

def get_values(r, w):
    values = []
    space = w//r

    for x in range(r):
        values.append([])
        for y in range(r):
            square = Square(x,y,space,space)
            values[x].append(square)
    
    return values

def lines(r, w):
    space = w//r

    # Drawing horizontal lines
    for x in range(r):
        pygame.draw.line(WINDOW, BLACK, (0,x*space), (w,x*space))
        
    
    # Drawing Vertical lines
    for y in range(r):
            pygame.draw.line(WINDOW, BLACK, (y*space,0), (y*space,w))
    

def update(values, r, w):
    WINDOW.fill(WHITE)
    
    # Each spot is colored with its respective color
    for row in values:
        for square in row:
            square.paint()

    lines(r, w)
    pygame.display.update()

def highlight_path(past, present, update):
    while present in past:
        present = past[present]
        present.mark_path()
        update()


def find_path(begin, stop, values, update):
    counter = 0
    possible_moves = PriorityQueue()
    possible_moves.put((0, counter, begin))
    unchecked_moves = {begin}

    # Keeps track of each square past square
    past = {}

    # Keeps track of the shortest path from the start node to the current node
    g = {Square: float('inf') for r in values for Square in r}

    # Keeps track fo the heuristic of the current node to the end node
    f = {Square: float('inf') for r in values for Square in r}

    g[begin] = 0

    # The f score (g + h) of the start square is just gonna be the heuristic
    f[begin] = heuristic(begin.location(), stop.location())

    while not possible_moves.empty():

        considering = possible_moves.get()[2]

        # CHecks to see if we arrived at the end
        if considering==stop:
            highlight_path(past, stop, update)
            return True

        for nexts in considering.nexts:
            new_g = g[considering]+1

            # Checks to see if the neighbor its checking is a better alternative
            if new_g < g[nexts]:
                past[nexts] = considering
                g[nexts] = new_g
                f[nexts] = heuristic(nexts.location(), stop.location())

                if nexts not in unchecked_moves:
                    counter = 1 + counter
                    possible_moves.put((f[nexts],counter,nexts))
                    unchecked_moves.add(nexts)
                    nexts.mark_open()
        update()

        if considering!=begin:
            considering.mark_checked()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
    
    return False



def main(w):
    values = get_values(NUM_ROWS, w)

    still_running = True
    begin = None
    stop = None

    while still_running:
        update(values, NUM_ROWS, w)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                still_running = False

        # Left Button
        if pygame.mouse.get_pressed()[0]:
            location = pygame.mouse.get_pos()
            r, c = obtain_point(location, NUM_ROWS, w)
            temp_square = values[c][r]

            if temp_square!= stop and not begin:
                begin = temp_square
                begin.mark_start()

            elif temp_square!= begin and not stop:
                stop = temp_square
                stop.mark_end()

            elif temp_square != begin and temp_square != stop:
                temp_square.mark_wall()

        if pygame.key.get_pressed()[pygame.K_BACKSPACE]:
            location = pygame.mouse.get_pos()
            r, c = obtain_point(location, NUM_ROWS, w)
            temp_square = values[c][r]

            if temp_square==begin:
                begin = None
            
            elif temp_square==stop:
                stop = None

            temp_square.mark_empty()
        
        if pygame.key.get_pressed()[pygame.K_r]: 
            begin = None
            stop = None
            for r in values:
                for Square in r:
                    Square.mark_empty()
        
        if pygame.key.get_pressed()[pygame.K_RETURN]:
            if begin != None and stop != None:
                for r in values:
                    for Square in r:
                        Square.contiguous_squares(values)

                find_path(begin, stop, values, lambda:  update(values, NUM_ROWS, w))

    pygame.quit()

        

main(SCREEN_SIZE)