from ursina import Entity, color

def create_bullet(camera, model_path, offset_x, offset_y):
    f = camera.forward.normalized()
    r = camera.right.normalized()
    u = camera.up.normalized()
    spawn = camera.world_position + f*1.2 + r*offset_x + u*offset_y

    b = Entity(
        model=model_path,
        scale=0.2,
        position=spawn,
        collider='box',
        color=color.white
    )
    b.look_at(spawn + f)
    b.rotation_x -= 90
    b.forward_vec = f
    b.life = 0

    return b
