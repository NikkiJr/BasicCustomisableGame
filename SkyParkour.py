import time
import pygame as py
import os
import random

py.init()
py.font.init()
py.mixer.init()

########################################  Main variables  #################################################

BASE_PLAYER_VEL = 8
PLAYER_SIZE = 30

POWER_UP_SIZE = 40
FIRE_SIZE = 40
CHECKPOINT_SIZE = 35

WIDTH, HEIGHT = 1400, 1040
COLOR = (0, 0, 0)
GRAVITY = 0.5

FONT = py.font.SysFont('comicsans', 30)
WIN = py.display.set_mode((WIDTH, HEIGHT))
py.display.set_caption('Sky Parkour')

########################################  Player Skins ####################################################

player_skins = [
    py.Surface((PLAYER_SIZE, PLAYER_SIZE)),
    py.Surface((PLAYER_SIZE, PLAYER_SIZE))
]
player_skins[0].fill((255, 255, 255))
player_skins[1].fill((0, 255, 255))
current_skin = 0

########################################  BGM #############################################################

py.mixer.music.load(os.path.join('Game1Assets', 'BGM.mp3'))
py.mixer.music.set_volume(0.5)
py.mixer.music.play(-1)

########################################  Intro  ##########################################################

def show_intro():
    running = True
    start_button = py.Rect(WIDTH//2 - 100, 400, 200, 60)
    exit_button = py.Rect(WIDTH//2 - 100, 500, 200, 60)
    controls_button = py.Rect(WIDTH//2 - 100, 600, 200, 60)

    while running:
        WIN.fill(COLOR)
        title = FONT.render("Welcome to Game1!", True, "white")
        WIN.blit(title, (WIDTH//2 - title.get_width()//2, 200))

        help_text = FONT.render("Click R to reset to the last checkpoint!", True, "white")
        WIN.blit(help_text, (WIDTH//2 - help_text.get_width()//2, 270))

        py.draw.rect(WIN, (0, 150, 0), start_button, border_radius=10)
        py.draw.rect(WIN, (150, 0, 0), exit_button, border_radius=10)
        py.draw.rect(WIN, (0, 0, 150), controls_button, border_radius=10)

        start_text = FONT.render("Start", True, "white")
        WIN.blit(start_text, (start_button.centerx - start_text.get_width()//2,
                              start_button.centery - start_text.get_height()//2))

        exit_text = FONT.render("Exit", True, "white")
        WIN.blit(exit_text, (exit_button.centerx - exit_text.get_width()//2,
                             exit_button.centery - exit_text.get_height()//2))

        controls_text = FONT.render("Controls", True, "white")
        WIN.blit(controls_text, (controls_button.centerx - controls_text.get_width()//2,
                                 controls_button.centery - controls_text.get_height()//2))

        py.display.update()

        for event in py.event.get():
            if event.type == py.QUIT:
                py.quit()
                quit()
            if event.type == py.MOUSEBUTTONDOWN:
                mouse_pos = py.mouse.get_pos()
                if start_button.collidepoint(mouse_pos):
                    running = False
                elif controls_button.collidepoint(mouse_pos):
                    print('1. Press ESC to pause the game')
                    print('2. Press R to restart to the last checkpoint.')

                elif exit_button.collidepoint(mouse_pos):
                    py.quit()
                    quit()

########################################  Seed Input  #####################################################

def get_seed():
    seed_active = True
    user_text = ''
    input_box = py.Rect(WIDTH//2 - 150, 350, 300, 50)
    info_text = FONT.render("Enter a world seed (or leave empty for random):", True, "white")

    while seed_active:
        WIN.fill(COLOR)
        WIN.blit(info_text, (WIDTH//2 - info_text.get_width()//2, 250))
        py.draw.rect(WIN, (50, 50, 50), input_box, border_radius=10)
        py.draw.rect(WIN, (255, 255, 255), input_box, 2, border_radius=10)

        txt_surface = FONT.render(user_text, True, (255, 255, 255))
        WIN.blit(txt_surface, (input_box.x + 10, input_box.y + 10))

        enter_text = FONT.render("Press ENTER to continue", True, "gray")
        WIN.blit(enter_text, (WIDTH//2 - enter_text.get_width()//2, 420))
        py.display.update()

        for event in py.event.get():
            if event.type == py.QUIT:
                py.quit()
                quit()
            if event.type == py.KEYDOWN:
                if event.key == py.K_RETURN:
                    seed_active = False
                elif event.key == py.K_BACKSPACE:
                    user_text = user_text[:-1]
                else:
                    if len(user_text) < 15:
                        user_text += event.unicode

    if user_text.strip() == '':
        seed_value = random.randint(0, 999999999)
    else:
        try:
            seed_value = int(user_text)
        except ValueError:
            seed_value = hash(user_text) % 999999999

    return seed_value

########################################  Game Setup  #####################################################

# Platforms
PF1 = py.Rect(200, 800, 200, 50)
PF2 = py.Rect(500, 700, 200, 50)
PF3 = py.Rect(800, 600, 200, 50)
PF4 = py.Rect(1100, 500, 200, 50)
PF5 = py.Rect(1400, 400, 200, 50)
PF6 = py.Rect(1700, 500, 200, 50)
PF7 = py.Rect(2000, 700, 200, 50)
PF8 = py.Rect(2400, 800, 300, 50)
PlatformList = [PF1, PF2, PF3, PF4, PF5, PF6, PF7, PF8]

# Player
Player = py.Rect(300, HEIGHT - PLAYER_SIZE - 500, PLAYER_SIZE, PLAYER_SIZE)

# Background
bg_img = py.image.load(os.path.join('Game1Assets', 'bg.png')).convert()
bg_img = py.transform.scale(bg_img, (WIDTH, HEIGHT))

# Health Power-Up
Healer1 = py.Rect(PF1.centerx - POWER_UP_SIZE//2, PF1.top - POWER_UP_SIZE, POWER_UP_SIZE, POWER_UP_SIZE)
healer_img = py.image.load(os.path.join('Game1Assets', 'Health.png')).convert_alpha()
healer_img = py.transform.scale(healer_img, (Healer1.width, Healer1.height))

# Fires
Fire1 = py.Rect(PF3.centerx - FIRE_SIZE//2, PF3.top - FIRE_SIZE, FIRE_SIZE, FIRE_SIZE)
Fires = [Fire1]

# Checkpoints
Checkpoint1 = py.Rect(PF1.centerx - CHECKPOINT_SIZE//2, PF1.top - CHECKPOINT_SIZE, CHECKPOINT_SIZE, CHECKPOINT_SIZE)
Checkpoints = [Checkpoint1]
checkpoint_count = 0
last_checkpoint_index = -1

# Lists
PowerUps = [Healer1]
clock = py.time.Clock()
velocity_y = 0
on_ground = False
last_hit_time = 0
damage_cooldown = 1000
camera_x = 0
HEALTH_VALUE = 100

# Last checkpoint
last_checkpoint = {
    "player_x": Player.x,
    "player_y": Player.y,
    "health": HEALTH_VALUE,
    "velocity_y": 0
}

########################################  Health Bar  #####################################################

def draw_health_bar(surface, x, y, health, max_health):
    py.draw.rect(surface, (80, 80, 80), (x - 2, y - 2, 104, 14))
    health_ratio = max(health, 0) / max_health
    bar_width = 100 * health_ratio
    if health_ratio > 0.6:
        color = (0, 255, 0)
    elif health_ratio > 0.3:
        color = (255, 255, 0)
    else:
        color = (255, 0, 0)
    py.draw.rect(surface, color, (x, y, bar_width, 10))

########################################  Pause Menu #####################################################

def show_pause_menu():
    py.mixer.music.pause()
    paused = True
    resume_button = py.Rect(WIDTH//2 - 100, 400, 200, 60)
    exit_button = py.Rect(WIDTH//2 - 100, 500, 200, 60)

    while paused:
        WIN.fill((30, 30, 30))
        title = FONT.render("Game Paused", True, "white")
        WIN.blit(title, (WIDTH//2 - title.get_width()//2, 200))

        py.draw.rect(WIN, (0, 150, 0), resume_button, border_radius=15)
        py.draw.rect(WIN, (150, 0, 0), exit_button, border_radius=15)

        resume_text = FONT.render("Resume", True, "white")
        WIN.blit(resume_text, (resume_button.centerx - resume_text.get_width()//2,
                               resume_button.centery - resume_text.get_height()//2))
        exit_text = FONT.render("Exit", True, "white")
        WIN.blit(exit_text, (exit_button.centerx - exit_text.get_width()//2,
                             exit_button.centery - exit_text.get_height()//2))
        py.display.update()

        for event in py.event.get():
            if event.type == py.QUIT:
                py.quit()
                quit()
            if event.type == py.MOUSEBUTTONDOWN:
                mouse_pos = py.mouse.get_pos()
                if resume_button.collidepoint(mouse_pos):
                    paused = False
                elif exit_button.collidepoint(mouse_pos):
                    py.quit()
                    quit()
            if event.type == py.KEYDOWN:
                if event.key == py.K_ESCAPE:
                    paused = False
    py.mixer.music.unpause()

########################################  Draw Function  ##################################################

def draw(Player, PlatformList, Fires, HEALTH_VALUE, camera_x, Checkpoints, PowerUps, checkpoint_count, seed_value):
    WIN.blit(bg_img, (0, 0))
    WIN.blit(player_skins[current_skin], (Player.x - camera_x, Player.y))

    for cp in Checkpoints:
        py.draw.rect(WIN, 'yellow', (cp.x - camera_x, cp.y, cp.width, cp.height))
    for platform in PlatformList:
        py.draw.rect(WIN, (200, 200, 200),
                     (platform.x - camera_x, platform.y, platform.width, platform.height))
    for f in Fires:
        points = [
            (f.x - camera_x + f.width//2, f.y),
            (f.x - camera_x, f.y + f.height),
            (f.x - camera_x + f.width, f.y + f.height)
        ]
        py.draw.polygon(WIN, (255, 100, 0), points)
    for p in PowerUps:
        WIN.blit(healer_img, (p.x - camera_x, p.y))

    draw_health_bar(WIN, 20, 20, HEALTH_VALUE, 100)
    counter_text = FONT.render(f"Checkpoints: {checkpoint_count}", True, "white")
    WIN.blit(counter_text, (20, 40))
    seed_text = FONT.render(f"Seed: {seed_value}", True, "white")
    WIN.blit(seed_text, (20, 90))
    py.display.update()

########################################  Infinite Terrain  ###############################################

def generate_new_platform(last_platform_x):
    max_attempts = 10
    attempt = 0
    while attempt < max_attempts:
        width = random.randint(150, 300)
        height = 40
        x = last_platform_x + random.randint(150, 300)
        y = random.randint(HEIGHT - 400, HEIGHT - 100)
        new_platform = py.Rect(x, y, width, height)
        overlap = any(new_platform.colliderect(p.inflate(10, 10)) for p in PlatformList)
        if not overlap:
            PlatformList.append(new_platform)
            platform_objects = []
            if random.random() < 0.5:
                for _ in range(random.randint(1, max(1, width // 100))):
                    fire_x = new_platform.x + random.randint(0, max(0, new_platform.width - FIRE_SIZE))
                    fire_y = new_platform.top - FIRE_SIZE
                    fire_rect = py.Rect(fire_x, fire_y, FIRE_SIZE, FIRE_SIZE)
                    if not any(fire_rect.colliderect(p) for p in PlatformList):
                        Fires.append(fire_rect)
                        platform_objects.append(fire_rect)

            if random.random() < 0.3:
                power_x = new_platform.x + 20
                power_y = new_platform.top - POWER_UP_SIZE
                p = py.Rect(power_x, power_y, POWER_UP_SIZE, POWER_UP_SIZE)
                if not any(p.colliderect(obj) for obj in PlatformList + Fires):
                    PowerUps.append(p)
                    platform_objects.append(p)

            if len(PlatformList) % 8 == 0:
                free_for_checkpoint = True
                for obj in platform_objects:
                    test_cp = py.Rect(new_platform.centerx - CHECKPOINT_SIZE//2,
                                      new_platform.top - CHECKPOINT_SIZE,
                                      CHECKPOINT_SIZE, CHECKPOINT_SIZE)
                    if test_cp.colliderect(obj):
                        free_for_checkpoint = False
                        break
                if free_for_checkpoint:
                    cx = new_platform.centerx - CHECKPOINT_SIZE // 2
                    cy = new_platform.top - CHECKPOINT_SIZE
                    new_checkpoint = py.Rect(cx, cy, CHECKPOINT_SIZE, CHECKPOINT_SIZE)
                    Checkpoints.append(new_checkpoint)
            break
        attempt += 1

######################################## Main game code ######################################################

show_intro()
seed_value = get_seed()
random.seed(seed_value)
print(f"World Seed: {seed_value}")

run = True
while run:
    clock.tick(60)
    current_time = py.time.get_ticks()

    for event in py.event.get():
        if event.type == py.QUIT:
            run = False
        if event.type == py.KEYDOWN:
            if event.key == py.K_ESCAPE:
                show_pause_menu()
            if event.key == py.K_1:
                current_skin = 0
            if event.key == py.K_2:
                current_skin = 1

    keys = py.key.get_pressed()
    player_vel = BASE_PLAYER_VEL
    if keys[py.K_LSHIFT]:
        player_vel = 12

    dx = 0
    if keys[py.K_LEFT]:
        dx = -player_vel
    if keys[py.K_RIGHT]:
        dx = player_vel
    if keys[py.K_UP] and on_ground:
        velocity_y = -15
        on_ground = False

    prev_y = Player.y
    Player.x += dx
    for platform in PlatformList:
        if Player.colliderect(platform):
            if dx > 0:
                Player.right = platform.left
            elif dx < 0:
                Player.left = platform.right

    velocity_y += GRAVITY
    Player.y += velocity_y
    on_ground = False
    for platform in PlatformList:
        if Player.colliderect(platform):
            if prev_y + Player.height <= platform.top + 5:
                Player.bottom = platform.top
                velocity_y = 0
                on_ground = True
            elif prev_y >= platform.bottom - 5:
                Player.top = platform.bottom
                velocity_y = 0

    if Player.y > HEIGHT:
        HEALTH_VALUE = 0

    for i, cp in enumerate(Checkpoints):
        if Player.colliderect(cp) and i > last_checkpoint_index:
            last_checkpoint_index = i
            checkpoint_count += 1
            last_checkpoint = {
                "player_x": Player.x,
                "player_y": Player.y,
                "health": HEALTH_VALUE,
                "velocity_y": velocity_y
            }

    if keys[py.K_r]:
        Player.x = last_checkpoint["player_x"]
        Player.y = last_checkpoint["player_y"]
        HEALTH_VALUE = last_checkpoint["health"]
        velocity_y = last_checkpoint["velocity_y"]

    camera_x = max(0, Player.x - WIDTH // 2)

    for f in Fires:
        if Player.colliderect(f):
            if current_time - last_hit_time > damage_cooldown:
                HEALTH_VALUE -= 10
                last_hit_time = current_time

    for p in PowerUps:
        if Player.colliderect(p):
            HEALTH_VALUE += 60
            PowerUps.remove(p)
            HEALTH_VALUE = min(HEALTH_VALUE, 100)

    max_platform_x = max(platform.x for platform in PlatformList)
    if Player.x + 600 > max_platform_x:
        generate_new_platform(max_platform_x)

    if HEALTH_VALUE <= 0:
        Loss_text = FONT.render('You Lost!', 1, 'red')
        WIN.blit(Loss_text, (WIDTH / 2 - Loss_text.get_width() / 2, HEIGHT / 2 - 80))
        under_text = FONT.render('Press R to restart or ESC to quit', 1, 'white')
        WIN.blit(under_text, (WIDTH / 2 - under_text.get_width() / 2, HEIGHT / 2 - 25))
        py.display.update()
        waiting = True
        while waiting:
            for event in py.event.get():
                if event.type == py.QUIT:
                    run = False
                    waiting = False
                if event.type == py.KEYDOWN:
                    if event.key == py.K_r:
                        Player.x = last_checkpoint["player_x"]
                        Player.y = last_checkpoint["player_y"]
                        HEALTH_VALUE = last_checkpoint["health"]
                        velocity_y = last_checkpoint["velocity_y"]
                        waiting = False
                    elif event.key == py.K_ESCAPE:
                        run = False
                        waiting = False

    draw(Player, PlatformList, Fires, HEALTH_VALUE, camera_x, Checkpoints, PowerUps, checkpoint_count, seed_value)

py.quit()
