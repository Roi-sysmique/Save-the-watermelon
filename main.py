import pygame
import math
import random

pygame.init()
SCREEN_WIDTH = 857
SCREEN_HEIGHT = 517
FONT = pygame.font.Font("Font/Retro-gaming.ttf", 20)
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("pygame")
clock = pygame.time.Clock()
BACKGROUND = pygame.image.load("Assets/Background.png")
title = pygame.transform.rotozoom(pygame.image.load('Assets/title.png'), 0, 0.5)
title_rect = title.get_rect(bottomright=(SCREEN_WIDTH-10, SCREEN_HEIGHT-10))
title_y_position = 0
start_time = 0
score = 0


class WaterMellon(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.angle = 0
        self.original_image = pygame.image.load("Assets/Watermelon.png")
        self.image = pygame.transform.rotozoom(self.original_image, self.angle, 0.5)
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH/2, SCREEN_HEIGHT*2/3 + 10)
        self.turn_power = 3

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
        global score
        if pygame.sprite.spritecollideany(self, Projectiles):
            self.collision = True

        if self.collision or self.rect.bottom >= SCREEN_HEIGHT:
            self.animation += 0.1
            self.image = pygame.transform.rotozoom(pygame.image.load(self.explosion_images[round(self.animation)]), 0,
                                                   0.3)
            if self.animation >= len(self.explosion_images) - 1:
                if not self.rect.bottom >= SCREEN_HEIGHT:
                    score += 1
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
SCORE_TXT = FONT.render(f"score: {score}", False, 'black')
SCORE_TXT_RECT = SCORE_TXT.get_rect(center=(player.rect.midleft[0] - 75, player.rect.midleft[1] + 100))


def title_animation():
    global title_y_position
    title_y_position += 0.04
    title_rect.bottomright = (SCREEN_WIDTH-10, (SCREEN_HEIGHT-10) + 10*math.sin(title_y_position))
    if title_y_position >= 100*math.pi:
        title_y_position = 0


def wave_sys():
    global start_time
    break_time = int(pygame.time.get_ticks() / 100) - start_time
    if break_time == 12:
        start_time = int(pygame.time.get_ticks() / 100)
        bee = Bee()
        Enemies.add(bee)


while True:
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                projectile = WatermelonSeed(player.rect.center[0], player.rect.center[1], player.angle)
                Projectiles.add(projectile)

    wave_sys()
    Projectiles.update()
    Enemies.update()
    player.update(keys)
    SCREEN.blit(BACKGROUND, (0, 0))
    Projectiles.draw(SCREEN)
    Enemies.draw(SCREEN)
    SCREEN.blit(player.image, player.rect)
    SCREEN.blit(title, title_rect)
    SCORE_TXT = FONT.render(f"score: {score}", False, 'black')
    SCREEN.blit(SCORE_TXT, SCORE_TXT_RECT)
    pygame.display.update()
    title_animation()
    clock.tick(240)
