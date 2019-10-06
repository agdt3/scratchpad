import sys, pygame, math

from pygame import (
    gfxdraw,
    mask,
    Surface,
    sprite,
    Vector2,
    Color,
)


def load_image(path):
    return pygame.image.load(path).convert_alpha()


def projection(vec1, vec2, theta=None):
    #vec1 and vec2 are pygame Vector2 structs
    if vec2.is_normalized():
        vec2_normal = vec2
    else:
        vec2_normal = vec2.normalize()

    if theta is None:
        scalar_projection = vec1.dot(vec2_normal)
    else:
        scalar_projection = vec1.length() * math.cos(math.radians(theta))

    vector_projection = Vector2(
        scalar_projection * vec2_normal.x,
        scalar_projection * vec2_normal.y
    )

    return vector_projection


class Particles(pygame.sprite.Group):
    def __init__(self, particle_params=[]):
        pygame.sprite.Group.__init__(self)
        self.defaults = {
            'position': (0, 0),
            'velocity': Vector2(1, 1),
            'mass': 1,
            'radius': 10,
            'color': Color(255, 255, 255),
        }
        self.generate_particles(particle_params)

    def generate_particles(self, particle_params):
        for params in particle_params:
            new_params = self.defaults.copy()
            new_params.update(params)
            self.add(Particle(**new_params))


class Particle(pygame.sprite.Sprite):
    def __init__(self, velocity, position, area, mass, radius, color, image=None, id=None):
        pygame.sprite.Sprite.__init__(self)
        if image:
            self.image = load_image(image)
            self.rect = self.image.get_rect()
        else:
            self.radius = radius
            side = self.radius * 2
            self.image = Surface((side, side))
            self.rect = self.image.get_rect()
            self.color = color
            self.generate_image()

        self.mask = pygame.mask.from_surface(self.image)

        self.rect.move_ip(position)
        self.center = self.mask.centroid()

        self.old_rect = self.image.get_rect()
        self.velocity = velocity
        self.area = area
        self.mass = mass
        self.id = id
        self.collisions = []

    def generate_image(self):
        self.image.set_colorkey((0,0,0))
        x = int(self.rect.width / 2)
        y = int(self.rect.height / 2)
        gfxdraw.filled_circle(self.image, x, y, self.radius - 1, self.color)
        gfxdraw.aacircle(self.image, x, y, self.radius - 1, self.color)

    def update(self):
        self.old_rect = self.rect.copy()
        dx, dy = self.calculatepos()
        self.rect.move_ip(dx, dy)

        if self.rect.left < 0:
            self.rect.left = 0
            self.velocity.x = -self.velocity.x
        elif self.rect.right > self.area[0]:
            self.rect.right = self.area[0]
            self.velocity.x = -self.velocity.x

        if self.rect.top < 0:
            self.rect.top = 0
            self.velocity.y = -self.velocity.y
        elif self.rect.bottom > self.area[1]:
            self.rect.bottom = self.area[1]
            self.velocity.y = -self.velocity.y

    def get_components(self, collision_point):
        # Distance vector between particle center and point of impact
        print(f"center {self.center} collision {collision_point}")
        d = Vector2(
            collision_point[0] - self.center[0],
            collision_point[1] - self.center[1]
        )
        # Decomposition of velocity into n and tangential vectors
        n = projection(self.velocity, d)
        tangent = self.velocity - n
        print(f"velo: {self.velocity} d: {d} n: {n} tangent: {tangent}")
        return n, tangent

    def calculatepos(self):
        print(f"pre-collision {self.id} velocity: {self.velocity}")
        for collision in self.collisions:
            m1 = self.mass
            m2 = collision[1]

            u1x = collision[2].x
            u1y = collision[2].y
            u2x = collision[3].x
            u2y = collision[3].y

            p1 = (m1 - m2) / (m1 + m2)
            p2 = 2 * m2 / (m1 + m2)

            v1x = math.floor(p1 * u1x + p2 * u2x)
            v1y = math.floor(p1 * u1y + p2 * u2y)
            print(f"{v1x} {v1y}")

            tangent = collision[4]
            v1fx = v1x + tangent.x
            v1fy = v1y + tangent.y
            self.velocity = Vector2(v1fx, v1fy)
            #self.velocity.update(v1x, v1y)
            print(f"post-collision {self.id} velocity: {self.velocity}")

        self.collisions = []

        dx, dy = self.velocity
        return (dx, dy)

    def add_collision(self, velocity, mass, n1, n2, tangent):
       self.collisions.append((velocity, mass, n1, n2, tangent))
