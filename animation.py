"""
Animation, Particle & Skin Engine
Menangani rendering dinamika partikel, parallax multi-layer, dan visualisasi skin.
"""
import pygame
import random
import math
from typing import List, Dict, Tuple
from game_config import GameConfig as Config

class Particle:
    def __init__(self, x: float, y: float, color: Tuple[int, int, int]):
        self.x = x
        self.y = y
        self.vx = random.uniform(-2, 2)
        self.vy = random.uniform(-2, 2)
        self.lifetime = 255
        self.color = color
        self.size = random.randint(3, 7)

    def update(self) -> bool:
        self.x += self.vx
        self.y += self.vy
        self.lifetime -= 8
        return self.lifetime > 0

    def draw(self, surface: pygame.Surface) -> None:
        if self.lifetime <= 0: return
        p_surf = pygame.Surface((self.size*2, self.size*2), pygame.SRCALPHA)
        pygame.draw.circle(p_surf, (self.color[0], self.color[1], self.color[2], self.lifetime), (self.size, self.size), self.size)
        surface.blit(p_surf, (int(self.x - self.size), int(self.y - self.size)))

class ParallaxBackground:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        # Lapisan paralaks: (Warna, Kecepatan relatif, Ketinggian, Offset)
        self.layers = [
            {"color": (26, 26, 36), "speed": 0.1, "height": height, "offset": 0},          # Sky
            {"color": (44, 44, 64), "speed": 0.3, "height": height * 0.6, "offset": 0},    # Clouds
            {"color": (58, 58, 86), "speed": 0.6, "height": height * 0.4, "offset": 0},    # Mountains
            {"color": (39, 174, 96), "speed": 1.2, "height": 80, "offset": 0}              # Ground
        ]

    def update(self) -> None:
        for layer in self.layers:
            layer["offset"] = (layer["offset"] + layer["speed"]) % self.width

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill(self.layers[0]["color"]) # Isi background dasar langit
        for layer in self.layers[1:]:
            # Menggambar dua segmen agar looping mulus tanpa patah-patah (seamless scrolling)
            y_pos = self.height - layer["height"]
            pygame.draw.rect(surface, layer["color"], (int(-layer["offset"]), int(y_pos), self.width + 5, int(layer["height"])))
            pygame.draw.rect(surface, layer["color"], (int(self.width - layer["offset"]), int(y_pos), self.width + 5, int(layer["height"])))