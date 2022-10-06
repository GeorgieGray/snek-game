import time
from src.choice import Choice
from src.snek import Snek
from src.world import World
    
def start_game():
    world = World()
    snek = Snek(world)

    while(True):
        if world.game_over:
            key = world.screen.getch()
            if key == Choice.YES:
                world = World()
                snek = Snek(world)
            elif key == Choice.NO:
                break

        world.cycle()
        snek.cycle()
        world.render()
        
        time.sleep(.11)