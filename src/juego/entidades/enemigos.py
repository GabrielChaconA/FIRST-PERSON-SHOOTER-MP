from ursina import *
import random

MESH_SCALES = {
    'creeper': 0.40,
    'enderman': 0.25,
    'mutant_enderman': 0.90,
    'skeleton': 0.20,
    'warden': 1.40,
    'minecraft_wither': 2.55,
}

HITBOX_SCALES = {
    'creeper': Vec3(0.4, 0.3, 0.6),
    'enderman': Vec3(0.6, 0.8, 0.7),
    'mutant_enderman': Vec3(0.9, 0.8, 0.9),
    'skeleton': Vec3(0.5, 0.9, 0.5),
    'warden': Vec3(1.0, 2, 1.0),
    'minecraft_wither': Vec3(1.0, 1.4, 1.0)
}

MESH_Y_OFFSETS = {
    'creeper': HITBOX_SCALES['creeper'].y,
    'enderman': 1.5,
    'mutant_enderman': HITBOX_SCALES['mutant_enderman'].y,
    'skeleton': 1.4,
    'warden': 0.0,
    'minecraft_wither': HITBOX_SCALES['minecraft_wither'].y
}

HEADBOX_OFFSETS = {
    'creeper': Vec3(0, HITBOX_SCALES['creeper'].y * 1.2, 0),
    'enderman': Vec3(0, HITBOX_SCALES['enderman'].y * 1.4, 0),
    'mutant_enderman': Vec3(0, HITBOX_SCALES['mutant_enderman'].y * 1.4, 0),
    'skeleton': Vec3(0, HITBOX_SCALES['skeleton'].y * 1.3, 0),
    'warden': Vec3(0, HITBOX_SCALES['warden'].y * 1.4, 0),
    'minecraft_wither': Vec3(0, HITBOX_SCALES['minecraft_wither'].y * 1.5, 0)
}

HEADBOX_SCALES = {
    'creeper': Vec3(3, 20, 3),
    'enderman': Vec3(0.6, 14, 0.6),
    'mutant_enderman': Vec3(0.9, 12, 0.9),
    'skeleton': Vec3(2, 12, 0.5),
    'warden': Vec3(1.0, 0.8, 1.0),
    'minecraft_wither': Vec3(1.0, 0.8, 1.0)
}


class BaseMonster(Entity):
    def __init__(self, position, mesh_model, mesh_scale, mesh_offset_y,
                 speed, max_health, collider_scale,
                 head_offset, head_scale):
        super().__init__(
            model=None,
            position=position,
            scale=collider_scale,
            collider='box'
        )

        self.health = max_health
        self.max_health = max_health
        self.speed = speed

        self.mesh = Entity(
            parent=self,
            model=mesh_model,
            scale=mesh_scale,
            y=mesh_offset_y,
            rotation=(0, 180, 0)
        )

        self.headbox = Entity(
            parent=self,
            model='cube',
            collider='box',
            position=head_offset,
            scale=head_scale,
            color=color.clear
        )

        bar_y = collider_scale.y * 2.0

        self.bar_bg = Entity(parent=self, model='quad', color=color.black,
                             scale=(0.4, 0.07), position=(0, bar_y, 0))

        self.bar_fg = Entity(parent=self, model='quad', color=color.red,
                             scale=(0.38, 0.05), position=(0, bar_y, -0.01))

    def update_bar(self):
        self.bar_fg.scale_x = 0.38 * max(self.health, 0) / self.max_health


class CreeperMonster(BaseMonster):
    def __init__(self, pos):
        super().__init__(
            pos, '../Modelos_3d/minecraft_creeper.glb',
            MESH_SCALES['creeper'], MESH_Y_OFFSETS['creeper'],
            random.uniform(1.5, 2.2), 80, HITBOX_SCALES['creeper'],
            HEADBOX_OFFSETS['creeper'], HEADBOX_SCALES['creeper']
        )
        self.mesh.rotation_y += 180


class SkeletonMonster(BaseMonster):
    def __init__(self, pos):
        super().__init__(
            pos, '../Modelos_3d/minecraft_-_skeleton.glb',
            MESH_SCALES['skeleton'], MESH_Y_OFFSETS['skeleton'],
            random.uniform(1.6, 2.2), 90, HITBOX_SCALES['skeleton'],
            HEADBOX_OFFSETS['skeleton'], HEADBOX_SCALES['skeleton']
        )


class EndermanMonster(BaseMonster):
    def __init__(self, pos):
        super().__init__(
            pos, '../Modelos_3d/minecraft_-_enderman.glb',
            MESH_SCALES['enderman'], MESH_Y_OFFSETS['enderman'],
            random.uniform(1.8, 2.4), 150, HITBOX_SCALES['enderman'],
            HEADBOX_OFFSETS['enderman'], HEADBOX_SCALES['enderman']
        )


class MutantEndermanMonster(BaseMonster):
    def __init__(self, pos):
        super().__init__(
            pos, '../Modelos_3d/minecraft_mutant_enderman.glb',
            MESH_SCALES['mutant_enderman'], MESH_Y_OFFSETS['mutant_enderman'],
            random.uniform(2.0, 2.6), 250, HITBOX_SCALES['mutant_enderman'],
            HEADBOX_OFFSETS['mutant_enderman'], HEADBOX_SCALES['mutant_enderman']
        )
        self.mesh.rotation_y += 180


class WardenMonster(BaseMonster):
    def __init__(self, pos):
        super().__init__(
            pos, '../Modelos_3d/minecraft_warden.glb',
            MESH_SCALES['warden'], MESH_Y_OFFSETS['warden'],
            random.uniform(1.4, 1.8), 300, HITBOX_SCALES['warden'],
            HEADBOX_OFFSETS['warden'], HEADBOX_SCALES['warden']
        )


class WitherMonster(BaseMonster):
    def __init__(self, pos):
        super().__init__(
            pos, '../Modelos_3d/minecraft_wither.glb',
            MESH_SCALES['minecraft_wither'], MESH_Y_OFFSETS['minecraft_wither'],
            random.uniform(1.2, 1.7), 400, HITBOX_SCALES['minecraft_wither'],
            HEADBOX_OFFSETS['minecraft_wither'], HEADBOX_SCALES['minecraft_wither']
        )
        self.mesh.rotation_y += 180
