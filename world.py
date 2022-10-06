import curses
import functools
import util
import random
from snek import SnekNode
from nom import Nom

class Character():
    SNEK = ' O '
    NOM = ' X '

def concat(a, b):
    if b == None:
        char = '   '
        return a + char

    character = Character.SNEK if isinstance(b, SnekNode) else Character.NOM
    return a + character

class World():
    def __init__(self, size = 30):
        self.screen = curses.initscr()
        self.size = size
        self.grid = [None] * size
        self.game_over = False
        self.nom_coordinate = None

    def reset(self):
        for x in range(0, self.size):
            for y in range(0, self.size):
                if not self.grid[x]:
                    self.grid[x] = [None] * self.size
                self.grid[x][y] = None
    
    def create_nom(self):
        non_snake_coordinates = []

        for x in range(0, self.size):
            for y in range(0, self.size):
                if not isinstance(self.grid[x][y], SnekNode):
                    non_snake_coordinates.append((x, y))
        
        (x, y) = random.choice(non_snake_coordinates)
        self.nom_coordinate = (x, y)

    def render_snek(self, snek):
        needs_nom = True if self.nom_coordinate == None else False

        for i, node in enumerate(snek.nodes):
            if self.game_over == True:
                return
            
            (x, y) = node.coordinate

            if x > (self.size - 1) or x < 0 or y > (self.size - 1) or y < 0:
                self.game_over = True
                return
            
            is_head = i == 0
            if is_head and isinstance(self.grid[x][y], Nom):
                snek.grow()
                needs_nom = True

            self.grid[x][y] = node
        
        if needs_nom:
            self.create_nom()

    def render_nom(self):
        if self.nom_coordinate == None:
            return

        (x, y) = self.nom_coordinate
        self.grid[x][y] = Nom()

    def cycle(self):
        self.screen.timeout(0)
        self.reset()
        self.render_nom()

    def render(self):
        self.screen.clear()

        if self.game_over:
            self.screen.addstr(0, 0, "GAME OVER")
        else:
            for i, row in enumerate(self.grid):
                current = functools.reduce(concat, row, '')
                self.screen.addstr(i, 0, current)
        
        self.screen.refresh()