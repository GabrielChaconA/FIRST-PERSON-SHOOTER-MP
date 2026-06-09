from ursina import *

def setup_ui():
    round_text = Text(text="Round: -", position=(0, .45), scale=2, color=color.yellow)
    health_text = Text(text="HP: 100", position=(-.85, .45))
    ammo_text = Text(text="Ammo: 20", position=(-.85, .40))
    kills_text = Text(text="Kills: 0", position=(-.85, .35))
    center_msg = Text(text="", origin=(0, 0), scale=3)

    stamina_bg = Entity(parent=camera.ui, model='quad', color=color.rgba(0,0,0,180),
                        scale=(0.3, 0.03), position=(-0.5, -0.45))
    stamina_fg = Entity(parent=camera.ui, model='quad', color=color.green,
                        scale=(0.29, 0.02), position=(-0.5, -0.45, -0.01))

    health_bg = Entity(parent=camera.ui, model='quad', color=color.rgba(0,0,0,180),
                       scale=(0.3, 0.03), position=(-0.5, -0.40))
    health_fg = Entity(parent=camera.ui, model='quad', color=color.red,
                       scale=(0.29, 0.02), position=(-0.5, -0.40, -0.01))

    return round_text, health_text, ammo_text, kills_text, center_msg, stamina_fg, health_fg
