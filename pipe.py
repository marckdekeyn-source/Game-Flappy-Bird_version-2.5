"""
Pipe Entity Module
Mengimplementasikan rintangan pipa presisi tinggi dengan hitbox akurat.
"""
import pygame
import random
from typing import Tuple # <-- Ini yang tadi kurang agar Tuple bisa dibaca
from game_config import GameConfig as Config

class Pipe:
    def __init__(self, x: float, gap_y: float):
        self.x = x
        self.gap_y = gap_y
        self.width = 90
        self.gap_height = Config.PIPE_GAP
        self.passed = False

    def update(self) -> None:
        self.x -= Config.PIPE_SPEED

    def draw(self, surface: pygame.Surface, screen_height: int) -> None:
        color_pipe = (46, 204, 113)
        color_lip = (39, 174, 96)
        
        # Pipa Atas
        pygame.draw.rect(surface, color_pipe, (int(self.x), 0, self.width, int(self.gap_y)))
        pygame.draw.rect(surface, color_lip, (int(self.x - 4), int(self.gap_y - 30), self.width + 8, 30), border_radius=3)
        
        # Pipa Bawah
        bot_y = self.gap_y + self.gap_height
        pygame.draw.rect(surface, color_pipe, (int(self.x), int(bot_y), self.width, int(screen_height - bot_y)))
        pygame.draw.rect(surface, color_lip, (int(self.x - 4), int(bot_y), self.width + 8, 30), border_radius=3)

    def get_rects(self, screen_height: int) -> Tuple[pygame.Rect, pygame.Rect]:
        top_rect = pygame.Rect(int(self.x), 0, self.width, int(self.gap_y))
        bot_rect = pygame.Rect(int(self.x), int(self.gap_y + self.gap_height), self.width, int(screen_height - (self.gap_y + self.gap_height)))
        return top_rect, bot_rect