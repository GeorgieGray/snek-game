# Snek game

![hero](https://i.gyazo.com/c66ab9c9282e37725605b09fe230446d.png)

[Snek](https://georgie-gray-snek.herokuapp.com/) is a fast paced video game inspired by the original Snake game for Nokia phones starting with the Nokia 6110 in 1998.

The game has four main views:
- Username entry view
- Home view
- Gameplay view
- Gameover view

The game is deployed to Heroku, see it here:  
https://georgie-gray-snek.herokuapp.com/

## Table of Contents
- [Target Demographic](#target-demographic)
- [User Stories](#user-stories)
- [Features](#features)
- [Technology](#technology)
- [Project Structure](#project-structure)
- [Local Development](#local-development)
- [Deployment](#deployment)
- [Testing](#testing)
  - [Methodology](#methodology)
  - [Third-Party](#third-party)
    - [Python Linting](#python-linting)
- [Citations & Credits](#citations--credits)

## Target Demographic
- Anyone who has played Snake on a Nokia phone in the past
- Anyone who likes browser-based games
- Anyone interested to learn about and experience the classic game: Snake

## User Stories
- As a user, I want to personalise my experience while playing the game
- As a user, I want to understand how to play and which controls to use
- As a user, I want to have fun and be challenged
- As a user, I want to feel nostalgia for the classic Snake game

## Features
### Username entry view
The user is first greeted by the username entry prompt. It's a simple view which allows the user to personalise their gaming experience by entering a name.

![img](https://i.gyazo.com/51ae1137a98b431d6e0df049d03eb9ca.png)

As the user types, their draft username will appear below the prompt.

This input has some basic validation:
- The user must enter a name;
- It must have at least 3 characters.
- It cannot have more than 12 characters.
- Only alphanumerical characters and spaces are allowed.
- If the user attempts to submit this screen by pressing `Enter` without satisfying these rules they will not be allowed. 

![img](https://i.gyazo.com/e40474e5fdf4653a73bad00a3ca25c43.png)

At any time the user can press `Esc` to reset the view and start entering their name again. When playing Snek local on your machine you can press `Backspace` to delete characters as you would expect, when playing Snek deployed to Heroku the same is possible by pressing `Shift + Backspace`.

### Home view
The home view - often called the "title screen" in video games - presents the games logo, some instructions for how to control the snake during gameplay and controls for how to exit the title screen or start the game.

![img](https://i.gyazo.com/3ccea17c97bb9771c011f0ea7d208d7f.png)

The players name as entered in the username entry view is displayed at the top left.

![img](https://i.gyazo.com/1502717e164e623c1ddc14905af778b5.png)

As the instructions explain pressing `Esc` will return the user to the username entry view where they came from. Pressing `Enter` will begin the game.

### Gameplay view
This view is the games primary view, the main show. Here the player controls a snake using the `W`, `A`, `S` and `D` keys. The objective of the game is to collect the food represented as an `X` without colliding with the walls or with the snake itself.

![img](https://i.imgur.com/Y4nBhga.png)

Collecting food increases the score and causes the snake to grow at the back of its body, as the game progresses the game becomes more hazardous: the snakes body takes up more of the game area and navigating to the food becomes more complicated as a result.

#### Allowed movements during gameplay
There is some logic applied to inputs before the raw input is applied to the snake to change its direction. It is not possible to change directly to suddenly turn in the opposite direction, doing so would mean the snake will turn around and immediately eat itself causing a game over.

The rule is simple: you cannot go in the opposite direction of your current direction. Each direction has a set of valid _next directions_. If you are traveling `UP`, next you may travel `LEFT` or `RIGHT`. If you are travelling `LEFT`, next you may `UP` or `DOWN` - and so on.

The players name is still displayed in the top left.

![img](https://i.gyazo.com/1502717e164e623c1ddc14905af778b5.png)

The players score is displayed in the bottom left.

![img](https://i.gyazo.com/cd35d4d634b02a75bf79bb5f6e14231f.png)

There is no way to exit from this view other than to lose and be sent to the game over view.

### Game over view
The player loses by colliding with a wall or with the snakes body. When this happens the game immediately ends and they are sent to the game over view.

![img](https://i.gyazo.com/7a7a9316a63de1d1d2fec2218be733b8.png)

This view displays the players name and score in the same place as during gameplay, but neither can be changed at this point. This allows the user an opportunity to take a screenshot and share their score with others.

The user is prompted to decide if they would like to play again:
- Pressing `Y` will return them to the gameplay view with a fresh instance of the game.
- Pressing `N` will return them to the home view.

## Technology

- [Python 3.10.8](https://www.python.org/downloads/release/python-3108/)
- [Python Essentials Template](https://github.com/Code-Institute-Org/python-essentials-template)
- [Python curses module](https://docs.python.org/3/howto/curses.html)

This project depends on the Python Essentials Template as required by the codeinstitue submission guidelines. No third party libraries are used. The Python 3.10.8 standard library is used, including the `math`, `curses`, `time`, `functools` and `random` modules.

The `curses` module is responsible for all the rendering of UI to the terminal window.

## Project Structure

The majority of the structure is as mandated by the [Python Essentials Template](https://github.com/Code-Institute-Org/python-essentials-template). The file structure and supporting files are necessary for deploying the Snek Python terminal game to Heroku, and make it playable via the web.

### Source folder

The `src` (source) folder is where all of the projects code lives. The primary file `main.py` includes the `start_game()` function, `start_game()` is imported into `run.py` in the project root - this is how the project gets executed by the [Python Essentials Template](https://github.com/Code-Institute-Org/python-essentials-template).

`main.py` is responsible for starting the game, bootstrapping the `World` and `Snek` classes, handling non-game related keyboard input for menu navigation and handling the transition between each of the games views.

The remaining files in the folder each serve a specific purpose which support the games gameplay:
- `choice.py`:
  - A class which stores ASCII key numbers for four main choices the user can make while navigating menus. 
  - These are: `YES`, `NO`, `START`, `QUIT`.
  - The rationale for this file is that the numbers behind keys on a keyboard are otherwise magical, and this makes understanding those magic numbers a little easier in the games code.
- `direction.py`:
  - A class which stores ASCII key numbers for the four directions of movement: `UP`, `DOWN`, `LEFT` and `RIGHT`.
  - There is similar rationale for storing like them like this as there is with `choice.py`.
  - One other use for this file is that these same ASCII values are used to represent and understand the movement direction stored in the `Snek()` class as `Snek.direction`.
- `util.py`:
  - Utilities which aren't specific to any particular class.
  - These include things like:
    - Working out the next position for a node in the game world given a movement direction.
    - Centering text that's rendered to the screen.
- `nom.py`:
  - This is an empty class that represents the food in the game.
  - The primary reason for this to exist is so it's easy to differentiate between nodes of the `Snek()` and food nodes. The check is done like this: `isinstance(self.grid[x][y], Nom)`.
- `snek.py`:
  - The player character class, the snake.
  - This file is responsible for all things related to the snake during gameplay.
  - This includes:
    - Applying user input to change direction
    - Making the snake grow after eating
    - Remembering the position of each of the snakes body parts
    - Creating the initial snake body parts (head, body, tail) when the game starts
    - Handling collision with itself, the wall and food
    - Placing the snake into the game world and updating its position
- `world.py`:
  - The game world class.
  - This file is responsible for:
    - Holding the state of the game world
    - Executing each game cycle
    - Rendering the world and its inhabitants to the screen

## Local Development

There is no special tool used for local development, only the standard terminal application that comes with your operating system.

To run the game locally, from a terminal do: `python ./run.py`

## Deployment
The game is deployed to Heroku.

Here are some instructions so you can do it yourself:
1. Create an account on Heroku
2. Follow the instructions for [Creating the Heroku app](https://github.com/Code-Institute-Org/python-essentials-template#creating-the-heroku-app) from the [Python Essentials Template](https://github.com/Code-Institute-Org/python-essentials-template).
3. Install the [heroku CLI](https://devcenter.heroku.com/articles/heroku-cli)
4. Authenticate with the CLI: `heroku login`
5. Follow the [Deploying with Git](https://devcenter.heroku.com/articles/git) instructions to setup your git repo correctly to speak with Heroku.
6. When you're ready to deploy: `git push heroku main`

## Testing
### Methodology

1. Run the game and confirm it launches without throwing errors.
2. Test each of the username input validation rules are enforced correctly.
3. Test that pressing `Esc` resets the username input.
4. Input a valid username, press enter and see that you are navigated to the home view.
5. Observe that the entered username is displayed at the top left.
6. Press `Esc` to return to the username entry view.
7. Enter a different valid name, press `Enter` and see that you are navigated and that now the new name is displayed in the top left.
8. Press `Enter` to begin playing, observe that the gameplay view is displayed.
9. Observe that the snake has 3 nodes, is in the center and begins moving immediately, `RIGHT`.
10. Press WASD and see that the snake changes direction with respect to the rules described in the [Allowed movements during gameplay](#allowed-movements-during-gameplay) section.
11. Collect food and see that the snake grows and the scores increments.
12. Collide with wall and observe game over.
13. Collide with the snake and observe game over.
14. Observe that the username and score remain the same from the gameplay view.
15. On the game over view observe that `Y` starts the game again with score 0 but the same username. The snake should reset to the center of the gameplay view and have 3 nodes only.
16. On the game over view observe that `N` returns the player to the home view.
17. After being returned to the home view it should be possible to go to the username entry view or the gameplay view again, there should be no dead ends.

### Third-party

#### Python linting 
The `.py` files in `src` were linted using `pycodestyle`. The code is compliant with this linters rules.

## Citations & Credits

### Learning resources

- Introduction to `functools` module and the `reduce` function
  - https://realpython.com/python-reduce-function/

- `curses` programming with Python
  - https://docs.python.org/3/howto/curses.html#

- `curses` library reference
  - https://docs.python.org/3/library/curses.html

- Python Essentials Template
  - https://github.com/Code-Institute-Org/python-essentials-template

- Heroku documentation
  - https://devcenter.heroku.com/articles/heroku-cli
  - https://devcenter.heroku.com/articles/git