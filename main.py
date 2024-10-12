import pygame
import math
import random

pygame.init()
SCREEN_WIDTH = 857
SCREEN_HEIGHT = 490
FONT = pygame.font.Font("Font/Retro-gaming.ttf", 20)
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("pygame")
clock = pygame.time.Clock()
BACKGROUND = pygame.image.load("Assets/Background.png")
title = pygame.transform.rotozoom(pygame.image.load('Assets/title.png'), 0, 0.8)
title_rect = title.get_rect(bottomright=(SCREEN_WIDTH-10, SCREEN_HEIGHT-10))
title_y_position = 0
title_size = 0.2
game_over_screen = pygame.transform.rotozoom(pygame.image.load("Assets/game-over-screen.png"), 0, 0.5)
game_over_screen_rect = game_over_screen.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
game_over_screen_size = 0.2
restart_message = FONT.render('PRESS ENTER TO RESTART', True, 'black')
restart_message_rect = restart_message.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT - 80))
start_message = FONT.render('PRESS ENTER TO RESTART', True, 'black')
start_message_rect = start_message.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT - 100))
start_title = pygame.transform.rotozoom(pygame.image.load('Assets/title.png'), 0, math.sin(title_size))
start_title_rect = start_title.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
start_time = 0
score = 0
lives = 3
game_run = False
start_game = True
game_over = False


class WaterMellon(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.angle = 0
        self.original_image = pygame.image.load("Assets/Watermelon.png")
        self.image = pygame.transform.rotozoom(self.original_image, self.angle, 0.5)
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH/2, SCREEN_HEIGHT*2/3 + 10)
        self.turn_power = 0.5

    def update(self, keys):
        self.turn_power = (3 * (130 - (abs(self.angle)/90) * 100))/100
        if keys[pygame.K_LEFT] and self.angle < 90:
            self.angle += self.turn_power
        elif keys[pygame.K_RIGHT] and self.angle > -90:
            self.angle -= self.turn_power

        self.image = pygame.transform.rotozoom(self.original_image, self.angle, 0.5)
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH/2, SCREEN_HEIGHT*2/3 + 100)


class WatermelonSeed(pygame.sprite.Sprite):

    def __init__(self, pos_x, pos_y, angle):
        pygame.sprite.Sprite.__init__(self)
        self.angle = angle
        self.original_image = pygame.image.load('Assets/watermelon-seed.png')
        self.image = pygame.transform.rotozoom(self.original_image, self.angle, 0.5)
        self.rect = self.image.get_rect()
        self.x = pos_x
        self.y = pos_y
        self.rect.center = (self.x, self.y)
        self.velocity = 6
        self.theta = self.angle + 90
        self.x_velocity = - self.velocity * math.cos(math.radians(self.theta))
        self.y_velocity = self.velocity * math.sin(math.radians(self.theta))

    def update(self):
        self.image = pygame.transform.rotozoom(self.original_image, self.angle, 0.5)
        self.y -= self.y_velocity
        self.x -= self.x_velocity
        self.rect.center = (self.x, self.y)
        if self.rect.centery < -50 or self.rect.centerx < -50 or self.rect.centerx > SCREEN_WIDTH + 15:
            self.kill()


