from ursina import *
import random, math

from juego.escena.escena import setup_window, setup_scene
from juego.entidades.jugador import create_player
from juego.sistemas.rondas import get_enemy_count_for_round, spawn_enemy_near_player, spawn_ammo_box
from juego.sistemas.disparo import create_bullet
from juego.sistemas.movimiento import clamp_player_position
from juego.sistemas.dano import apply_knockback
from juego.interfaz.ui import setup_ui
from juego.interfaz.menu import show_menu
from juego.entidades.enemigos import CreeperMonster

PLAYER_HP_MAX = 100
START_BULLETS_PER_ROUND = 20
BULLET_SPEED = 40
BULLET_OFFSET_Y = -0.6
BULLET_OFFSET_X = 0.30
DAMAGE_PER_BULLET = 35
HEADSHOT_MULTIPLIER = 2.0

LIMIT_X = 60
LIMIT_Z = 60

BASE_ENEMIES = 4
ENEMIES_INCREMENT = 2

AMMO_BOXES_PER_ROUND = 4
AMMO_PER_BOX = 8

SPRINT_SPEED = 11
WALK_SPEED = 7
STAMINA_MAX = 100
STAMINA_USE_RATE = 35
STAMINA_REGEN = 20

SLIDE_SPEED = 16.0
SLIDE_DURATION = 0.55
SLIDE_COOLDOWN = 1.0
SLIDE_CAMERA_OFFSET = -0.6

CREEPER_EXPLOSION_RADIUS = 1.0
CREEPER_EXPLOSION_DAMAGE = 80
KNOCKBACK_FORCE = 10

game_started = False
game_mode = None

player = None
weapon_gun = None

round_text = None
health_text = None
ammo_text = None
kills_text = None
center_msg = None
stamina_fg = None
health_fg = None

player_health = PLAYER_HP_MAX
player_stamina = STAMINA_MAX
bullets_left = START_BULLETS_PER_ROUND
player_alive = True

enemies = []
ammo_boxes = []
bullets = []
current_round = 0
kills = 0
enemies_alive = 0

slide_active = False
slide_timer = 0.0
slide_cooldown_timer = 0.0
slide_direction = Vec3(0,0,0)
slide_velocity = 0.0
slide_camera_original_y = 0.0


def start_round():
    global current_round, bullets_left, enemies_alive
    current_round += 1
    bullets_left = START_BULLETS_PER_ROUND
    enemies_alive = 0
    mode = "Normal" if game_mode == "normal" else "Hard"
    round_text.text = f"Round: {current_round} ({mode})"
    center_msg.text = f"ROUND {current_round}"
    invoke(lambda: setattr(center_msg,'text',''), delay=1.5)

    count = get_enemy_count_for_round(current_round, game_mode, BASE_ENEMIES, ENEMIES_INCREMENT)
    for _ in range(count):
        spawn_enemy()

    spawn_boxes()


def reset_lists():
    global enemies, bullets, ammo_boxes, enemies_alive, kills
    for e in enemies:
        destroy(e)
    for b in bullets:
        destroy(b)
    for x in ammo_boxes:
        destroy(x)
    enemies.clear()
    bullets.clear()
    ammo_boxes.clear()
    enemies_alive = 0
    kills = 0


def spawn_boxes():
    for _ in range(AMMO_BOXES_PER_ROUND):
        box = spawn_ammo_box(LIMIT_X, LIMIT_Z)
        ammo_boxes.append(box)


def spawn_enemy():
    global enemies_alive
    mob = spawn_enemy_near_player(player, current_round, game_mode)
    enemies.append(mob)
    enemies_alive += 1


def start_game(mode):
    global game_started, game_mode, player_health, player_stamina, bullets_left
    global current_round, player_alive
    global slide_active, slide_timer, slide_cooldown_timer, slide_velocity

    game_mode = mode
    game_started = True
    mouse.locked = True

    player_health = PLAYER_HP_MAX
    player_stamina = STAMINA_MAX
    bullets_left = START_BULLETS_PER_ROUND
    current_round = 0
    player_alive = True

    slide_active = False
    slide_timer = 0
    slide_cooldown_timer = 0
    slide_velocity = 0

    reset_lists()
    start_round()


def open_menu():
    def set_round(t):
        round_text.text = t
    def clear_center():
        center_msg.text = ""
    show_menu(
        start_normal=lambda: start_game('normal'),
        start_hard=lambda: start_game('hard'),
        on_quit=lambda: application.quit(),
        set_round=set_round,
        clear_center=clear_center
    )


def shoot():
    global bullets_left
    if not player_alive:
        return
    if bullets_left <= 0:
        return
    bullets_left -= 1
    bullet = create_bullet(camera, '../Modelos_3d/pocisk.obj', BULLET_OFFSET_X, BULLET_OFFSET_Y)
    bullets.append(bullet)


def input(key):
    global slide_active, slide_timer, slide_cooldown_timer
    global slide_direction, slide_velocity

    if key == 'left mouse down' and game_started:
        shoot()

    if key == 'c' and game_started and not slide_active and slide_cooldown_timer<=0 and player_alive:
        moving = any(held_keys[k] for k in ('w','a','s','d'))
        if moving:
            slide_active = True
            slide_timer = SLIDE_DURATION
            slide_cooldown_timer = SLIDE_COOLDOWN
            f = camera.forward
            v = Vec3(f.x,0,f.z)
            if v.length()>0:
                v = v.normalized()
            slide_direction = v
            slide_velocity = SLIDE_SPEED

    if key == 'escape':
        application.quit()


