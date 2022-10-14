from src.direction import Direction
import math


def is_valid_input(key, direction):
    valid = [Direction.LEFT, Direction.UP, Direction.RIGHT, Direction.DOWN]

    opposite_keys = {
        Direction.LEFT: Direction.RIGHT,
        Direction.RIGHT: Direction.LEFT,
        Direction.UP: Direction.DOWN,
        Direction.DOWN: Direction.UP
    }

    if key in valid:
        opposite = opposite_keys[direction]
        if key == opposite:
            return False

        return True
    else:
        return False


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


def center_text(string, text):
    text_arr = list(text)
    out = list(string)

    width = len(out)
    text_width = len(text_arr)

    middle = math.floor(width / 2)
    start = middle - math.ceil(text_width / 2)

    for i in range(text_width):
        out[i + start] = text_arr[i]

    prefix = "".join([' '] * text_width)

    return prefix + "".join(out)
