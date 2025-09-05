import pygame
import random
import config

class Food:
    def __init__(self, x=None, y=None):
        self.x = x if x is not None else random.randint(0, config.SCREEN_WIDTH)
        self.y = y if y is not None else random.randint(0, config.SCREEN_HEIGHT)
        self.energy = config.FOOD_ENERGY

    def draw(self, screen):
        pygame.draw.circle(screen, config.FOOD_COLOR, (self.x, self.y), config.FOOD_RADIUS)
    def to_dict(self):
        return {"x": self.x, "y": self.y}

    @classmethod
    def from_dict(cls, data):
        return cls(x=data["x"], y=data["y"])
