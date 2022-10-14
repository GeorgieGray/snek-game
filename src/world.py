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
    if b is None:
        char = '   '
        return a + char

    character = Character.SNEK if isinstance(b, SnekNode) else Character.NOM
    return a + character


def create_line(length):
    line_segments = ['---'] * length
    line_segments[0] = '+--'
    line_segments[len(line_segments) - 1] = '----+'
    return "".join(line_segments)


class World():
    def __init__(self, player=None):
        self.screen = curses.initscr()
        self.size = 22
        self.grid = [None] * self.size
        self.playing = False
        self.game_over = False
        self.nom_coordinate = None
        self.line = create_line(self.size)
        self.score = 0
        self.player = player
        self.player_name_input = []

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
        needs_nom = True if self.nom_coordinate is None else False

        for i, node in enumerate(snek.nodes):
            if self.game_over is True or self.playing is False:
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
        if self.nom_coordinate is None:
            return

        (x, y) = self.nom_coordinate
        self.grid[x][y] = Nom()

    def cycle(self):
        self.screen.timeout(0)
        self.reset()
        self.render_nom()

    def get_player_line(self):
        arr = list(self.line)
        name = list(self.player.strip())
        player = list(' PLAYER: ')
        playerLength = len(player) + 2

        for i, char in enumerate(player):
            arr[i + 2] = char

        for i, char in enumerate(name):
            arr[i + playerLength] = char

        arr[playerLength + len(name)] = ' '

        return "".join(arr)

    def get_score_line(self):
        arr = list(self.line)
        score = list(' SCORE: ')
        scoreLength = len(score) + 2

        for i, char in enumerate(score):
            arr[i + 2] = char

        score = list(str(self.score))

        for i, digit in enumerate(score):
            arr[scoreLength + i] = digit

        arr[scoreLength + len(score)] = ' '

        return "".join(arr)

    def draw_line(self, index, text):
        whitespace = 12
        padding = int(whitespace / 2)
        self.screen.addstr(index, padding, text)

    def render_game_over(self):
        player_line = self.get_player_line()
        score_line = self.get_score_line()

        self.draw_line(0, player_line)

        for i in range(len(self.grid)):
            current = "".join(['   '] * len(self.grid))
            self.draw_line(i + 1, "|" + current + "|")

        empty_line = ['   '] * self.size
        game_over = util.center_text(empty_line, "GAME OVER")
        play_again = util.center_text(empty_line, "Play again?")
        yes = util.center_text(empty_line, "Yes (y)")
        no = util.center_text(empty_line, " No (n)")
        self.draw_line(8, "|" + game_over)
        self.draw_line(10, "|" + play_again)
        self.draw_line(12, "|" + yes)
        self.draw_line(13, "|" + no)

        self.draw_line(len(self.grid) + 1, score_line)

    def render_home(self):
        player_line = self.get_player_line()
        self.draw_line(0, player_line)

        for i in range(len(self.grid)):
            current = "".join(['   '] * len(self.grid))
            self.draw_line(i + 1, "|" + current + "|")

        empty_line = ['   '] * self.size
        title = [
            " #### #   # #### #   #",
            " #    ##  # #    #  # ",
            " #### # # # #### ###  ",
            "    # #  ## #    #  # ",
            " #### #   # #### #   #"
        ]

        for i, title_line in enumerate(title):
            centered_title_line = util.center_text(empty_line, title_line)
            self.draw_line(4 + i, "|" + centered_title_line)

        controls = util.center_text(empty_line, " Controls - WASD")
        up = util.center_text(empty_line, "Up (W)")
        left = util.center_text(empty_line, "Left (A)")
        down = util.center_text(empty_line, "Down (S)")
        right = util.center_text(empty_line, " Right (D)")
        start = util.center_text(empty_line, "Press (ENTER) to start")
        quit = util.center_text(empty_line, " Press (ESC) to quit")

        self.draw_line(10, "|" + controls)
        self.draw_line(12, "|" + up)
        self.draw_line(13, "|" + left)
        self.draw_line(14, "|" + down)
        self.draw_line(15, "|" + right)

        self.draw_line(17, "|" + start)
        self.draw_line(18, "|" + quit)

        self.draw_line(len(self.grid) + 1, self.line)

    def render_name_input(self):
        self.draw_line(0, self.line)

        for i in range(len(self.grid)):
            current = "".join(['   '] * len(self.grid))
            self.draw_line(i + 1, "|" + current + "|")

        empty_line = ['   '] * self.size
        prompt = util.center_text(empty_line, " Enter a username:")
        self.draw_line(14, "|" + prompt)

        username = "".join(self.player_name_input)
        username_is_even = len(self.player_name_input) % 2 == 0
        if not username_is_even:
            username = username + " "

        self.draw_line(16, "|" + util.center_text(empty_line, username))
        self.draw_line(len(self.grid) + 1, self.line)

    def render(self):
        if self.player is None:
            self.render_name_input()
        else:
            self.screen.erase()

            if self.playing:
                if self.game_over:
                    self.render_game_over()
                else:
                    self.draw_line(0, self.get_player_line())

                    for i, row in enumerate(self.grid):
                        current = functools.reduce(concat, row, '')
                        self.draw_line(i + 1, "|" + current + "|")

                    self.draw_line(len(self.grid) + 1, self.get_score_line())
            else:
                self.render_home()

        self.screen.refresh()
