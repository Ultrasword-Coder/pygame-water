import pygame
from pygame import draw as pgdraw
from pygame import math as pgmath

import soragl as SORA
from soragl import physics, base_objects, smath


# ------------------------------- #
# ball

class Ball(physics.Entity):
    def __init__(self, radius: int):
        """Initialize the ball object"""
        super().__init__()
        self.radius = radius
        self.area = (radius*2, radius*2)
        
        # components
        self.c_sprite = base_objects.Sprite(self.area[0], self.area[1])
        self.sprite = self.c_sprite.sprite
        pgdraw.circle(self.sprite, (255, 255, 255), self.rect.center, self.radius)

    def on_ready(self):
        """Called when the object is ready."""
        self.add_component(self.c_sprite)
        self.add_component(base_objects.SpriteRenderer())
        self.add_component(base_objects.Collision2DComponent())
    
    #=== update
    def update(self):
        """Update ball"""
        self.velocity += physics.World2D.GRAVITY * SORA.DELTA

