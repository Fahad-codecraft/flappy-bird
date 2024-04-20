import pygame

class Button(pygame.sprite.Sprite):
    def __init__(self, image, position, callback):
        super().__init__()
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect(topleft=position)
        self.callback = callback
