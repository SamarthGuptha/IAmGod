import random
from critter import Critter
from food import Food
import config


class Simulation:
    def __init__(self):
        self.critters = []
        self.food = []
        self.generation = 0

    def reset(self):
        self.critters = [Critter() for _ in range(config.INITIAL_CRITTERS)]
        self.food = [Food() for _ in range(config.INITIAL_FOOD)]
        self.generation = 0
        print("Simulation reset.")

    def add_food(self, count=50):
        for _ in range(count):
            if len(self.food) < config.MAX_FOOD:
                self.food.append(Food())

    def update(self):
        if len(self.food) < config.MAX_FOOD and random.random() < 0.5:
            for _ in range(config.FOOD_SPAWN_RATE):
                self.food.append(Food())

        new_critters = []
        for critter in self.critters:
            critter.sense_think_act(self.food)
            critter.update()

            remaining_food = []
            eaten = False
            for f in self.food:
                dist_sq = (critter.x - f.x) ** 2 + (critter.y - f.y) ** 2
                if not eaten and dist_sq < (critter.radius + config.FOOD_RADIUS) ** 2:
                    critter.eat(f)
                    eaten = True
                else:
                    remaining_food.append(f)
            self.food = remaining_food

            if critter.energy > config.REPRODUCTION_THRESHOLD:
                new_critters.append(critter.reproduce())
                self.generation += 1

        self.critters.extend(new_critters)
        self.critters = [c for c in self.critters if c.energy > 0]

    def draw(self, screen):
        for f in self.food:
            f.draw(screen)
        for critter in self.critters:
            critter.draw(screen)

