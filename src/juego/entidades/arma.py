from ursina import *

PLAYER_MODEL_SCALE = 0.003
PLAYER_MODEL_OFFSET = Vec3(0, -0.1, 0.04)
MODEL_PATH = '../Modelos_3d/fps_hands__sig_sauer_225.glb'

def create_weapon():
    weapon = Entity(
        parent=camera,
        model=MODEL_PATH,
        scale=PLAYER_MODEL_SCALE,
        position=PLAYER_MODEL_OFFSET,
        rotation=(0, 180, 0),
        unlit=True
    )
    return weapon
