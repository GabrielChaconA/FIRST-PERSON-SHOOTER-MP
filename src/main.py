from ursina import Ursina
from juego.logica import setup_game, update as game_update, input as game_input

app = Ursina()

setup_game()

def update():
    game_update()

def input(key):
    game_input(key)

if __name__ == '__main__':
    app.run()
