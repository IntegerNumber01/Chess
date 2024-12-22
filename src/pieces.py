import pygame
import os
from exe_image_loader import resource_path


class Pieces:
    def __init__(self, screen, size):
        self.images = self.load_images()
        self.resize_images(size)
        self.screen = screen

    def load_images(self):
        names = ['K', 'Q', 'R', 'N', 'B', 'P', 'k', 'q', 'r', 'n', 'b', 'p']
        files = ['WK', 'WQ', 'WR', 'WN', 'WB', 'WP',
                 'Bk', 'Bq', 'Br', 'Bn', 'Bb', 'Bp']
        images = {}

        for i in range(len(names)):
            # Use when creating exe file
            image_path = resource_path(os.path.join('Piece Images', files[i] + '.png'))
            images[names[i]] = pygame.image.load(image_path)

            # Windows:
            # images[names[i]] = pygame.image.load('C:/Users/arjun/OneDrive - Hindupedia/Documents/Chess/Piece Images/' + files[i] + '.png')
            # Linux
            # images[names[i]] = pygame.image.load('/home/arjun/OneDrive/Documents/Chess/Piece Images/' + files[i] + '.png')

        return images

    def resize_images(self, size):
        for key, value in self.images.items():
            new_width = int(value.get_width() * size)
            new_height = int(value.get_height() * size)

            self.images[key] = pygame.transform.smoothscale(value, (new_width,
                                                                    new_height)
                                                            )

    def render(self, piece, coordinates, transparency):
        sprite = self.images[piece]

        if transparency is not None:
            copy = sprite.copy()
            copy.set_alpha(transparency)
            self.screen.blit(copy, sprite.get_rect(center=coordinates))
        else:
            self.screen.blit(sprite, sprite.get_rect(center=coordinates))
