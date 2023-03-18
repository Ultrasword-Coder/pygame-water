import pygame
from pygame import draw as pgdraw
from pygame import math as pgmath

import soragl as SORA
from soragl import physics, base_objects, smath

import numpy as np
import scipy
from scipy import interpolate as sciinterpolate


# ------------------------------- #
# water

DEFAULT_CONFIG = {
    "color": (0, 0, 255, 159),
    "resolution": 3,
    "damping": 0.7,
    "tension": 0.01,
    "height": 0.5,
    "spread": 0.7,
}


class WaterSpring:
    def __init__(self, position, damping, tension):
        """Initialize the water spring."""
        self.position = pgmath.Vector2(position)
        self.hvel = 0
        self.damping = damping
        self.tension = tension

    def update(self):
        """Update the spring."""
        self.hvel = self.hvel * self.damping + self.tension * -self.position.y
        self.hvel *= self.damping
        self.position.y += self.hvel


class Water(physics.Entity):
    def __init__(self, width: int, height: int, config: dict = None):
        """Initialize the water object."""
        super().__init__()
        self.area = (width, height)
        self.config = config if config else DEFAULT_CONFIG.copy()
        self.surface = pygame.Surface(self.area)

        self.spread = self.config["spread"]
        self.damping = self.config["damping"]
        self.tension = self.config["tension"]
        self.w_height = 1 - self.config["height"]
        # points / 100px
        self.resolution = 100 / self.config["resolution"]
        self.section_w = int(self.area[0] / self.resolution)
        self.const_volume = self.section_w / self.area[0]
        # self.points = numpy.zeros(int(width / self.config["resolution"]))
        self.points = [
            WaterSpring((i, 0), self.damping, self.tension)
            for i in range(0, width + self.section_w, self.section_w)
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
        # negative because (pygame height stuff)
        self.w_height -= volume / self.area[0]

    def remove_volume(self, volume):
        """Remove volume from the water."""
        self.add_volume(-volume)

    def spread_wave(self):
        """Spread waves around"""
        # update first point
        self.points[0].hvel += self.spread * (
            self.points[1].position.y - self.points[0].position.y
        )
        # update rest
        for i in range(1, len(self.points) - 1):
            self.points[i].hvel += self.spread * (
                self.points[i + 1].position.y - self.points[i].position.y
            ) + self.spread * (
                self.points[i - 1].position.y - self.points[i].position.y
            )

    def splash(self, location, velocity):
        """Splash the water."""
        if 0 <= location < len(self.points):
            self.points[location].hvel += velocity

    def xpoint_to_location(self, xpoint):
        """Convert a point to a location."""
        return int(
            (xpoint - self.position.x + self.c_sprite.hwidth)
            / self.area[0]
            * len(self.points)
        )

    # === update

    def update(self):
        self.sprite.fill((0, 0, 0, 0))

        # testing
        if SORA.is_mouse_clicked(0):
            # self.add_volume(10)
            # and spread wave
            x = self.xpoint_to_location(SORA.get_mouse_rel()[0])
            self.splash(x, 10)

        # self.sprite.fill(self.config["color"])
        # draw each point
        h = self.area[1] * self.w_height
        self.spread_wave()

        addition_volume = 0
        for point in self.points:
            point.update()
            addition_volume += point.position.y
        # print(addition_volume)
        # calculate the extra height to add
        # draw each point as a circle on SORA.FRAMEBUFFER
        # for point in self.points:
        #     pgdraw.circle(
        #         SORA.FRAMEBUFFER,
        #         (255, 255, 255),
        #         (
        #             int(self.position.x - self.c_sprite.hwidth + point.position.x),
        #             int(self.position.y + point.position.y + h - self.c_sprite.hheight),
        #         ),
        #         3,
        #     )

        # draw polygon between points
        pygame.draw.polygon(
            self.sprite,
            self.config["color"],
            [
                (p.position.x, p.position.y + h - addition_volume * self.const_volume)
                for p in self.points
            ]
            + [(self.area[0], self.area[1]), (0, self.area[1])],
        )
