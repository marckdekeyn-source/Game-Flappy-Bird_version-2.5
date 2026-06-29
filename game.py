"""
Core Game Engine Module
Mengatur Finite State Machine (FSM), penanganan loop game, kalkulasi skor,
pemrosesan screen-shake, dan integrasi antar komponen (Clean Architecture).
"""
import pygame
import random
import time
from game_config import GameConfig as Config
from save_manager import SaveManager
from audio import AudioSystem
from bird import Bird      # Mengambil dari bird.py
from pipe import Pipe      # Mengambil dari pipe.py
from ui import ModernButton, ModernSlider, UIUtils
from animation import ParallaxBackground, Particle
from achievement import AchievementTracker

class GameEngine:
    def __init__(self):
        pygame.init()
        self.save_manager = SaveManager()
        self.res = self.save_manager.data["settings"]["resolution"]
        
        if self.save_manager.data["settings"]["fullscreen"]:
            self.screen = pygame.display.set_mode(self.res, pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode(self.res)
            
        pygame.display.set_caption("Flappy Bird 2.5 Pro")
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = Config.STATE_SPLASH
        
        # System Inits
        self.audio = AudioSystem(self.save_manager)
        self.bg_parallax = ParallaxBackground(self.res[0], self.res[1])
        self.achievement_tracker = AchievementTracker(self.save_manager, self.audio)
        
        # Load Fonts
        self.font_title = pygame.font.SysFont("Impact", 56)
        self.font_main = pygame.font.SysFont("Arial", 24, bold=True)
        self.font_sub = pygame.font.SysFont("Arial", 18)

        # Game Session Variables
        self.bird = None
        self.pipes = []
        self.particles = []
        self.score = 0
        self.last_pipe_spawn = 0
        self.state_timer = 120 # Untuk timer splash/loading screen
        self.shake_intensity = 0
        self.countdown_val = 3
        
        # Initialize UI Components
        self._init_ui_buttons()
        self.slider_music = ModernSlider(540, 260, 200, 10, self.audio.music_volume)
        self.slider_sfx = ModernSlider(540, 310, 200, 10, self.audio.sfx_volume)

        # Performance analytics session
        self.session_start_time = time.time()

    def _init_ui_buttons(self) -> None:
        cx = self.res[0] // 2
        # Main Menu Buttons
        self.menu_buttons = [
            ModernButton(cx - 120, 240, 240, 45, "▶ Play", lambda: self.switch_state(Config.STATE_COUNTDOWN)),
            ModernButton(cx - 120, 300, 240, 45, "📊 Statistics", lambda: self.switch_state(Config.STATE_STATS)),
            ModernButton(cx - 120, 360, 240, 45, "🏆 Achievement", lambda: self.switch_state(Config.STATE_ACHIEVEMENT)),
            ModernButton(cx - 120, 420, 240, 45, "🐦 Bird Collection", lambda: self.switch_state(Config.STATE_SKIN)),
            ModernButton(cx - 120, 480, 240, 45, "⚙ Settings", lambda: self.switch_state(Config.STATE_SETTINGS)),
            ModernButton(cx - 120, 540, 240, 45, "🚪 Exit", self.quit_game)
        ]
        # Back Buttons Universal
        self.btn_back = ModernButton(40, 40, 110, 40, "← Back", lambda: self.switch_state(Config.STATE_MENU))
        # Pause Buttons
        self.pause_buttons = [
            ModernButton(cx - 100, 260, 200, 45, "Resume", lambda: self.switch_state(Config.STATE_PLAYING)),
            ModernButton(cx - 100, 320, 200, 45, "Restart", lambda: self.switch_state(Config.STATE_COUNTDOWN)),
            ModernButton(cx - 100, 380, 200, 45, "Main Menu", lambda: self.switch_state(Config.STATE_MENU)),
            ModernButton(cx - 100, 440, 200, 45, "Quit", self.quit_game)
        ]
        # Game Over Buttons
        self.gameover_buttons = [
            ModernButton(cx - 210, 460, 200, 50, "Play Again", lambda: self.switch_state(Config.STATE_COUNTDOWN)),
            ModernButton(cx + 10, 460, 200, 50, "Main Menu", lambda: self.switch_state(Config.STATE_MENU))
        ]

    def switch_state(self, new_state: int) -> None:
        self.state = new_state
        if new_state == Config.STATE_COUNTDOWN:
            self.reset_match()
            self.countdown_val = 3
            self.state_timer = 45 # Per-angka durasi countdown
        elif new_state == Config.STATE_MENU:
            self.save_manager.data["statistics"]["play_time"] += round((time.time() - self.session_start_time) / 60, 2)
            self.session_start_time = time.time()
            self.save_manager.save_data()

    def reset_match(self) -> None:
        current_skin = self.save_manager.data["skins"]["current"]
        self.bird = Bird(250, self.res[1] // 2, current_skin)
        self.pipes.clear()
        self.particles.clear()
        self.score = 0
        self.last_pipe_spawn = pygame.time.get_ticks()

    def quit_game(self) -> None:
        self.running = False

    def handle_events(self) -> None:
        m_pos = pygame.mouse.get_pos()
        m_clicked = False
        m_down = pygame.mouse.get_pressed()[0]
        
        for event in pygame.get_pattern() if hasattr(pygame, "get_pattern") else pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: m_clicked = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_p:
                    if self.state == Config.STATE_PLAYING:
                        self.switch_state(Config.STATE_PAUSE)
                    elif self.state == Config.STATE_PAUSE:
                        self.switch_state(Config.STATE_PLAYING)
                if event.key == pygame.K_SPACE:
                    if self.state == Config.STATE_PLAYING:
                        self.bird.jump()
                        self.audio.play_sfx("jump")
                        # Spawn partikel lompat
                        for _ in range(5):
                            self.particles.append(Particle(self.bird.x, self.bird.y, self.bird.color))

        # Update UI Buttons berdasarkan state saat ini
        if m_clicked: self.audio.play_sfx("click")
        
        if self.state == Config.STATE_MENU:
            for btn in self.menu_buttons: btn.update(m_pos, m_clicked)
        elif self.state in [Config.STATE_STATS, Config.STATE_ACHIEVEMENT, Config.STATE_SKIN, Config.STATE_SETTINGS]:
            if self.btn_back.update(m_pos, m_clicked): return
            
            if self.state == Config.STATE_SETTINGS:
                old_m, old_s = self.audio.music_volume, self.audio.sfx_volume
                self.audio.set_music_volume(self.slider_music.update(m_pos, m_down))
                self.audio.set_sfx_volume(self.slider_sfx.update(m_pos, m_down))
                
                # Check Reset Progress Button
                btn_reset = ModernButton(self.res[0]//2 - 100, 420, 200, 40, "Reset Data", self.save_manager.reset_progress)
                btn_reset.update(m_pos, m_clicked)
                
            elif self.state == Config.STATE_SKIN:
                # Loop dynamic selection buttons
                for i, name in enumerate(["Default", "Blue", "Red", "Golden"]):
                    btn_skin = ModernButton(250 + (i*200), 480, 160, 45, f"Select {name}", lambda n=name: self._select_skin(n))
                    btn_skin.update(m_pos, m_clicked)
                    
        elif self.state == Config.STATE_PAUSE:
            for btn in self.pause_buttons: btn.update(m_pos, m_clicked)
        elif self.state == Config.STATE_GAMEOVER:
            for btn in self.gameover_buttons: btn.update(m_pos, m_clicked)

    def _select_skin(self, name: str) -> None:
        self.save_manager.data["skins"]["current"] = name
        self.save_manager.save_data()

    def update(self) -> None:
        self.bg_parallax.update()
        self.achievement_tracker.update()
        
        # State Logic Machine
        if self.state in [Config.STATE_SPLASH, Config.STATE_LOADING]:
            self.state_timer -= 1
            if self.state_timer <= 0:
                self.switch_state(Config.STATE_LOADING if self.state == Config.STATE_SPLASH else Config.STATE_MENU)
                self.state_timer = 90
                
        elif self.state == Config.STATE_COUNTDOWN:
            self.state_timer -= 1
            if self.state_timer <= 0:
                self.countdown_val -= 1
                self.state_timer = 45
                if self.countdown_val < 0:
                    self.state = Config.STATE_PLAYING
                    
        elif self.state == Config.STATE_PLAYING:
            self.bird.update()
            
            # Spawn Pipa otomatis
            now = pygame.time.get_ticks()
            if now - self.last_pipe_spawn > Config.PIPE_SPAWN_TIME:
                gap_y = random.randint(150, self.res[1] - 150 - Config.PIPE_GAP)
                self.pipes.append(Pipe(self.res[0], gap_y))
                self.last_pipe_spawn = now
                
            # Update Pipa & Collisions
            for pipe in self.pipes[:]:
                pipe.update()
                
                # Cek Tabrakan Presisi Tinggi menggunakan AABB Rect
                t_rect, b_rect = pipe.get_rects(self.res[1])
                b_rect_ent = self.bird.get_rect()
                if b_rect_ent.colliderect(t_rect) or b_rect_ent.colliderect(b_rect):
                    self.trigger_gameover()
                    
                # Hitung Score Passing Pipa
                if not pipe.passed and pipe.x < self.bird.x:
                    pipe.passed = True
                    self.score += 1
                    self.audio.play_sfx("score")
                    self.save_manager.data["statistics"]["pipes_passed"] += 1
                    for _ in range(10): # Partikel reward
                        self.particles.append(Particle(pipe.x + 45, self.res[1]//2, Config.COLOR_SUCCESS))

                # Hapus pipa luar layar
                if pipe.x < -100:
                    self.pipes.remove(pipe)
                    
            # Batasan layar atas/bawah ground
            if self.bird.y - self.bird.radius > self.res[1] - 80 or self.bird.y + self.bird.radius < 0:
                self.trigger_gameover()
                
        # Update system partikel
        self.particles = [p for p in self.particles if p.update()]
        
        # Hitung reduksi screen shake
        if self.shake_intensity > 0:
            self.shake_intensity -= 1

    def trigger_gameover(self) -> None:
        self.audio.play_sfx("hit")
        self.shake_intensity = 15
        self.state = Config.STATE_GAMEOVER
        
        # Menyimpan Score & Stats
        stats = self.save_manager.data["statistics"]
        stats["games_played"] += 1
        
        if self.score > self.save_manager.data["high_score"]:
            self.save_manager.data["high_score"] = self.score
            
        # Kalkulasi rata-rata skor
        total_games = stats["games_played"]
        stats["average_score"] = round(((stats["average_score"] * (total_games-1)) + self.score) / total_games, 1)
        
        # Validasi achievement unlock
        self.achievement_tracker.check_achievements()
        self.save_manager.save_data()

    def get_medal_string(self, score: int) -> str:
        if score >= 40: return "💎 Diamond"
        if score >= 30: return "🥇 Gold"
        if score >= 20: return "🥈 Silver"
        if score >= 10: return "🥉 Bronze"
        return "None"

    def render(self) -> None:
        # Menangani screen shake surface translation
        render_surf = pygame.Surface(self.res)
        self.bg_parallax.draw(render_surf)
        
        # Draw game entities jika sedang bermain/pause/gameover
        if self.state in [Config.STATE_PLAYING, Config.STATE_PAUSE, Config.STATE_GAMEOVER, Config.STATE_COUNTDOWN]:
            for pipe in self.pipes:
                pipe.draw(render_surf, self.res[1])
            self.bird.draw(render_surf)
            
        for p in self.particles:
            p.draw(render_surf)
            
        # HUD Panel Transparan Modern pada saat Game Aktif
        if self.state == Config.STATE_PLAYING:
            hud_p = pygame.Surface((220, 80), pygame.SRCALPHA)
            pygame.draw.rect(hud_p, (20, 20, 30, 160), (0,0, 220, 80), border_radius=12)
            render_surf.blit(hud_p, (self.res[0] - 250, 30))
            render_surf.blit(self.font_sub.render(f"SCORE: {self.score}", True, Config.COLOR_TEXT), (self.res[0]-230, 42))
            render_surf.blit(self.font_sub.render(f"BEST:  {self.save_manager.data['high_score']}", True, Config.COLOR_ACCENT), (self.res[0]-230, 68))
            
        # State Interfaces Overlay
        if self.state == Config.STATE_SPLASH:
            UIUtils.draw_text_with_shadow(render_surf, "MADE WITH PYTHON & PYGAME", self.font_main, Config.COLOR_TEXT, (self.res[0]//2, self.res[1]//2))
        elif self.state == Config.STATE_LOADING:
            UIUtils.draw_text_with_shadow(render_surf, "LOADING ASSETS...", self.font_main, Config.COLOR_PRIMARY, (self.res[0]//2, self.res[1]//2))
            pygame.draw.rect(render_surf, (40, 40, 50), (self.res[0]//2 - 150, self.res[1]//2 + 40, 300, 15), border_radius=6)
            pygame.draw.rect(render_surf, Config.COLOR_PRIMARY, (self.res[0]//2 - 150, self.res[1]//2 + 40, int(300 * (1 - self.state_timer/90)), 15), border_radius=6)
            
        elif self.state == Config.STATE_MENU:
            UIUtils.draw_text_with_shadow(render_surf, "FLAPPY BIRD 2.5", self.font_title, Config.COLOR_PRIMARY, (self.res[0]//2, 130))
            for btn in self.menu_buttons: btn.draw(render_surf, self.font_main)
            
        elif self.state == Config.STATE_COUNTDOWN:
            txt = "GO!" if self.countdown_val == 0 else str(self.countdown_val)
            UIUtils.draw_text_with_shadow(render_surf, txt, self.font_title, Config.COLOR_ACCENT, (self.res[0]//2, self.res[1]//2))
            
        elif self.state == Config.STATE_PAUSE:
            blur_overlay = pygame.Surface(self.res, pygame.SRCALPHA)
            blur_overlay.fill((10, 10, 15, 200)) # Efek overlay gelap transparan
            render_surf.blit(blur_overlay, (0,0))
            UIUtils.draw_text_with_shadow(render_surf, "PAUSED", self.font_title, Config.COLOR_TEXT, (self.res[0]//2, 160))
            for btn in self.pause_buttons: btn.draw(render_surf, self.font_main)
            
        elif self.state == Config.STATE_GAMEOVER:
            blur_overlay = pygame.Surface(self.res, pygame.SRCALPHA)
            blur_overlay.fill((20, 5, 5, 180))
            render_surf.blit(blur_overlay, (0,0))
            
            panel = pygame.Surface((460, 220), pygame.SRCALPHA)
            pygame.draw.rect(panel, (35, 30, 30, 240), (0,0, 460, 220), border_radius=16)
            pygame.draw.rect(panel, Config.COLOR_DANGER, (0,0, 460, 220), width=2, border_radius=16)
            render_surf.blit(panel, (self.res[0]//2 - 230, 200))
            
            UIUtils.draw_text_with_shadow(render_surf, "GAME OVER", self.font_title, Config.COLOR_DANGER, (self.res[0]//2, 140))
            render_surf.blit(self.font_main.render(f"Final Score: {self.score}", True, Config.COLOR_TEXT), (self.res[0]//2 - 180, 230))
            render_surf.blit(self.font_main.render(f"Best Score:  {self.save_manager.data['high_score']}", True, Config.COLOR_ACCENT), (self.res[0]//2 - 180, 270))
            render_surf.blit(self.font_main.render(f"Medal Award: {self.get_medal_string(self.score)}", True, Config.COLOR_PRIMARY), (self.res[0]//2 - 180, 310))
            
            for btn in self.gameover_buttons: btn.draw(render_surf, self.font_main)
            
        elif self.state == Config.STATE_STATS:
            self.btn_back.draw(render_surf, self.font_main)
            UIUtils.draw_text_with_shadow(render_surf, "PLAYER STATISTICS", self.font_title, Config.COLOR_TEXT, (self.res[0]//2, 100))
            s = self.save_manager.data["statistics"]
            labels = [
                f"Games Played: {s['games_played']}",
                f"Highest Score: {self.save_manager.data['high_score']}",
                f"Average Score: {s['average_score']}",
                f"Pipes Passed: {s['pipes_passed']}",
                f"Total Play Time: {s['play_time']} mins"
            ]
            for i, text in enumerate(labels):
                render_surf.blit(self.font_main.render(text, True, Config.COLOR_TEXT), (250, 220 + (i*45)))

        elif self.state == Config.STATE_ACHIEVEMENT:
            self.btn_back.draw(render_surf, self.font_main)
            UIUtils.draw_text_with_shadow(render_surf, "ACHIEVEMENTS", self.font_title, Config.COLOR_ACCENT, (self.res[0]//2, 100))
            ach = self.save_manager.data["achievements"]
            for i, (name, unlocked) in enumerate(ach.items()):
                color = Config.COLOR_TEXT if unlocked else Config.COLOR_TEXT_MUTED
                prefix = "🏆" if unlocked else "🔒"
                status_txt = "Unlocked" if unlocked else "Locked"
                
                box = pygame.Surface((700, 50), pygame.SRCALPHA)
                pygame.draw.rect(box, (30,30,40, 200) if unlocked else (20,20,25, 120), (0,0, 700, 50), border_radius=8)
                render_surf.blit(box, (290, 200 + (i*65)))
                
                render_surf.blit(self.font_main.render(f"{prefix} {name}", True, color), (310, 210 + (i*65)))
                render_surf.blit(self.font_sub.render(status_txt, True, Config.COLOR_SUCCESS if unlocked else Config.COLOR_DANGER), (860, 212 + (i*65)))

        elif self.state == Config.STATE_SKIN:
            self.btn_back.draw(render_surf, self.font_main)
            UIUtils.draw_text_with_shadow(render_surf, "BIRD COLLECTION", self.font_title, Config.COLOR_PRIMARY, (self.res[0]//2, 100))
            
            # Draw preview birds rotating/floating
            for i, (name, color) in enumerate([("Default", (241,196,15)), ("Blue", (52,152,219)), ("Red", (231,76,60)), ("Golden", (255,215,0))]):
                cx = 330 + (i * 200)
                cy = 320
                pygame.draw.circle(render_surf, color, (cx, cy), 35)
                pygame.draw.circle(render_surf, (255,255,255), (cx+14, cy-6), 8)
                if self.save_manager.data["skins"]["current"] == name:
                    pygame.draw.circle(render_surf, Config.COLOR_SUCCESS, (cx, cy + 60), 8) # Active indicator
                render_surf.blit(self.font_sub.render(name, True, Config.COLOR_TEXT), (cx - 25, cy + 85))
                
                btn_skin = ModernButton(cx - 80, 450, 160, 40, "Equip", lambda n=name: self._select_skin(n))
                btn_skin.draw(render_surf, self.font_sub)

        elif self.state == Config.STATE_SETTINGS:
            self.btn_back.draw(render_surf, self.font_main)
            UIUtils.draw_text_with_shadow(render_surf, "SETTINGS", self.font_title, Config.COLOR_TEXT, (self.res[0]//2, 100))
            
            render_surf.blit(self.font_main.render("Music Volume:", True, Config.COLOR_TEXT), (320, 250))
            self.slider_music.draw(render_surf)
            render_surf.blit(self.font_sub.render(f"{int(self.slider_music.value*100)}%", True, Config.COLOR_TEXT), (760, 250))
            
            render_surf.blit(self.font_main.render("SFX Volume:", True, Config.COLOR_TEXT), (320, 300))
            self.slider_sfx.draw(render_surf)
            render_surf.blit(self.font_sub.render(f"{int(self.slider_sfx.value*100)}%", True, Config.COLOR_TEXT), (760, 300))
            
            btn_reset = ModernButton(self.res[0]//2 - 100, 420, 200, 40, "Reset Progress", self.save_manager.reset_progress)
            btn_reset.draw(render_surf, self.font_sub)

        # Draw Dynamic Popups Achievement di paling atas layer
        self.achievement_tracker.draw_popup(render_surf, self.font_sub)

        # Blit rendering surface ke main screen dengan kalkulasi screen shake vibration
        shake_x = random.randint(-self.shake_intensity, self.shake_intensity) if self.shake_intensity > 0 else 0
        shake_y = random.randint(-self.shake_intensity, self.shake_intensity) if self.shake_intensity > 0 else 0
        self.screen.blit(render_surf, (shake_x, shake_y))
        
        pygame.display.flip()

    def run(self) -> None:
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(Config.FPS)
            
        pygame.quit()