from ursina import clamp

def clamp_player_position(player, limit_x, limit_z):
    player.x = clamp(player.x, -limit_x, limit_x)
    player.z = clamp(player.z, -limit_z, limit_z)
