import random
import pygame
from pygame_func import load_image


class Particle(pygame.sprite.Sprite):

    def __init__(self, pos, dx, dy, all_sprites, width, height):
        fire = [load_image("star.png")]
        for scale in (5, 10, 20):
            fire.append(pygame.transform.scale(fire[0], (scale, scale)))
        super().__init__(all_sprites)
        self.image = random.choice(fire)
        self.rect = self.image.get_rect()

        self.screen_rect = (0, 0, width, height)

        self.velocity = [dx, dy]
        self.rect.x, self.rect.y = pos

        self.gravity = 0.1

    def update(self):
        self.velocity[1] += self.gravity
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        if not self.rect.colliderect(self.screen_rect):
            self.kill()


def create_particles(position, all_sprites, width, height):
    particle_count = 30
    numbers = range(-5, 6)
    for _ in range(particle_count):
        Particle(position, random.choice(numbers), random.choice(numbers),
                 all_sprites, width, height)
