import curses
import functools
import src.util as util
import random
from src.snek import SnekNode
from src.nom import Nom

class Character():
    SNEK = ' O '
    NOM = ' X '

def concat(a, b):
    if b == None:
        char = '   '
        return a + char

    character = Character.SNEK if isinstance(b, SnekNode) else Character.NOM
    return a + character

def create_line(length):
    line_segments = ['---'] * length
    line_segments[0] = '+--'
    line_segments[len(line_segments) - 1] =  '----+'
    return "".join(line_segments)

class World():
    def __init__(self):
        self.screen = curses.initscr()
        self.size = 22
        self.grid = [None] * self.size
        self.game_over = False
        self.nom_coordinate = None
        self.line = create_line(self.size)
        self.score = 0

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
                self.score = self.score + 1
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

    def add_score_to_line(self, line):
        arr = list(line)
        arr[2] = ' '
        arr[3] = 'S'
        arr[4] = 'C'
        arr[5] = 'O'
        arr[6] = 'R'
        arr[7] = 'E'
        arr[8] = ' '

        score = list(str(self.score))

        for i, digit in enumerate(score):
            arr[9 + i] = digit
        
        arr[9 + len(score)] = ' '

        return "".join(arr)

    def render(self):
        self.screen.clear()
        score_line = self.add_score_to_line(self.line)

        if self.game_over:
            self.screen.addstr(0, 0, self.line)

            for i in range(len(self.grid)):
                current = "".join(['   '] * len(self.grid))
                self.screen.addstr(i + 1, 0, "|" + current + "|")

            empty_line = ['   '] * self.size
            game_over = util.center_text(empty_line, "GAME OVER")
            play_again = util.center_text(empty_line, "Play again?")
            yes = util.center_text(empty_line, "Yes (y)")
            no = util.center_text(empty_line, " No (n)")
            self.screen.addstr(8, 0, "|" + game_over)
            self.screen.addstr(10, 0, "|" + play_again)
            self.screen.addstr(12, 0, "|" + yes)
            self.screen.addstr(13, 0, "|" + no)

            self.screen.addstr(len(self.grid) + 1, 0, score_line)
        else:
            self.screen.addstr(0, 0, self.line)

            for i, row in enumerate(self.grid):
                current = functools.reduce(concat, row, '')
                self.screen.addstr(i + 1, 0, "|" + current + "|")

            self.screen.addstr(len(self.grid) + 1, 0, score_line)
        
        self.screen.refresh()