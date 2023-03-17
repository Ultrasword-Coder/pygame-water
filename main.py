import pygame
import soragl as SORA
import struct

from pygame import draw as pgdraw
from pygame import math as pgmath
from soragl import animation, scene, physics, base_objects, mgl

# ------------------------------ #
# setup
SORA.initialize(
    {
        "fps": 30,
        "window_size": [1280, 720],
        "window_flags": pygame.RESIZABLE | pygame.DOUBLEBUF,
        "window_bits": 32,
        "framebuffer_flags": pygame.SRCALPHA,
        "framebuffer_size": [1280 // 3, 720 // 3],
        "framebuffer_bits": 32,
        "debug": True,
    }
)

SORA.create_context()

# ------------------------------- #
# imports

from scripts import water

# ------------------------------- #

sc = scene.Scene(config=scene.load_config(scene.Scene.DEFAULT_CONFIG))
scw = sc.make_layer(sc.get_config(), 1)
# scw.get_chunk(0, 0)

# create water
ww = water.Water(300, 50)
ww.position.xy = (200, 200)

scw.add_entity(ww)

# aspects
# scw.add_aspect(base_objects.TileMapDebug())
scw.add_aspect(base_objects.SpriteRendererAspectDebug())
scw.add_aspect(base_objects.Collision2DRendererAspectDebug())
scw.add_aspect(base_objects.RenderableAspect())

# push scene
scene.SceneHandler.push_scene(sc)

# ------------------------------ #
# game loop
SORA.start_engine_time()
while SORA.RUNNING:
    # SORA.FRAMEBUFFER.fill((255, 255, 255, 255))
    SORA.FRAMEBUFFER.fill((0, 0, 0, 255))
    SORA.DEBUGBUFFER.fill((0, 0, 0, 0))
    # pygame update + render
    scene.SceneHandler.update()

    if SORA.is_key_clicked(pygame.K_d) and SORA.is_key_pressed(pygame.K_LSHIFT):
        SORA.DEBUG = not SORA.DEBUG

    # push frame
    SORA.push_framebuffer()
    # pygame.display.flip()
    # update events
    SORA.update_hardware()
    SORA.handle_pygame_events()
    # clock tick
    SORA.CLOCK.tick(SORA.FPS)
    SORA.update_time()

pygame.quit()
