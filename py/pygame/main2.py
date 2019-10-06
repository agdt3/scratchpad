import sys, pygame, math
from particle import (
    Particle,
    Particles
)


pygame.init()
pygame.font.init()


class World:
    def __init__(self, size=None, debug=False):
        self.debug = debug
        self.width = 640
        self.height = 480
        self.size = size if size is not None else (self.width, self.height)
        flags = pygame.DOUBLEBUF | pygame.FULLSCREEN
        #flags = pygame.DOUBLEBUF
        self.screen = pygame.display.set_mode(self.size, flags)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('Arial', 32)

        self.particles = Particles([
            {
                'velocity': pygame.Vector2(0, 5),
                'position': (50, 100),
                'area': (self.width, self.height),
                'radius': 10,
                'mass': 1,
                'color': pygame.Color(255, 0, 0),
                'id': 1
            },
            {
                'velocity': pygame.Vector2(2, 5),
                'position': (100, 100),
                'area': (self.width, self.height),
                'radius': 100,
                'mass': 10,
                'id': 2
            },
            {
                'velocity': pygame.Vector2(-5, 5),
                'position': (self.width - 100, 100),
                'area': (self.width, self.height),
                'radius': 50,
                'mass': 5,
                'color': pygame.Color(0, 0, 255),
                'id': 3
            },
        ])

        self.background = pygame.Surface((self.width, self.height))
        self.background.fill((0,0,0))

        self.loop()

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

    def check_collisions(self):
        print("check collisions")
        for sprite in self.particles.sprites():
            for sprite2 in self.particles.sprites():
                if sprite2 is sprite:
                    continue

                if pygame.sprite.collide_circle(sprite, sprite2):
                    # Collision point is relative to item rect
                    collision_point = pygame.sprite.collide_mask(sprite, sprite2)
                    if collision_point is not None:
                        print(f"sprite {sprite.id} collided with sprite {sprite2.id} at {collision_point}")
                        n1, tangent1 = sprite.get_components(collision_point)
                        n2, tangent2 = sprite2.get_components(collision_point)
                        sprite.add_collision(sprite2.velocity, sprite2.mass, n1, n2, tangent1)

    def update(self):
        self.particles.update()

    def draw(self):
        to_erase = []

        if self.debug:
            #pygame.display.set_caption("FPS: " + str(self.clock.get_fps()))
            text = self.font.render("FPS: " + str(self.clock.get_fps()), False, (255, 255, 255))
            text_rect = text.get_rect()
            to_erase.append((self.background, text_rect, text_rect))

        for sprite in self.particles.sprites():
            to_erase.append((self.background, sprite.old_rect, sprite.old_rect))

        self.screen.blits(to_erase)
        self.particles.draw(self.screen)

        if self.debug:
            self.screen.blit(text, text_rect)

        pygame.display.flip()

    def loop(self):
        while 1:
            #self.clock.tick(60)
            self.clock.tick_busy_loop(60)
            self.check_events()
            self.check_collisions()
            self.update()
            self.draw()

world = World(debug=True)