def update():
    global player_health, player_stamina, bullets_left, enemies_alive
    global kills, player_alive
    global slide_active, slide_timer, slide_cooldown_timer, slide_velocity

    if not game_started:
        return

    dt = time.dt

    clamp_player_position(player, LIMIT_X, LIMIT_Z)

    weapon_gun.position = Vec3(0, -0.1, 0.04)

    if slide_cooldown_timer>0:
        slide_cooldown_timer -= dt

    if slide_active:
        player.speed = 0
        player.position += slide_direction*slide_velocity*dt
        slide_velocity -= (SLIDE_SPEED/SLIDE_DURATION)*dt
        if slide_velocity<0:
            slide_velocity=0
        target = slide_camera_original_y + SLIDE_CAMERA_OFFSET
        camera.position = Vec3(
            camera.position.x,
            lerp(camera.position.y, target, 10*dt),
            camera.position.z
        )
        slide_timer -= dt
        if slide_timer<=0 or slide_velocity<=0:
            slide_active = False
    else:
        camera.position = Vec3(
            camera.position.x,
            lerp(camera.position.y, slide_camera_original_y, 10*dt),
            camera.position.z
        )
        moving = any(held_keys[k] for k in ('w','a','s','d'))
        if held_keys['shift'] and moving and player_stamina>0 and player_alive:
            player.speed = SPRINT_SPEED
            player_stamina -= STAMINA_USE_RATE * dt
        else:
            player.speed = WALK_SPEED
            player_stamina += STAMINA_REGEN * dt

    player_stamina = clamp(player_stamina, 0, STAMINA_MAX)
    stamina_fg.scale_x = 0.29 * (player_stamina / STAMINA_MAX)
    health_fg.scale_x = 0.29 * clamp(player_health/PLAYER_HP_MAX, 0, 1)

    for b in bullets[:]:
        b.position += b.forward_vec * BULLET_SPEED * dt
        b.life += dt
        if b.life > 3:
            destroy(b)
            bullets.remove(b)
            continue
        hit = False
        for e in enemies[:]:
            head = b.intersects(e.headbox)
            if head.hit:
                dmg = DAMAGE_PER_BULLET * HEADSHOT_MULTIPLIER
                e.health -= dmg
                e.update_bar()
                e.mesh.color = color.lime
                invoke(lambda m=e.mesh: setattr(m,'color',color.white), delay=0.15)
                destroy(b)
                bullets.remove(b)
                hit=True
                if e.health<=0:
                    destroy(e.bar_bg)
                    destroy(e.bar_fg)
                    destroy(e)
                    enemies.remove(e)
                    enemies_alive -= 1
                    kills+=1
                break
            body = b.intersects(e)
            if body.hit:
                dmg = DAMAGE_PER_BULLET
                e.health -= dmg
                e.update_bar()
                e.mesh.color = color.red
                invoke(lambda m=e.mesh: setattr(m,'color',color.white), delay=0.15)
                destroy(b)
                bullets.remove(b)
                hit=True
                if e.health<=0:
                    destroy(e.bar_bg)
                    destroy(e.bar_fg)
                    destroy(e)
                    enemies.remove(e)
                    enemies_alive -= 1
                    kills+=1
                break
        if hit:
            continue

    for e in enemies[:]:
        d = player.position - e.position
        d.y = 0
        if d.length()>0:
            d = d.normalized()
            e.position += d*e.speed*dt
            e.look_at(player.position)
            e.rotation_x = 0
            e.rotation_z = 0

        if isinstance(e, CreeperMonster) and distance(e.position, player.position)<CREEPER_EXPLOSION_RADIUS:
            player_health -= CREEPER_EXPLOSION_DAMAGE
            destroy(e.bar_bg)
            destroy(e.bar_fg)
            destroy(e)
            enemies.remove(e)
            enemies_alive -= 1
            continue

        if distance(e.position, player.position)<0.6:
            player_health -= 20*dt
            apply_knockback(player, e.position, KNOCKBACK_FORCE, dt)

    for x in ammo_boxes[:]:
        if distance(player.position, x.position)<1.2:
            bullets_left += AMMO_PER_BOX
            destroy(x)
            ammo_boxes.remove(x)

    if game_mode in ('normal','hard') and len(ammo_boxes)==0:
        spawn_boxes()

    if enemies_alive==0:
        start_round()

    health_text.text = f"HP: {int(player_health)}"
    ammo_text.text = f"Ammo: {bullets_left}"
    kills_text.text = f"Kills: {kills}"

    if player_health<=0 and player_alive:
        player_alive = False
        center_msg.text = "GAME OVER"


def setup_game():
    global round_text, health_text, ammo_text, kills_text
    global center_msg, stamina_fg, health_fg
    global player, weapon_gun, slide_camera_original_y

    setup_window()
    setup_scene()
    player, weapon_gun, slide_camera_original_y = create_player()

    (
        round_text,
        health_text,
        ammo_text,
        kills_text,
        center_msg,
        stamina_fg,
        health_fg
    ) = setup_ui()

    open_menu()
