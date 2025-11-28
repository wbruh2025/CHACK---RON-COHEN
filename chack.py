import pygame
import os

# אתחול pygame
pygame.init()

# --- מנגנון לתיקון נתיבים ---
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
def get_path(relative_path):
    return os.path.join(SCRIPT_DIR, relative_path)
# -----------------------------

# הגדרות מסך
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 640
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('שיעור אנימציה - Pygame')

clock = pygame.time.Clock()
FPS = 60

BLACK = (0, 0, 0)

# משתני דמות
character_x = SCREEN_WIDTH // 2
character_y = SCREEN_HEIGHT // 2
character_speed = 5
character_flip = False

# --- Jump / Physics ---
velocity_y = 0
GRAVITY = 1
JUMP_POWER = -14
is_jumping = False
GROUND_Y = character_y

# אנימציה
current_animation = 'Idle'
frame_index = 0
animation_timer = 0
ANIMATION_COOLDOWN = 100

# תנועה
moving_left = False
moving_right = False


def load_animation_frames(animation_name, scale=1.65):
    frames = []
    folder_path = get_path(os.path.join('img', 'player', animation_name))
    for file in sorted(os.listdir(folder_path)):
        img = pygame.image.load(os.path.join(folder_path, file)).convert_alpha()
        img = pygame.transform.scale(
            img,
            (int(img.get_width() * scale), int(img.get_height() * scale))
        )
        frames.append(img)
    return frames


def update_animation(animations, current_anim, frame_idx, anim_timer):
    now = pygame.time.get_ticks()
    if now - anim_timer > ANIMATION_COOLDOWN:
        anim_timer = now
        frame_idx += 1
        if frame_idx >= len(animations[current_anim]):
            frame_idx = 0
    return frame_idx, anim_timer


def draw_character(anim, name, idx, x, y, flip):
    img = anim[name][idx]
    img = pygame.transform.flip(img, flip, False)
    rect = img.get_rect(center=(x, y))
    screen.blit(img, rect)


# טעינת אנימציות
animations = {
    'Idle': load_animation_frames('Idle'),
    'Run': load_animation_frames('Run')
}

sprite_half = animations['Idle'][0].get_width() // 2

# לולאת המשחק
run = True
while run:
    clock.tick(FPS)

    # אירועים
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                moving_left = True
            if event.key == pygame.K_RIGHT:
                moving_right = True
            if event.key == pygame.K_SPACE and not is_jumping:
                velocity_y = JUMP_POWER
                is_jumping = True
            if event.key == pygame.K_ESCAPE:
                run = False

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                moving_left = False
            if event.key == pygame.K_RIGHT:
                moving_right = False

    # --- תנועה אופקית ---
    previous_x = character_x

    if moving_left:
        character_x -= character_speed
        character_flip = True
    elif moving_right:
        character_x += character_speed
        character_flip = False

    # גבולות (ימין קרוב יותר!)
    LEFT_LIMIT = sprite_half
    RIGHT_LIMIT = SCREEN_WIDTH - sprite_half - 10  # פחות מרווח ימינה

    character_x = max(LEFT_LIMIT, min(character_x, RIGHT_LIMIT))

    hit_edge = character_x == LEFT_LIMIT or character_x == RIGHT_LIMIT

    # --- קפיצה / כבידה ---
    velocity_y += GRAVITY
    character_y += velocity_y

    if character_y >= GROUND_Y:
        character_y = GROUND_Y
        velocity_y = 0
        is_jumping = False

    # --- אנימציה ---
    previous_animation = current_animation

    if hit_edge:
        current_animation = 'Idle'
    elif moving_left or moving_right:
        current_animation = 'Run'
    else:
        current_animation = 'Idle'

    if previous_animation != current_animation:
        frame_index = 0
        animation_timer = pygame.time.get_ticks()

    frame_index, animation_timer = update_animation(
        animations, current_animation, frame_index, animation_timer
    )

    # ציור
    screen.fill(BLACK)
    draw_character(
        animations, current_animation, frame_index,
        character_x, character_y, character_flip
    )

    pygame.display.update()

pygame.quit()