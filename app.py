import pygame
import random
import sys

# Inisialisasi pygame

pygame.init()

# Dimensi layar
SCREEN_WIDTH = 612
SCREEN_HEIGHT = 347

# Warna
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 100, 100)
GREEN = (100, 255, 100)

# Pengaturan permainan
FPS = 60
GRAVITY = 0.5
FLAP_STRENGTH = -10
PIPE_SPEED = -4
PIPE_VERTICAL_GAP = 180  # Celah vertikal antara pipa atas dan bawah
PIPE_HORIZONTAL_GAP = 250  # Jarak horizontal antar pipa
PIPE_WIDTH = 50

LEVELS = {
    "Easy": {"PIPE_SPEED": -3, "PIPE_VERTICAL_GAP": 200},
    "Medium": {"PIPE_SPEED": -4, "PIPE_VERTICAL_GAP": 180},
    "Hard": {"PIPE_SPEED": -5, "PIPE_VERTICAL_GAP": 150},
}

# Inisialisasi layar
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Load assets
background_image = pygame.image.load('assets/mountain_background.jpg')
bird_image = pygame.image.load('assets/bird_sprites.png')
pipe_top_image = pygame.image.load('assets/pipa atas.png')
pipe_bottom_image = pygame.image.load('assets/pipa bawah.png')

# sounds
flap_sound = pygame.mixer.Sound('assets/flap.wav')
collision_sound = pygame.mixer.Sound('assets/collision.wav')
score_sound = pygame.mixer.Sound('assets/score.wav')

# background music
pygame.mixer.music.load('assets/background_music.wav')  
pygame.mixer.music.set_volume(0.5)  # Mengatur volume (0.0 hingga 1.0)
pygame.mixer.music.play(-1, 0.0)  # Memutar musik secara loop (-1 untuk loop terus)


# Variabel permainan
bird_x = 50
bird_y = SCREEN_HEIGHT // 2
bird_velocity = 0

pipes = []
pipe_spawn_timer = 0

score = 0
font = pygame.font.SysFont(None, 48)
current_level = "Medium"

# Variabel untuk kesulitan dinamis
speed_increment_interval = 5 * FPS  # Tingkatkan setiap 5 detik
gravity_increment = 0.05
pipe_speed_increment = -0.1
timer = 0  # Inisialisasi pengatur waktu

def draw_text(text, x, y, color):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))

def spawn_pipe():
    top_height = random.randint(50, SCREEN_HEIGHT - PIPE_VERTICAL_GAP - 50)
    bottom_height = SCREEN_HEIGHT - top_height - PIPE_VERTICAL_GAP
    pipes.append({
        "x": SCREEN_WIDTH,
        "top_height": top_height,
        "bottom_height": bottom_height
    })

def draw_pipes():
    for pipe in pipes:
        screen.blit(pipe_top_image, (pipe["x"], pipe["top_height"] - pipe_top_image.get_height()))
        screen.blit(pipe_bottom_image, (pipe["x"], SCREEN_HEIGHT - pipe["bottom_height"]))

def move_pipes():
    global score
    for pipe in pipes[:]:
        pipe["x"] += PIPE_SPEED
        if pipe["x"] + PIPE_WIDTH < 0:
            pipes.remove(pipe)
            score += 1
            score_sound.play()

def check_collision():
    for pipe in pipes:
        if bird_x + 30 > pipe["x"] and bird_x < pipe["x"] + PIPE_WIDTH:
            if bird_y < pipe["top_height"] or bird_y + 21 > SCREEN_HEIGHT - pipe["bottom_height"]:
                collision_sound.play()
                return True
    if bird_y < 0 or bird_y + 21 > SCREEN_HEIGHT:
        collision_sound.play()
        return True
    return False

def reset_game():
    global bird_y, bird_velocity, pipes, score, pipe_spawn_timer, GRAVITY, PIPE_SPEED, timer
    bird_y = SCREEN_HEIGHT // 2
    bird_velocity = 0
    pipes = []
    score = 0
    pipe_spawn_timer = 0
    GRAVITY = 0.5
    PIPE_SPEED = LEVELS[current_level]["PIPE_SPEED"]
    timer = 0

