import pygame
import random
import math
import config
from neural_network import NeuralNetwork


class Critter:

    def __init__(self, dna=None, x=None, y=None, energy=0.5, angle=None):
        if dna:
            self.dna = list(dna)
        else:
            self.dna = [random.uniform(-1, 1) for _ in range(config.DNA_LENGTH)]

        self.x = x if x is not None else random.randint(0, config.SCREEN_WIDTH)
        self.y = y if y is not None else random.randint(0, config.SCREEN_HEIGHT)
        self.energy = energy
        self.angle = angle if angle is not None else random.uniform(0, 2 * math.pi)
        self.speed = 0

        self._decode_dna()

        nn_weights = self.dna[config.DNA_NN_START_INDEX: config.DNA_NN_START_INDEX + config.NN_WEIGHTS_COUNT]
        self.brain = NeuralNetwork(nn_weights)

    def _decode_dna(self):
        self.radius = 4 + (self.dna[0] + 1) * 4
        self.max_speed = 1 + (self.dna[1] + 1) * 2
        self.metabolism = 0.0005 + ((self.dna[2] + 1) / 2) * 0.002

        r = int((self.dna[3] + 1) / 2 * 255)
        g = int((self.dna[4] + 1) / 2 * 255)
        b = int((self.dna[5] + 1) / 2 * 255)
        self.color = (max(0, min(255, r)), max(0, min(255, g)), max(0, min(255, b)))

    def find_closest_food(self, food_sources):
        if not food_sources:
            return None, float('inf')

        closest_food = min(
            food_sources,
            key=lambda food: (self.x - food.x) ** 2 + (self.y - food.y) ** 2
        )
        dist_sq = (self.x - closest_food.x) ** 2 + (self.y - closest_food.y) ** 2
        return closest_food, math.sqrt(dist_sq)

    def sense_think_act(self, food_sources):
        closest_food, dist = self.find_closest_food(food_sources)

        angle_to_food, normalized_dist = 0, 1.0
        if closest_food:
            dx = closest_food.x - self.x
            dy = closest_food.y - self.y
            food_angle = math.atan2(dy, dx)
            angle_to_food = (food_angle - self.angle + math.pi) % (2 * math.pi) - math.pi
            normalized_dist = min(1.0, dist / 200)

        inputs = [self.energy, angle_to_food / math.pi, normalized_dist]
        outputs = self.brain.process(inputs)

        self.angle += outputs[0] * 0.2
        self.speed = max(0, min(self.max_speed, self.speed + outputs[1] * 0.2))

    def update(self):
        self.x += math.cos(self.angle) * self.speed
        self.y += math.sin(self.angle) * self.speed

        self.x %= config.SCREEN_WIDTH
        self.y %= config.SCREEN_HEIGHT

        energy_cost = self.metabolism + (self.radius * 0.0001) + (self.speed * 0.0002)
        self.energy -= energy_cost

    def eat(self, food):
        self.energy = min(1.0, self.energy + food.energy)

    def reproduce(self):
        child_energy = self.energy * config.REPRODUCTION_ENERGY_COST
        self.energy -= child_energy

        child_dna = [
            max(-1, min(1, gene + random.uniform(-config.MUTATION_AMOUNT, config.MUTATION_AMOUNT)))
            if random.random() < config.MUTATION_RATE else gene
            for gene in self.dna
        ]

        spawn_angle = random.uniform(0, 2 * math.pi)
        spawn_dist = self.radius * 2 + 5
        child_x = self.x + math.cos(spawn_angle) * spawn_dist
        child_y = self.y + math.sin(spawn_angle) * spawn_dist

        return Critter(dna=child_dna, x=child_x, y=child_y, energy=child_energy)

    def draw(self, screen):
        pos = (int(self.x), int(self.y))

        pygame.draw.circle(screen, self.color, pos, int(self.radius))
        end_x = self.x + math.cos(self.angle) * self.radius
        end_y = self.y + math.sin(self.angle) * self.radius
        end_pos = (int(end_x), int(end_y))

        pygame.draw.line(screen, (255, 255, 255), pos, end_pos, 2)

    def to_dict(self):
        return {"dna": self.dna, "x": self.x, "y": self.y, "energy": self.energy, "angle": self.angle}

    @classmethod
    def from_dict(cls, data):
        return cls(
            dna=data.get("dna"),
            x=data.get("x"),
            y=data.get("y"),
            energy=data.get("energy"),
            angle=data.get("angle")
        )

