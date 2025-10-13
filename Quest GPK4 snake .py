import pygame
import sys
import time
import random

# Constantes
FRAME_SIZE_X = 720
FRAME_SIZE_Y = 480
CELL_SIZE = 10

MIN_FPS = 10
MAX_FPS = 60

BLACK = pygame.Color(0, 0, 0)
WHITE = pygame.Color(255, 255, 255)
RED = pygame.Color(255, 0, 0)
GREEN = pygame.Color(0, 255, 0)
BLUE = pygame.Color(0, 0, 255)
YELLOW = pygame.Color(255, 255, 0)

pygame.init()
pygame.display.set_caption('Snake Eater')
game_window = pygame.display.set_mode((FRAME_SIZE_X, FRAME_SIZE_Y))
fps_controller = pygame.time.Clock()

snake_pos = [100, 50]
snake_body = [[100, 50], [90, 50], [80, 50]]

food_pos = [random.randrange(0, FRAME_SIZE_X // CELL_SIZE) * CELL_SIZE,
            random.randrange(0, FRAME_SIZE_Y // CELL_SIZE) * CELL_SIZE]

direction = 'RIGHT'
change_to = direction

score = 0

# Variables para habilidades
ability_active = False
ability_name = None
ability_end_time = 0

# Para multiplicador de puntos
score_multiplier = 1

# Para invencibilidad
invincible = False

def show_score(choice=1, color=WHITE, font='consolas', size=20):
    score_font = pygame.font.SysFont(font, size)
    score_surface = score_font.render(f'Score : {score}', True, color)
    score_rect = score_surface.get_rect()
    if choice == 1:
        score_rect.topleft = (10, 10)
    else:
        score_rect.midtop = (FRAME_SIZE_X // 2, FRAME_SIZE_Y // 1.25)
    game_window.blit(score_surface, score_rect)

def show_ability():
    if ability_active and ability_name:
        font = pygame.font.SysFont('consolas', 20)
        ability_surface = font.render(f'Habilidad: {ability_name}', True, YELLOW)
        ability_rect = ability_surface.get_rect()
        ability_rect.topright = (FRAME_SIZE_X - 10, 10)
        game_window.blit(ability_surface, ability_rect)

def game_over():
    my_font = pygame.font.SysFont('times new roman', 90)
    game_over_surface = my_font.render('YOU DIED', True, RED)
    game_over_rect = game_over_surface.get_rect()
    game_over_rect.midtop = (FRAME_SIZE_X // 2, FRAME_SIZE_Y // 4)
    game_window.fill(BLACK)
    game_window.blit(game_over_surface, game_over_rect)
    show_score(0, RED, 'times', 20)
    pygame.display.flip()
    time.sleep(3)
    pygame.quit()
    sys.exit()

def spawn_food():
    while True:
        new_food_pos = [random.randrange(0, FRAME_SIZE_X // CELL_SIZE) * CELL_SIZE,
                        random.randrange(0, FRAME_SIZE_Y // CELL_SIZE) * CELL_SIZE]
        if new_food_pos not in snake_body:
            return new_food_pos

def handle_keys():
    global change_to
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_UP, ord('w')):
                change_to = 'UP'
            elif event.key in (pygame.K_DOWN, ord('s')):
                change_to = 'DOWN'
            elif event.key in (pygame.K_LEFT, ord('a')):
                change_to = 'LEFT'
            elif event.key in (pygame.K_RIGHT, ord('d')):
                change_to = 'RIGHT'
            elif event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

def update_direction():
    global direction, change_to
    opposite_directions = {'UP': 'DOWN', 'DOWN': 'UP', 'LEFT': 'RIGHT', 'RIGHT': 'LEFT'}
    if change_to != opposite_directions.get(direction):
        direction = change_to

def move_snake():
    if direction == 'UP':
        snake_pos[1] -= CELL_SIZE
    elif direction == 'DOWN':
        snake_pos[1] += CELL_SIZE
    elif direction == 'LEFT':
        snake_pos[0] -= CELL_SIZE
    elif direction == 'RIGHT':
        snake_pos[0] += CELL_SIZE

def check_collisions():
    # Colisión con bordes solo si NO está invencible
    if not invincible:
        if (snake_pos[0] < 0 or snake_pos[0] >= FRAME_SIZE_X or
            snake_pos[1] < 0 or snake_pos[1] >= FRAME_SIZE_Y):
            game_over()

    # Colisión con cuerpo solo si NO está invencible
    if not invincible and snake_pos in snake_body[1:]:
        game_over()

def draw_elements():
    game_window.fill(BLACK)
    # Dibujar serpiente
    for pos in snake_body:
        pygame.draw.rect(game_window, GREEN, pygame.Rect(pos[0], pos[1], CELL_SIZE, CELL_SIZE))

    # Dibujar comida
    pygame.draw.rect(game_window, WHITE, pygame.Rect(food_pos[0], food_pos[1], CELL_SIZE, CELL_SIZE))

    show_score()
    show_ability()

    pygame.display.update()

def get_current_difficulty(score):
    return min(MIN_FPS + (score // 5) * 5, MAX_FPS)

def activate_ability():
    global ability_active, ability_name, ability_end_time
    global score_multiplier, invincible

    abilities = ['Velocidad', 'Invencible', 'Multiplicador']

    ability_active = True
    ability_name = random.choice(abilities)
    ability_end_time = time.time() + 5  # dura 5 segundos

    # Resetear efectos antes de activar
    score_multiplier = 1
    invincible = False

    if ability_name == 'Velocidad':
        print("Habilidad activada: Velocidad aumentada")
    elif ability_name == 'Invencible':
        invincible = True
        print("Habilidad activada: Invencibilidad temporal")
    elif ability_name == 'Multiplicador':
        score_multiplier = 2
        print("Habilidad activada: Multiplicador de puntos")

def update_ability():
    global ability_active, ability_name, score_multiplier, invincible

    if ability_active:
        if time.time() > ability_end_time:
            # Termina la habilidad
            ability_active = False
            ability_name = None
            score_multiplier = 1
            invincible = False
            print("Habilidad terminada")

# Variable para controlar activaciones para que no se repita varias veces al mismo puntaje
last_ability_score = 0

# Bucle principal
while True:
    handle_keys()
    update_direction()
    move_snake()

    snake_body.insert(0, list(snake_pos))

    # Comer comida
    if snake_pos == food_pos:
        score += score_multiplier  # multiplica puntos si habilidad activa
        food_pos = spawn_food()
        
        # Activar habilidad cada 3 puntos alcanzados (evita repetición con last_ability_score)
        if score // 3 > last_ability_score // 3:
            activate_ability()
            last_ability_score = score
    else:
        snake_body.pop()

    check_collisions()
    update_ability()
    draw_elements()

    current_difficulty = get_current_difficulty(score)
    # Si habilidad velocidad activa, aumentamos fps temporalmente
    if ability_active and ability_name == 'Velocidad':
        fps_controller.tick(min(current_difficulty + 20, MAX_FPS + 20))  # velocidad extra
    else:
        fps_controller.tick(current_difficulty)
