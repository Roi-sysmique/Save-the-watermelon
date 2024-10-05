import pygame
import math

pygame.init()

SCREEN_WIDTH = 700
SCREEN_HEIGHT = 600
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("pygame")
clock = pygame.time.Clock()
BACKGROUND = pygame.surface.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))


class WaterMellon(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.angle = 0
        self.original_image = pygame.image.load("Assets/Watermellon.png")
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


player = WaterMellon()

while True:
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    player.update(keys)
    SCREEN.blit(BACKGROUND, (0, 0))
    SCREEN.blit(player.image, player.rect)
    pygame.display.update()
    clock.tick(120)
