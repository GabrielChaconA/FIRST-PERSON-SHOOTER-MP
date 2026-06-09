from ursina import *

def setup_window():
    window.title = 'SHOOTER-3D'
    window.borderless = False
    window.fps_counter.enabled = True
    mouse.locked = True
    window.color = color.rgb(10, 10, 20)

def setup_scene():
    global escenario, piso

    escenario = Entity(
        model='../Modelos_3d/laundry.glb',
        scale=1,
        position=(0, 0, 0),
        collider=None
    )

    piso = Entity(
        model='plane',
        scale=200,
        position=(0, 0, 0),
        collider='box',
        visible=False
    )

    DirectionalLight(direction=(1, -1, -1), shadows=True)
    AmbientLight(color=color.rgba(160, 160, 160, 255))