def show_start_screen():
    global current_level, PIPE_SPEED, PIPE_VERTICAL_GAP

    screen.blit(background_image, (0, 0))
    draw_text("FLAPPY BIRD", SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 120, RED)
    draw_text("Pilih Level:", SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 60, BLACK)

    easy_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2, 200, 40)
    medium_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 50, 200, 40)
    hard_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 100, 200, 40)

    pygame.draw.rect(screen, GREEN, easy_rect)
    pygame.draw.rect(screen, (255, 255, 0), medium_rect)
    pygame.draw.rect(screen, RED, hard_rect)

    draw_text("Easy", easy_rect.x + 70, easy_rect.y + 5, BLACK)
    draw_text("Medium", medium_rect.x + 50, medium_rect.y + 5, BLACK)
    draw_text("Hard", hard_rect.x + 70, hard_rect.y + 5, BLACK)

    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if easy_rect.collidepoint(event.pos):
                    current_level = "Easy"
                elif medium_rect.collidepoint(event.pos):
                    current_level = "Medium"
                elif hard_rect.collidepoint(event.pos):
                    current_level = "Hard"
                else:
                    continue

                PIPE_SPEED = LEVELS[current_level]["PIPE_SPEED"]
                PIPE_VERTICAL_GAP = LEVELS[current_level]["PIPE_VERTICAL_GAP"]
                waiting = False

def show_game_over_screen():
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    overlay.set_alpha(200)
    overlay.fill((0, 0, 0))
    screen.blit(overlay, (0, 0))

    # Tentukan Medali Berdasarkan Skor
    if score < 20:
        medal_image = pygame.image.load('assets/medal_bronze.png')
    elif score < 40:
        medal_image = pygame.image.load('assets/medal_silver.png')
    else:
        medal_image = pygame.image.load('assets/medal_gold.png')

    # Ukuran gambar medali
    medal_width, medal_height = medal_image.get_size()
    medal_x = SCREEN_WIDTH // 2 - medal_width // 2
    medal_y = SCREEN_HEIGHT // 2 - 50  # Posisi medali sedikit di atas teks

    # Teks utama
    draw_text("GAME OVER", SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 150, RED)
    draw_text(f"Skor Anda: {score}", SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT // 2 - 100, WHITE)
    screen.blit(medal_image, (medal_x, medal_y))

    # Tombol Play Again dan Quit
    play_again_rect = pygame.Rect(SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT // 2 + 20, 240, 40)
    quit_rect = pygame.Rect(SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT // 2 + 80, 240, 40)

    pygame.draw.rect(screen, GREEN, play_again_rect)
    pygame.draw.rect(screen, RED, quit_rect)

    draw_text("Play Again", play_again_rect.x + 50, play_again_rect.y + 5, BLACK)
    draw_text("Quit", quit_rect.x + 85, quit_rect.y + 5, BLACK)

    pygame.display.flip()

    # Tunggu input pengguna
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_again_rect.collidepoint(event.pos):
                    reset_game()
                    waiting = False
                elif quit_rect.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

# Tampilkan layar mulai
show_start_screen()

# Main game loop
clock = pygame.time.Clock()
running = True
while running:
    screen.blit(background_image, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            bird_velocity = FLAP_STRENGTH
            flap_sound.play()

    bird_velocity += GRAVITY
    bird_y += bird_velocity

    pipe_spawn_timer += 1
    timer += 1

    # Tingkatkan kesulitan berdasarkan waktu atau skor
    if timer % speed_increment_interval == 0:
        GRAVITY += gravity_increment  # Meningkatkan kecepatan jatuhnya burung
        PIPE_SPEED += pipe_speed_increment  # Membuat pipa bergerak lebih cepat

    if len(pipes) == 0 or pipes[-1]["x"] < SCREEN_WIDTH - PIPE_HORIZONTAL_GAP:
        spawn_pipe()

    move_pipes()
    draw_pipes()

    screen.blit(bird_image, (bird_x, bird_y))

    if check_collision():
        show_game_over_screen()

    draw_text(str(score), SCREEN_WIDTH // 2 - 20, 20, BLACK)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
