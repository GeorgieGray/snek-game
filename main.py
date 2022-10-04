import curses
import time
import functools

class SnekNode():
    def __init__(self, coordinate, neighbour = None):
        self.coordinate = coordinate
        self.neighbour = neighbour

class Direction():
    LEFT = 97
    UP = 119
    RIGHT = 100
    DOWN = 115

def reset_grid():
    for x in range(0, size):
        for y in range(0, size):
            if not grid[x]:
                grid[x] = [None] * size
            grid[x][y] = None

def put_snek_in_grid(snek):
    for part in snek:
        (x, y) = part.coordinate
        grid[x][y] = part

def concat(a, b):
    if b == None:
        char = '   '
        return a + char
    return a + ' O '

def create_snek():
    tail = SnekNode((15, 13))
    body = SnekNode((15, 14), tail)
    head = SnekNode((15, 15), body)

    return (head, body, tail)

def next_direction(key):
    valid = [Direction.LEFT, Direction.UP, Direction.RIGHT, Direction.DOWN]

    if key in valid:
        return key
    else:
        return direction

def get_next_coordinate(direction, head):
    (x, y) = head.coordinate

    match direction:
        case Direction.LEFT:
            return (x, y - 1)
        case Direction.UP:
            return (x - 1, y)
        case Direction.RIGHT:
            return (x, y + 1)
        case Direction.DOWN:
            return (x + 1, y)
        case _:
            return None

def move_snek(direction):
    head = snek[0]
    next_coordinate = get_next_coordinate(direction, head)
    if (next_coordinate == None):
        return

    previous_coordinate = head.coordinate
    head.coordinate = next_coordinate
    current_part = head.neighbour
    
    while(current_part != None):
        (x, y) = previous_coordinate
        previous_coordinate = current_part.coordinate
        current_part.coordinate = (x, y)
        current_part = current_part.neighbour

size = 30
grid = [None] * size
direction = Direction.RIGHT
snek = create_snek()
reset_grid()
put_snek_in_grid(snek)
screen = curses.initscr()
frame = 0

while(frame < 200):  
    screen.timeout(0)
    frame = frame + 1

    key = screen.getch()
    if key != -1:
        direction = next_direction(key)

    move_snek(direction)
    reset_grid()
    put_snek_in_grid(snek)
    
    screen.clear()

    for i, row in enumerate(grid):
        current = functools.reduce(concat, row, '')
        screen.addstr(i, 0, current)

    # screen.addstr(0, 0, 'Key {0}'.format(key))
    # screen.addstr(1, 0, 'Direction {0}'.format(direction))
    screen.refresh()
    time.sleep(.1)