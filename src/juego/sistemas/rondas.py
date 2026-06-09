from ursina import Vec3, Entity, color
import random, math
from juego.entidades.enemigos import (
    CreeperMonster,
    SkeletonMonster,
    EndermanMonster,
    MutantEndermanMonster,
    WardenMonster,
    WitherMonster,
)

def get_types_for_round(r, game_mode):
    if game_mode == 'hard':
        return [
            CreeperMonster,
            SkeletonMonster,
            EndermanMonster,
            MutantEndermanMonster,
            WardenMonster,
            WitherMonster
        ]
    if r == 1:
        return [CreeperMonster]
    if r == 2:
        return [CreeperMonster, SkeletonMonster]
    if r == 3:
        return [CreeperMonster, SkeletonMonster, EndermanMonster]
    if r == 4:
        return [CreeperMonster, SkeletonMonster, EndermanMonster, MutantEndermanMonster]
    if r == 5:
        return [CreeperMonster, SkeletonMonster, EndermanMonster, MutantEndermanMonster, WardenMonster]
    return [
        CreeperMonster,
        SkeletonMonster,
        EndermanMonster,
        MutantEndermanMonster,
        WardenMonster,
        WitherMonster
    ]

def get_enemy_count_for_round(r, game_mode, base_enemies, enemies_increment):
    if game_mode == 'hard':
        base = 10
        inc = enemies_increment + 1
    else:
        base = base_enemies
        inc = enemies_increment
    return base + (r - 1) * inc

def spawn_enemy_near_player(player, current_round, game_mode):
    dist = random.uniform(10, 30)
    angle = random.uniform(0, 360)
    x = player.x + math.cos(math.radians(angle)) * dist
    z = player.z + math.sin(math.radians(angle)) * dist
    cls_list = get_types_for_round(current_round, game_mode)
    mob_cls = random.choice(cls_list)
    return mob_cls(Vec3(x, 0.2, z))

def spawn_ammo_box(limit_x, limit_z):
    x = random.uniform(-limit_x, limit_x)
    z = random.uniform(-limit_z, limit_z)
    return Entity(
        model='cube', color=color.yellow, scale=(0.5, 0.3, 0.5),
        collider='box', position=(x, 0.25, z)
    )
