import pygame
import sys
import time
import random

# --- Initialization ---
pygame.init()
screen = pygame.display.set_mode((800, 480))
pygame.display.set_caption("Robot Eyes")
clock = pygame.time.Clock()

# --- Constants ---
GLOW_RADIUS = 50
EYE_COLOR = (0, 255, 255)
LEFT_CENTER = (800 // 2 - 150, 240)
RIGHT_CENTER = (800 // 2 + 150, 240)

# --- State ---
expression = "neutral"
expression_time = 0
is_blinking = False
blink_start = 0
next_blink = time.time() + random.uniform(3, 7)

# --- Drawing Functions ---
def draw_eye(surface, center, size, glow_radius, color):
    eye_surf = pygame.Surface((size[0] + glow_radius * 2, size[1] + glow_radius * 2), pygame.SRCALPHA)
    cx, cy = eye_surf.get_width() // 2, eye_surf.get_height() // 2

    for r in range(glow_radius, 0, -1):
        alpha = int(255 * (1 - r / glow_radius) ** 2)
        pygame.draw.ellipse(eye_surf, (*color, alpha),
                            (cx - size[0] // 2 - r, cy - size[1] // 2 - r,
                             size[0] + 2 * r, size[1] + 2 * r))
    surface.blit(eye_surf, (center[0] - eye_surf.get_width() // 2,
                            center[1] - eye_surf.get_height() // 2))

def draw_polygon_eye(surface, center, points_fn, glow_radius, color):
    width, height = 180, 100
    eye_surf = pygame.Surface((width + glow_radius * 2, height + glow_radius * 2), pygame.SRCALPHA)
    cx, cy = eye_surf.get_width() // 2, eye_surf.get_height() // 2

    for r in range(glow_radius, 0, -1):
        alpha = int(255 * (1 - r / glow_radius) ** 2)
        points = points_fn(cx, cy, width, height, r)
        pygame.draw.polygon(eye_surf, (*color, alpha), points)

    surface.blit(eye_surf, (center[0] - eye_surf.get_width() // 2,
                            center[1] - eye_surf.get_height() // 2))

# --- Expression Shapes ---
def sad_shape(cx, cy, w, h, r):
    return [
        (cx - w // 2 - r, cy),
        (cx - w // 3, cy + h // 3 + r // 2),
        (cx, cy + h // 2 + r),
        (cx + w // 3, cy + h // 3 + r // 2),
        (cx + w // 2 + r, cy),
        (cx + w // 3, cy - h // 5 - r // 2),
        (cx - w // 3, cy - h // 5 - r // 2),
    ]

def angry_shape(cx, cy, w, h, r):
    return [
        (cx - w // 2 - r, cy + h // 4),
        (cx - w // 3, cy + h // 2 + r),
        (cx, cy + h // 3 + r),
        (cx + w // 3, cy + h // 2 + r),
        (cx + w // 2 + r, cy + h // 4),
        (cx + w // 3, cy - h // 3 - r),
        (cx - w // 3, cy - h // 5 - r),
    ]

def happy_shape(cx, cy, w, h, r):
    return [
        (cx - w // 2 - r, cy),
        (cx - w // 3, cy - h // 3 - r // 2),
        (cx, cy - h // 2 - r),
        (cx + w // 3, cy - h // 3 - r // 2),
        (cx + w // 2 + r, cy),
        (cx + w // 3, cy + h // 5 + r // 2),
        (cx - w // 3, cy + h // 5 + r // 2),
    ]

def draw_blinking_eye(surface, center):
    width, height = 180, 20
    draw_eye(surface, center, (width, height), GLOW_RADIUS, EYE_COLOR)

# --- Expression Renderer ---
def draw_expression(expr, blinking):
    if blinking:
        draw_blinking_eye(screen, LEFT_CENTER)
        draw_blinking_eye(screen, RIGHT_CENTER)
    elif expr == "sad":
        draw_polygon_eye(screen, LEFT_CENTER, sad_shape, GLOW_RADIUS, EYE_COLOR)
        draw_polygon_eye(screen, RIGHT_CENTER, sad_shape, GLOW_RADIUS, EYE_COLOR)
    elif expr == "angry":
        draw_polygon_eye(screen, LEFT_CENTER, angry_shape, GLOW_RADIUS, EYE_COLOR)
        draw_polygon_eye(screen, RIGHT_CENTER, angry_shape, GLOW_RADIUS, EYE_COLOR)
    elif expr == "happy":
        draw_polygon_eye(screen, LEFT_CENTER, happy_shape, GLOW_RADIUS, EYE_COLOR)
        draw_polygon_eye(screen, RIGHT_CENTER, happy_shape, GLOW_RADIUS, EYE_COLOR)
    else:
        draw_eye(screen, LEFT_CENTER, (180, 120), GLOW_RADIUS, EYE_COLOR)
        draw_eye(screen, RIGHT_CENTER, (180, 120), GLOW_RADIUS, EYE_COLOR)

# --- Main Loop ---
while True:
    now = time.time()
    screen.fill((0, 0, 0))

    # Handle expression timeout
    if expression != "neutral" and now - expression_time > 2:
        expression = "neutral"

    # Blink logic
    if not is_blinking and now > next_blink:
        is_blinking = True
        blink_start = now
        next_blink = now + random.uniform(3, 7)
    if is_blinking and now - blink_start > 0.2:
        is_blinking = False

    # Draw
    draw_expression(expression, is_blinking)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                expression = "sad"
                expression_time = now
            elif event.key == pygame.K_a:
                expression = "angry"
                expression_time = now
            elif event.key == pygame.K_h:
                expression = "happy"
                expression_time = now

    pygame.display.flip()
    clock.tick(30)