class Bee(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.images = ["Assets/bee-animation-1.png", "Assets/bee-animation-2.png",
                       "Assets/bee-animation-3.png", "Assets/bee-animation-4.png"]
        self.explosion_images = ["Assets/explosion-animation-1.png", "Assets/explosion-animation-2.png",
                                 "Assets/explosion-animation-3.png", "Assets/explosion-animation-4.png",
                                 "Assets/explosion-animation-5.png", "Assets/explosion-animation-6.png"]
        self.animation = 0
        self.image = pygame.transform.rotozoom(pygame.image.load(self.images[self.animation]), 0, 0.2)
        self.rect = self.image.get_rect()
        self.y = -50
        self.rect.center = (random.randint(0, 700) + 5*math.sin(5), self.y)
        self.collision = False
        self.random_x = random.randint(0, 700)
        self.x = 0

    def update(self, *args, **kwargs):
        global score, lives
        if pygame.sprite.spritecollideany(self, Projectiles):
            self.collision = True

        if self.collision or self.rect.bottom >= SCREEN_HEIGHT:
            self.animation += 0.1
            self.image = pygame.transform.rotozoom(pygame.image.load(self.explosion_images[round(self.animation)]), 0,
                                                   0.3)
            if self.animation >= len(self.explosion_images) - 1:
                if not self.rect.bottom >= SCREEN_HEIGHT:
                    score += 1
                else:
                    lives -= 1
                self.kill()
        else:
            self.y += 0.7
            self.animation += 0.2
            self.x += 0.1
            if self.animation >= len(self.images) - 1:
                self.animation = 0
            self.rect.center = (self.random_x + 10*math.sin(self.x), self.y)
            self.image = pygame.transform.rotozoom(pygame.image.load(self.images[round(self.animation)]), 0, 0.3)


player = WaterMellon()
Projectiles = pygame.sprite.Group()
Enemies = pygame.sprite.Group()
SCREEN.blit(title, title_rect)
SCORE_TXT = FONT.render(f"score: {score}", True, 'white')
SCORE_TXT_RECT = SCORE_TXT.get_rect(center=(player.rect.midleft[0] - 75, player.rect.midleft[1] + 75))
LIVES_TXT = FONT.render(f"Lives: {lives}", True, (166, 13, 2))
LIVES_TXT_RECT = LIVES_TXT.get_rect(centerx=SCORE_TXT_RECT.centerx, centery=SCORE_TXT_RECT.centery + 30)


def title_animation():
    global title_y_position
    title_y_position += 0.04
    title_rect.bottomright = (SCREEN_WIDTH-10, (SCREEN_HEIGHT-10) + 15*math.sin(title_y_position))
    if title_y_position >= 100*math.pi:
        title_y_position = 0


def wave_sys():
    global start_time
    break_time = int(pygame.time.get_ticks() / 100) - start_time
    if break_time == 12:
        start_time = int(pygame.time.get_ticks() / 100)
        bee = Bee()
        Enemies.add(bee)


def game_over_animation():
    global game_over_screen_size, game_over_screen, game_over_screen_rect
    game_over_screen_size += 0.02
    game_over_screen = pygame.transform.rotozoom(pygame.image.load("Assets/game-over-screen.png"), 0,
                                                 0.2*math.sin(game_over_screen_size) + 1)
    game_over_screen_rect = game_over_screen.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))


def start_title_animation():
    global title_size, start_title, start_title_rect
    title_size += 0.02
    start_title = pygame.transform.rotozoom(pygame.image.load('Assets/title.png'), 0, 0.5*math.sin(title_size) + 1.5)
    start_title_rect = start_title.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 50))


while True:
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN:
            if game_run:
                if event.key == pygame.K_SPACE:
                    projectile = WatermelonSeed(player.rect.center[0], player.rect.center[1], player.angle)
                    Projectiles.add(projectile)
            elif game_over:
                if event.key == pygame.K_RETURN:
                    score = 0
                    lives = 3
                    start_time = int(pygame.time.get_ticks() / 100)
                    game_over = False
                    Projectiles.empty()
                    Enemies.empty()
                    game_run = True
            elif start_game:
                if event.key == pygame.K_RETURN:
                    game_run = True
                    start_game = False
    if lives <= 0:
        game_over = True
        game_run = False
    if game_run:
        wave_sys()
        SCORE_TXT = FONT.render(f"score: {score}", True, 'white')
        LIVES_TXT = FONT.render(f"Lives: {lives}", True, (166, 13, 2))
        Projectiles.update()
        Enemies.update()
        player.update(keys)
        SCREEN.blit(BACKGROUND, (0, 0))
        Projectiles.draw(SCREEN)
        Enemies.draw(SCREEN)
        SCREEN.blit(player.image, player.rect)
        SCREEN.blit(SCORE_TXT, SCORE_TXT_RECT)
        SCREEN.blit(LIVES_TXT, LIVES_TXT_RECT)
        wave_sys()
    elif start_game:
        start_title_animation()
        SCREEN.blit(BACKGROUND, (0, 0))
        SCREEN.blit(start_title, start_title_rect)
        SCREEN.blit(start_message, start_message_rect)
    elif game_over:
        SCORE_TXT_GAME_OVER = pygame.transform.rotozoom(FONT.render(f"Score: {score}", False, 'white'), 0, 2)
        SCORE_TXT_GAME_OVER_RECT = SCORE_TXT_GAME_OVER.get_rect(midtop=(game_over_screen_rect.midbottom[0],
                                                                        game_over_screen_rect.midbottom[1]))
        game_over_animation()
        SCREEN.blit(BACKGROUND, (0, 0))
        SCREEN.blit(game_over_screen, game_over_screen_rect)
        SCREEN.blit(SCORE_TXT_GAME_OVER, SCORE_TXT_GAME_OVER_RECT)
        SCREEN.blit(restart_message, restart_message_rect)
    pygame.display.update()
    title_animation()
    clock.tick(210)
