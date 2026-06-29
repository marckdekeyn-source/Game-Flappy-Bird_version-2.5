"""
Entities Module: Bird and Pipe Classes
Mengimplementasikan pergerakan burung (kinematika), rotasi, dan manajemen rintangan pipa.
"""
import pygame
import math
from game_config import GameConfig as Config 
from skin import SkinSystem

class Bird:
    def __init__(self, x: int, y: int, skin_name: str = "Default"):
        self.x = x
        self.y = y
        self.velocity = 0.0
        self.skin_name = skin_name
        self.color = SkinSystem.get_color(skin_name)
        self.radius = 24
        self.anim_frame = 0
        self.angle = 0.0

    def jump(self) -> None:
        self.velocity = Config.FLAP_POWER

    def update(self) -> None:
        self.velocity += Config.GRAVITY
        self.y += self.velocity
        self.anim_frame = (self.anim_frame + 1) % 30 # Siklus animasi kepak
        
        # Kalkulasi rotasi sudut (Clamping antara -30 deg hingga 70 deg)
        target_angle = -self.velocity * 5.0
        self.angle += (target_angle - self.angle) * 0.2
        self.angle = max(-70.0, min(30.0, self.angle))

    def draw(self, surface: pygame.Surface) -> None:
        # Membuat permukaan transparan untuk rotasi aman
        bird_surf = pygame.Surface((self.radius*2 + 20, self.radius*2 + 20), pygame.SRCALPHA)
        
        # Efek Kepakan Sayap Prosedural (Wing Up, Mid, Down) berdasarkan amplitudo sinus
        wing_offset = math.sin(self.anim_frame * 0.4) * 8
        
        # Body Burung
        pygame.draw.circle(bird_surf, self.color, (self.radius + 10, self.radius + 10), self.radius)
        # Eye
        pygame.draw.circle(bird_surf, (255, 255, 255), (self.radius + 20, self.radius + 2), 6)
        pygame.draw.circle(bird_surf, (0, 0, 0), (self.radius + 22, self.radius + 2), 3)
        # Beak
        pygame.draw.polygon(bird_surf, (230, 126, 34), [(self.radius*2 + 6, self.radius + 5), (self.radius + 16, self.radius - 2), (self.radius + 16, self.radius + 12)])
        # Wing
        pygame.draw.ellipse(bird_surf, (max(0, self.color[0]-40), max(0, self.color[1]-40), max(0, self.color[2]-40)), (self.radius - 12, int(self.radius - 5 + wing_offset), 18, 14))

        # Golden Skin Glow effect
        if self.skin_name == "Golden":
            glow = pygame.Surface((self.radius*2 + 24, self.radius*2 + 24), pygame.SRCALPHA)
            pygame.draw.circle(glow, (255, 215, 0, 60), (self.radius+12, self.radius+12), self.radius + 6)
            surface.blit(glow, (int(self.x - self.radius - 12), int(self.y - self.radius - 12)))

        rotated_surf = pygame.transform.rotate(bird_surf, self.angle)
        new_rect = rotated_surf.get_rect(center=(int(self.x), int(self.y)))
        surface.blit(rotated_surf, new_rect.topleft)

    def get_rect(self) -> pygame.Rect:
        return pygame.Rect(int(self.x - self.radius + 4), int(self.y - self.radius + 4), self.radius*2 - 8, self.radius*2 - 8)