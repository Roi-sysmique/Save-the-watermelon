import pygame
import math

pygame.init()

SCREEN_WIDTH = 700
SCREEN_HEIGHT = 600
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("pygame")
clock = pygame.time.Clock()
BACKGROUND = pygame.surface.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
BACKGROUND.fill('blue')
title = pygame.transform.rotozoom(pygame.image.load('Assets/title.png'), 0, 0.5)
title_rect = title.get_rect(bottomright=(SCREEN_WIDTH-10, SCREEN_HEIGHT-10))
title_y_position = 0


class WaterMellon(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.angle = 0
        self.original_image = pygame.image.load("Assets/Watermelon.png")
        self.image = pygame.transform.rotozoom(self.original_image, self.angle, 0.5)
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH/2, SCREEN_HEIGHT*2/3 + 10)

    def update(self, keys):
        if keys[pygame.K_LEFT] and self.angle < 60:
            self.angle += 2
        elif keys[pygame.K_RIGHT] and self.angle > -60:
            self.angle -= 2

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
        if self.rect.centery > 600 or self.rect.centerx > 700:
            self.kill()


player = WaterMellon()
Projectiles = pygame.sprite.Group()


def title_animation():
    global title_y_position
    title_y_position += 0.04
    title_rect.bottomright = (SCREEN_WIDTH-10, (SCREEN_HEIGHT-10) + 10*math.sin(title_y_position))


while True:
    Projectiles.update()
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                projectile = WatermelonSeed(player.rect.center[0], player.rect.center[1], player.angle)
                Projectiles.add(projectile)

    player.update(keys)
    SCREEN.blit(BACKGROUND, (0, 0))
    Projectiles.draw(SCREEN)
    SCREEN.blit(player.image, player.rect)
    SCREEN.blit(title, title_rect)
    pygame.display.update()
    title_animation()
    clock.tick(120)
