import pygame
import soragl as SORA
from soragl import physics, base_objects

import numpy as np


# ------------------------------- #
# pointspring
class PointSpring:
    def __init__(self, origin, k, damping, tension):
        self.origin = pygame.math.Vector2(origin)
        self.position = pygame.math.Vector2(origin)
        self.velocity = pygame.math.Vector2(0, 0)
        self.k = k
        self.damping = damping
        self.tension = tension

    def update(self):
        """Update the point spring."""
        dh = self.position - self.origin
        self.velocity += self.tension * dh - self.velocity * self.damping
        self.position += self.velocity


# ------------------------------- #
# water

DEFAULT_CONFIG = {
    "color": (0, 0, 255, 159),
    "resolution": 10,
    "k": 1.0,
    "damping": 0.05,
    "tension": 0.01,
    "height": 0.8,
    "spread": 0.1,
}


class Water(physics.Entity):
    def __init__(self, width: int, height: int, config: dict = None):
        """Initialize the water object."""
        super().__init__()
        self.area = (width, height)
        self.config = config if config else DEFAULT_CONFIG.copy()
        self.surface = pygame.Surface(self.area)

        self.spread = self.config["spread"]
        self.kc = self.config["k"]
        self.damping = self.config["damping"]
        self.tension = self.config["tension"]
        self.w_height = 1 - self.config["height"]
        # points / 100px
        self.resolution = self.config["resolution"]
        # self.points = numpy.zeros(int(width / self.config["resolution"]))
        wp = int(self.resolution * self.area[0] / 100)
        self.points = [
            PointSpring((x, 0), self.kc, self.damping, self.tension)
            for x in range(0, width + wp, wp)
        ]

        # components
        self.c_sprite = base_objects.Sprite(width, height)
        self.sprite = self.c_sprite.sprite
        self.c_collision = base_objects.Collision2DComponent()

    def on_ready(self):
        """Called when the object is ready."""
        self.add_component(self.c_sprite)
        self.add_component(base_objects.SpriteRenderer())
        # add collision body
        self.add_component(self.c_collision)

    def add_volume(self, volume):
        """Add volume to the water."""
        self.w_height += volume / self.area[0]

    def remove_volume(self, volume):
        """Remove volume from the water."""
        self.add_volume(-volume)

    def spread_wave(self, x, y):
        """Spread a wave from a point."""
        # changes for first and last point
        self.points[0].velocity.y += self.spread * (y - self.points[0].position.y)
        self.points[-1].velocity.y += self.spread * (y - self.points[-1].position.y)

        # changes for other points
        for i in range(1, len(self.points) - 2):
            self.points[i].velocity.y += self.spread * (y - self.points[i].position.y)
            self.points[i].velocity.y += self.spread * (
                self.points[i].height - self.points[i + 1].height
            )

    def splash(self, location, velocity):
        """Splash the water."""
        if 0 <= location < len(self.points):
            self.points[location].velocity.y += velocity

    # === update

    def update(self):
        self.sprite.fill((0, 0, 0, 0))
        # self.sprite.fill(self.config["color"])
        # draw each point
        h = self.area[1] * self.w_height
        for point in self.points:
            point.update()
        # draw polygon between points
        pygame.draw.polygon(
            self.sprite,
            self.config["color"],
            [
                (
                    p.position.x,
                    p.position.y + h + np.sin(SORA.ENGINE_UPTIME + p.position.x) * 3,
                )
                for p in self.points
            ]
            + [(self.area[0], self.area[1]), (0, self.area[1])],
        )
