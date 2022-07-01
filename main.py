import pygame
import math
from random import randint, uniform

pygame.init()


WIDTH, HEIGHT = 800, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Collide Simulation.py")
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FPS = 60
RADIUS = 5
COUNT = 400


class Particle:
    def __init__(self, pos, speed, angle):
        self.x, self.y = pos
        self.radius = RADIUS
        self.color = BLACK
        self.speed = speed
        self.angle = angle

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)

    def move(self):
        self.x -= math.cos(self.angle) * self.speed
        self.y += math.sin(self.angle) * self.speed

    def bounce(self):
        if self.x > WIDTH - self.radius:
            self.x = 2 * (WIDTH - self.radius) - self.x
            self.angle = math.pi - self.angle
        elif self.x < self.radius:
            self.x = 2 * self.radius - self.x
            self.angle = math.pi - self.angle

        if self.y > HEIGHT - self.radius:
            self.y = 2 * (WIDTH - self.radius) - self.y
            self.angle *= -1
        elif self.y < self.radius:
            self.y = 2 * self.radius - self.y
            self.angle *= -1

    def collide(self, other):
        dx = self.x - other.x
        dy = self.y - other.y
        distance = math.hypot(dx, dy)
        if distance < self.radius + other.radius:
            tangent = math.atan2(dy, dx)
            angle = 0.5 * math.pi + tangent
            angle1 = 2 * tangent - self.angle
            angle2 = 2 * tangent - other.angle
            self.angle = angle1
            other.angle = angle2
            self.x -= math.cos(angle)
            self.y += math.sin(angle)
            other.x += math.cos(angle)
            other.y -= math.sin(angle)

            
class Environment:
    def __init__(self):
        self.width = WIDTH
        self.height = HEIGHT
        self.win = WIN
        self.clock = pygame.time.Clock()
        self.particles = []
        self.iterations = 500
        self.add_particles()


    def draw(self):
        self.win.fill(WHITE)
        for particle in self.particles:
            particle.draw(self.win)
        pygame.display.update()

    def add_particles(self):
        
        for _ in range(COUNT):
            particle = Particle(
                (randint(RADIUS, WIDTH - RADIUS), randint(RADIUS, HEIGHT - RADIUS)),
                randint(1,10),
                uniform(0, math.pi / 2),
            )
            self.particles.append(particle)

    def sort_particle(self):
        return sorted(self.particles, key=lambda particle: particle.x)

    def update(self):
        for i, particle in enumerate(self.particles):
            for particle2 in self.particles[i + 1 :]:
                if particle.x + particle.radius > particle2.x - particle2.radius:
                    particle.collide(particle2)
            particle.bounce()
            particle.move()
        self.draw()

    def run(self):
        while True:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
            self.update()
            self.draw()


if __name__ == "__main__":
    env = Environment()
    env.run()
