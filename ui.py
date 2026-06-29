"""
UI Engine Module
Menyediakan builder UI kustom, tombol interaktif dengan animasi hover, slider volume, dan text shadow.
"""
import pygame
from typing import Tuple, Callable
from game_config import GameConfig as Config

class ModernButton:
    def __init__(self, x: int, y: int, w: int, h: int, text: str, callback: Callable, border_radius: int = 12):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.callback = callback
        self.border_radius = border_radius
        self.is_hovered = False
        self.current_color = Config.COLOR_PANEL

    def update(self, mouse_pos: Tuple[int, int], mouse_clicked: bool) -> bool:
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        if self.is_hovered:
            self.current_color = (45, 52, 71)  # Warna panel agak terang saat hover
            if mouse_clicked:
                self.callback()
                return True
        else:
            self.current_color = Config.COLOR_PANEL
        return False

    def draw(self, surface: pygame.Surface, font: pygame.font.Font) -> None:
        # Efek Drop Shadow untuk Button
        shadow_rect = self.rect.copy()
        shadow_rect.y += 4
        pygame.draw.rect(surface, (10, 10, 15, 150), shadow_rect, border_radius=self.border_radius)
        
        # Gambar Kotak Utama Button
        pygame.draw.rect(surface, self.current_color, self.rect, border_radius=self.border_radius)
        
        # Border Glow jika di-hover kursor
        if self.is_hovered:
            pygame.draw.rect(surface, Config.COLOR_PRIMARY, self.rect, width=2, border_radius=self.border_radius)
            
        # Perataan Teks ke Tengah Button
        txt_s = font.render(self.text, True, Config.COLOR_TEXT)
        txt_r = txt_s.get_rect(center=self.rect.center)
        surface.blit(txt_s, txt_r)


class ModernSlider:
    def __init__(self, x: int, y: int, w: int, h: int, value: float):
        self.rect = pygame.Rect(x, y, w, h)
        self.value = value  # Nilai dari 0.0 sampai 1.0
        self.handle_radius = 10
        self.is_dragging = False

    def update(self, mouse_pos: Tuple[int, int], mouse_down: bool) -> float:
        if mouse_down:
            extended_rect = pygame.Rect(self.rect.x - 10, self.rect.y - 10, self.rect.w + 20, self.rect.h + 20)
            if extended_rect.collidepoint(mouse_pos):
                self.is_dragging = True
        else:
            self.is_dragging = False

        if self.is_dragging:
            relative_x = mouse_pos[0] - self.rect.x
            self.value = max(0.0, min(1.0, relative_x / self.rect.w))
            
        return self.value

    def draw(self, surface: pygame.Surface) -> None:
        # Background track slider
        pygame.draw.rect(surface, (60, 64, 80), self.rect, border_radius=4)
        # Active track slider (Warna progress)
        active_w = int(self.rect.w * self.value)
        if active_w > 0:
            pygame.draw.rect(surface, Config.COLOR_PRIMARY, (self.rect.x, self.rect.y, active_w, self.rect.h), border_radius=4)
        # Knob / Buletan handle slider
        handle_x = self.rect.x + active_w
        handle_y = self.rect.y + (self.rect.h // 2)
        pygame.draw.circle(surface, Config.COLOR_TEXT, (handle_x, handle_y), self.handle_radius)


class UIUtils:
    @staticmethod
    def draw_text_with_shadow(surface: pygame.Surface, text: str, font: pygame.font.Font, color: Tuple[int, int, int], center_pos: Tuple[int, int]) -> None:
        # Render Bayangan Teks (Warna gelap digeser sedikit)
        shadow_s = font.render(text, True, (15, 15, 20))
        shadow_r = shadow_s.get_rect(center=(center_pos[0] + 3, center_pos[1] + 3))
        surface.blit(shadow_s, shadow_r)
        
        # Render Teks Utama
        main_s = font.render(text, True, color)
        main_r = main_s.get_rect(center=center_pos)
        surface.blit(main_s, main_r)