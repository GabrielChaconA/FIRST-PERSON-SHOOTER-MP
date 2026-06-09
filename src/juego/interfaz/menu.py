from ursina import *

menu_entities = []
background_entity = None


def hide_menu():
    global menu_entities, background_entity
    if background_entity:
        destroy(background_entity)
        background_entity = None
    for e in menu_entities:
        destroy(e)
    menu_entities = []


def create_custom_button(text, position, base_border_color, hover_border_color, text_color, action):
    # Outer glowing border / frame
    border = Entity(
        parent=camera.ui,
        model='quad',
        color=base_border_color,
        scale=(0.4, 0.08),
        position=(position[0], position[1], 0)
    )
    
    # Inner sleek glass-morphic button
    btn = Button(
        parent=border,
        model='quad',
        color=color.rgba(10/255, 15/255, 25/255, 220/255),  # Normalized semi-transparent dark glass
        highlight_color=color.rgba(25/255, 35/255, 55/255, 230/255),  # Normalized hover color
        pressed_color=color.rgba(5/255, 8/255, 15/255, 240/255),
        scale=(0.96, 0.85),
        position=(0, 0, -0.01)
    )
    
    btn.text = text
    # Counteract both border and button scaling to make text uniform and clear
    btn.text_entity.scale_x = 2.0 / (border.scale_x * btn.scale_x)
    btn.text_entity.scale_y = 2.0 / (border.scale_y * btn.scale_y)
    btn.text_entity.color = text_color
    btn.text_entity.origin = (0, 0)
    btn.text_entity.align = 'center'
    
    # Dynamic animations for border color and scale on hover
    def on_hover():
        border.color = hover_border_color
        border.animate_scale((0.42, 0.088), duration=0.1, curve=curve.out_sine)
        
    def on_unhover():
        border.color = base_border_color
        border.animate_scale((0.4, 0.08), duration=0.1, curve=curve.out_sine)
        
    btn.on_mouse_enter = on_hover
    btn.on_mouse_exit = on_unhover
    btn.on_click = action
    
    return border


def show_menu(start_normal, start_hard, on_quit, set_round, clear_center):
    global menu_entities, background_entity

    mouse.locked = False
    clear_center()
    set_round("Round: -")

    background_entity = Entity(
        parent=camera.ui,
        model='quad',
        texture='../Capturas/Menu.png',
        scale=(2, 1.5),
        color=color.white
    )

    border_rondas = create_custom_button(
        text='R O U N D S',
        position=(0, 0.15),
        base_border_color=color.cyan,
        hover_border_color=color.white,
        text_color=color.cyan,
        action=lambda: (hide_menu(), start_normal())
    )

    border_dificil = create_custom_button(
        text='H A R D  M O D E',
        position=(0, 0.0),
        base_border_color=color.red,
        hover_border_color=color.white,
        text_color=color.red,
        action=lambda: (hide_menu(), start_hard())
    )

    border_quit = create_custom_button(
        text='Q U I T',
        position=(0, -0.15),
        base_border_color=color.gray,
        hover_border_color=color.white,
        text_color=color.white,
        action=on_quit
    )

    # Controls Panel Border / Frame
    controls_border = Entity(
        parent=camera.ui,
        model='quad',
        color=color.rgba(0/255, 255/255, 255/255, 80/255),  # Subtle cyan border
        scale=(1.1, 0.07),
        position=(0, -0.33, 0)
    )

    # Controls Panel Glass Background
    controls_bg = Entity(
        parent=controls_border,
        model='quad',
        color=color.rgba(10/255, 15/255, 25/255, 220/255),
        scale=(0.985, 0.85),
        position=(0, 0, -0.01)
    )

    # Controls text
    controls_text = Text(
        text="<cyan>[W, A, S, D]</cyan> Move   •   <cyan>[SHIFT]</cyan> Sprint   •   <cyan>[C]</cyan> Slide   •   <cyan>[L-CLICK]</cyan> Shoot   •   <cyan>[ESC]</cyan> Quit",
        parent=controls_bg,
        color=color.white,
        origin=(0, 0),
        position=(0, 0, -0.01)
    )

    # Counteract scaling for text inside panel
    controls_text.scale_x = 1.3 / (controls_border.scale_x * controls_bg.scale_x)
    controls_text.scale_y = 1.3 / (controls_border.scale_y * controls_bg.scale_y)
    controls_text.align = 'center'

    menu_entities = [border_rondas, border_dificil, border_quit, controls_border]
