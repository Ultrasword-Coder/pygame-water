import pygame
import soragl as SORA
from soragl import physics, base_objects

# ------------------------------- #
# water

DEFAULT_CONFIG = {
    "color": (0, 0, 255, 255),
    "speed": 1,
    "amplitude": 10,
    "frequency": 0.1,
    "phase": 0,
    "period": 0,
    "resolution": 0.1,
}


class Water(physics.Entity):
    def __init__(self, width: int, height: int, config: dict = None):
        """Initialize the water object."""
        super().__init__()
        self.area = (width, height)
        self.config = config if config else DEFAULT_CONFIG.copy()
        self.surface = pygame.Surface(self.area)

        self.points = [0 for i in range(int(width / self.config["resolution"]))]
        self.freq = self.config["frequency"]
        self.amp = self.config["amplitude"]
        self.speed = self.config["speed"]
        self.phase = self.config["phase"]
        self.period = self.config["period"]

        # components
        self.c_sprite = base_objects.Sprite(width, height)
        self.sprite = self.c_sprite.sprite

    def on_ready(self):
        """Called when the object is ready."""
        self.add_component(self.c_sprite)
        self.add_component(base_objects.SpriteRenderer())
        print(self.position)

    def update(self):
        self.sprite.fill(self.config["color"])
