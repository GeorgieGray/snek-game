import time
from curses import ascii
from src.choice import Choice
from src.snek import Snek
from src.world import World
    
def start_game():
    world = World()
    snek = Snek(world)

    while(True):
        if world.player == None:
            world.render()
            key = world.screen.getch()
            input_size = len(world.player_name_input)

            if key == Choice.QUIT:
                world = World()
                snek = Snek(world)
                continue
            
            if key == Choice.START:
                if len(world.player_name_input) < 3:
                    continue
                
                world.player = "".join(world.player_name_input)
                continue

            if (ascii.isalnum(key) or ascii.isspace(key)) and input_size < 12:
                world.player_name_input.append(chr(key))

            if key == ascii.BS and len(world.player_name_input) > 0:
                del world.player_name_input[-1]

            continue

        if world.playing == False:
            world.render()
            key = world.screen.getch()
            if key == Choice.START:
                world.playing = True
            elif key == Choice.QUIT:
                world = World()
                snek = Snek(world)

            continue

        if world.game_over:
            key = world.screen.getch()
            if key == Choice.YES:
                world = World(world.player)
                snek = Snek(world)
                world.playing = True
            elif key == Choice.NO:
                world = World(world.player)
                snek = Snek(world)
                world.playing = False

        world.cycle()
        snek.cycle()
        world.render()
        
        time.sleep(.11)
    