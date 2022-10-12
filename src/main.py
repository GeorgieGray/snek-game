import time
from src.choice import Choice
from src.snek import Snek
from src.world import World
    
def start_game():
    world = World()
    snek = Snek(world)

    while(True):
        if world.playing == False:
            world.render()
            key = world.screen.getch()
            if key == Choice.START:
                world.playing = True
            elif key == Choice.QUIT:
                break

            continue

        if world.game_over:
            key = world.screen.getch()
            if key == Choice.YES:
                world = World()
                snek = Snek(world)
                world.playing = True
            elif key == Choice.NO:
                world = World()
                snek = Snek(world)
                world.playing = False

        world.cycle()
        snek.cycle()
        world.render()
        
        time.sleep(.11)
    