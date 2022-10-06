import time
from snek import Snek
from world import World
    
world = World()
snek = Snek(world)

game_over_counter = 0

while(True):
    if world.game_over:
        game_over_counter = game_over_counter + 1
    
    if game_over_counter == 30:
        break

    world.cycle()
    snek.cycle()
    world.render()
    
    time.sleep(.1)