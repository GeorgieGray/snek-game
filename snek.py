import util
from direction import Direction

class SnekNode():
    def __init__(self, coordinate, neighbour = None):
        self.coordinate = coordinate
        self.previous_coordinate = None
        self.neighbour = neighbour

class Snek():
    def __init__(self, world):
        self.world = world
        self.nodes = self.__create()
        self.direction = Direction.RIGHT

    def __create(self):
        tail = SnekNode((15, 13))
        body = SnekNode((15, 14), tail)
        head = SnekNode((15, 15), body)

        return [head, body, tail]

    def grow(self):
        tail = self.nodes[-1]
        coordinate = tail.previous_coordinate
        new_node = SnekNode(coordinate)
        tail.neighbour = new_node
        self.nodes.append(new_node)

    def __handle_input(self):
        key = self.world.screen.getch()
        if util.is_valid_input(key):
            self.direction = key

    def __move(self):
        head = self.nodes[0]
        next_coordinate = util.get_next_coordinate(self.direction, head)
        if (next_coordinate == None):
            return

        previous_coordinate = head.coordinate
        head.previous_coordinate = previous_coordinate
        head.coordinate = next_coordinate
        current_part = head.neighbour
        
        while(current_part != None):
            (x, y) = previous_coordinate
            previous_coordinate = current_part.coordinate
            current_part.previous_coordinate = previous_coordinate
            current_part.coordinate = (x, y)
            current_part = current_part.neighbour

    def __render(self):
        self.world.render_snek(self)

    def __detect_collision(self):
        head = self.nodes[0]
        (x1, y1) = head.coordinate

        for i, node in enumerate(self.nodes):
            if i == 0:
                continue

            (x2, y2) = node.coordinate

            if x1 == x2 and y1 == y2:
                self.world.game_over = True
                break

    def cycle(self):
        self.__handle_input()
        self.__move()
        self.__render()
        self.__detect_collision()