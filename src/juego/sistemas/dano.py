from ursina import *

def apply_knockback(player, enemy_pos, force, dt):
    k = player.position - enemy_pos
    k.y = 0
    if k.length() > 0:
        k = k.normalized()
        player.position += k * force * dt
