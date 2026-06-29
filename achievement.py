"""
Achievement & Statistics Modules
Memproses kalkulasi milestone, pencatatan waktu bermain, serta notifikasi popup.
"""
import pygame
from typing import Dict, List, Tuple
from game_config import GameConfig as Config

class AchievementTracker:
    def __init__(self, save_manager, audio_system):
        self.save_manager = save_manager
        self.audio_system = audio_system
        self.popup_queue: List[str] = []
        self.popup_y = -80
        self.popup_timer = 0

    def check_achievements(self) -> None:
        stats = self.save_manager.data["statistics"]
        ach = self.save_manager.data["achievements"]
        high = self.save_manager.data["high_score"]

        milestones: List[Tuple[str, bool]] = [
            ("First Flight", stats["games_played"] >= 1),
            ("Rookie", high >= 10),
            ("Skilled", high >= 25),
            ("Expert", high >= 50),
            ("Master Bird", high >= 100)
        ]

        for name, condition in milestones:
            if condition and not ach[name]:
                ach[name] = True
                self.popup_queue.append(name)
                self.audio_system.play_sfx("achievement")
                self.save_manager.save_data()

    def update(self) -> None:
        if self.popup_queue:
            if self.popup_timer <= 0:
                self.popup_timer = 180  # Tampil selama 3 detik pada 60fps
                self.popup_y = -80
            
            self.popup_timer -= 1
            if self.popup_timer > 150:  # Slide down
                self.popup_y += (60 - self.popup_y) * 0.2
            elif self.popup_timer < 30: # Slide up
                self.popup_y += (-90 - self.popup_y) * 0.2
                if self.popup_timer == 0:
                    self.popup_queue.pop(0)
        else:
            self.popup_y = -80

    def draw_popup(self, surface: pygame.Surface, font: pygame.font.Font) -> None:
        if not self.popup_queue: return
        name = self.popup_queue[0]
        
        # Render Banner Transparan
        box_w, box_h = 320, 70
        box_x = (surface.get_width() - box_w) // 2
        popup_surf = pygame.Surface((box_w, box_h), pygame.SRCALPHA)
        pygame.draw.rect(popup_surf, (30, 30, 45, 235), (0,0, box_w, box_h), border_radius=16)
        pygame.draw.rect(popup_surf, Config.COLOR_ACCENT, (0,0, box_w, box_h), width=2, border_radius=16)
        
        # Tulisan teks popup
        lbl = font.render("🏆 Achievement Unlocked!", True, Config.COLOR_ACCENT)
        ach_lbl = font.render(name, True, Config.COLOR_TEXT)
        popup_surf.blit(lbl, (20, 12))
        popup_surf.blit(ach_lbl, (20, 38))
        
        surface.blit(popup_surf, (box_x, int(self.popup_y)))