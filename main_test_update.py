import pygame
import sys
import random
import os


pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Skyfall')
clock = pygame.time.Clock()

# Dynamically build base project folder path
project_folder = os.path.dirname(__file__)

# Font loading
font_path = os.path.join(project_folder, 'font', 'Pixelon.ttf')
font = pygame.font.Font(font_path, 100)
small_font = pygame.font.Font(None, 36)


# Game states
game_state = 'menu'


# Colors
SKY_COLOR = '#cef1f9'
OVERLAY_COLOR = '#80e8ff'
BRICK_RED = (178, 34, 34)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)


# Assets
text_surf = font.render('Skyfall', False, ('#c55b56'))
text_rect = text_surf.get_rect(center=(400, 150))

graphics_folder = os.path.join(project_folder, 'graphics')
block_image_path = os.path.join(graphics_folder, 'enemy_block.png')  # Replace 'block.png' with your file name
block_surf = pygame.image.load(block_image_path).convert_alpha()
block_surf = pygame.transform.scale(block_surf, (100, 100))


cloud_image_path = os.path.join(graphics_folder, 'cloud1.png')
play_button_path = os.path.join(graphics_folder, 'playbutton.png')
shop_button_path = os.path.join(graphics_folder, 'shopbutton.png')
highscore_panel_path = os.path.join(graphics_folder, 'highscorepanel.png')

cloud_surf = pygame.image.load(cloud_image_path).convert_alpha()
cloud_surf = pygame.transform.scale(cloud_surf, (155, 93))
cloud_rect = cloud_surf.get_rect(center=(260, 160))
cloud_rect_2 = cloud_surf.get_rect(center=(550, 120))

cloud_surf_2 = pygame.transform.scale(cloud_surf, (126, 76))
cloud_rect_3 = cloud_surf_2.get_rect(topleft=(120, 448))
cloud_rect_4 = cloud_surf_2.get_rect(topleft=(545, 480))

overlay_shape = pygame.surface.Surface((774, 568))
overlay_rect = overlay_shape.get_rect(center=(400, 300))

play_btn = pygame.image.load(play_button_path).convert_alpha()
play_btn_rect = play_btn.get_rect(topleft=(185, 260))

shop_btn = pygame.image.load(shop_button_path).convert_alpha()
shop_btn_rect = shop_btn.get_rect(topleft=(438, 260))

highscore_panel = pygame.image.load(highscore_panel_path).convert_alpha()
highscore_panel_rect = highscore_panel.get_rect(topleft=(193, 358))


# Gameplay variables
player = pygame.Rect(400 - 25, 520, 50, 50)
player_speed = 7
blocks = []
block_speed = 10
abilities = []
ability_speed = 4
spawn_timer = 0
invincible = False
break_blocks = False
invincible_timer = 0
break_timer = 0
INVINCIBLE_DURATION = 300
BREAK_DURATION = 180
score = 0


def reset_game():
    global player, blocks, abilities, invincible, break_blocks, invincible_timer, break_timer, spawn_timer, score
    player = pygame.Rect(400 - 25, 520, 50, 50)
    blocks = []
    abilities = []
    invincible = False
    break_blocks = False
    invincible_timer = 0
    break_timer = 0
    spawn_timer = 0
    score = 0


def spawn_block():
    x = random.randint(0, 740)
    blocks.append(pygame.Rect(x, -30, 60, 30))


def spawn_ability():
    x = random.randint(0, 770)
    ability_type = random.choice(["invincible", "break"])
    abilities.append({"rect": pygame.Rect(x, -30, 30, 30), "type": ability_type})

def update_block_speed(score):
    # Increase block speed every 100 points, capped to a max speed, e.g., 25
    base_speed = 10
    max_speed = 25
    increment = score // 500
    return min(base_speed + increment, max_speed)


# ========================= MAIN LOOP ==============================
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()


    # ========================= MENU SCREEN =========================
    if game_state == 'menu':
        screen.fill(SKY_COLOR)
        pygame.draw.rect(screen, OVERLAY_COLOR, overlay_rect, 500, border_radius=15)
        screen.blit(cloud_surf, cloud_rect)
        screen.blit(cloud_surf, cloud_rect_2)
        screen.blit(text_surf, text_rect)
        screen.blit(play_btn, play_btn_rect)
        screen.blit(shop_btn, shop_btn_rect)
        screen.blit(highscore_panel, highscore_panel_rect)
        screen.blit(cloud_surf_2, cloud_rect_3)
        screen.blit(cloud_surf_2, cloud_rect_4)


        # Button clicks
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if play_btn_rect.collidepoint(event.pos):
                reset_game()
                game_state = 'playing'
            elif shop_btn_rect.collidepoint(event.pos):
                game_state = 'shop'


    # ========================= GAMEPLAY ============================
    elif game_state == 'playing':
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.left > 0:
            player.x -= player_speed
        if keys[pygame.K_RIGHT] and player.right < 800:
            player.x += player_speed


        spawn_timer += 1
        score += 1  # score increases as time passes
        block_speed = update_block_speed(score)


        if spawn_timer % 40 == 0:
            spawn_block()
        if spawn_timer % 250 == 0:
            spawn_ability()


        # Timers
        if invincible:
            invincible_timer -= 1
            if invincible_timer <= 0:
                invincible = False
        if break_blocks:
            break_timer -= 1
            if break_timer <= 0:
                break_blocks = False

        # Move blocks
        for block in blocks[:]:
            block.y += block_speed
            if block.top > 600:
                blocks.remove(block)
            elif block.colliderect(player):
                if break_blocks:
                    blocks.remove(block)
                elif not invincible:
                    game_state = 'menu'


        # Move abilities
        for ability in abilities[:]:
            ability["rect"].y += ability_speed
            if ability["rect"].top > 600:
                abilities.remove(ability)
            elif ability["rect"].colliderect(player):
                if ability["type"] == "invincible":
                    invincible = True
                    invincible_timer = INVINCIBLE_DURATION
                elif ability["type"] == "break":
                    break_blocks = True
                    break_timer = BREAK_DURATION
                abilities.remove(ability)


        # Draw everything
        screen.fill(SKY_COLOR)
        pygame.draw.rect(screen, OVERLAY_COLOR, overlay_rect, 500, border_radius=15)


        pygame.draw.rect(screen, BLUE, player, border_radius=8)
        for block in blocks:
            screen.blit(block_surf, block.topleft)

        for ability in abilities:
            color = YELLOW if ability["type"] == "invincible" else GREEN
            pygame.draw.circle(screen, color, ability["rect"].center, 15)


        if invincible:
            pygame.draw.circle(screen, YELLOW, player.center, 30, 3)
        if break_blocks:
            pygame.draw.circle(screen, GREEN, player.center, 30, 3)


        # Score display
        score_text = small_font.render(f"Score: {score}", True, (0, 0, 0))
        screen.blit(score_text, (20, 20))


    # ========================= SHOP SCREEN =========================
    elif game_state == 'shop':
        screen.fill("#a0ff6b")
        back_text = small_font.render("Press ESC to return", True, (0, 0, 0))
        screen.blit(back_text, (280, 280))
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            game_state = 'menu'


    pygame.display.update()
    clock.tick(60)
