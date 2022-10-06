from direction import Direction

def is_valid_input(key):
    valid = [Direction.LEFT, Direction.UP, Direction.RIGHT, Direction.DOWN]

    if key in valid:
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