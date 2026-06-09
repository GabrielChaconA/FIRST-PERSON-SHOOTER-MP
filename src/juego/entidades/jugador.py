from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from .arma import create_weapon


def create_player():
    player = FirstPersonController(
        position=(1, 3, 0),
        speed=7
    )
    player.gravity = 1

    weapon = create_weapon()
    slide_camera_y = camera.position.y

    return player, weapon, slide_camera_y
