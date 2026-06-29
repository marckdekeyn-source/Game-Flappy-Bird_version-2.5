# game_config.py
import pygame
from typing import Tuple

class GameConfig:  # Mengubah nama kelas dari Config menjadi GameConfig
    BASE_WIDTH: int = 1280
    BASE_HEIGHT: int = 720
    FPS: int = 60
    
    STATE_SPLASH: int = 0
    STATE_LOADING: int = 1
    STATE_MENU: int = 2
    STATE_COUNTDOWN: int = 3
    STATE_PLAYING: int = 4
    STATE_PAUSE: int = 5
    STATE_GAMEOVER: int = 6
    STATE_STATS: int = 7
    STATE_ACHIEVEMENT: int = 8
    STATE_SKIN: int = 9
    STATE_SETTINGS: int = 10

    GRAVITY: float = 0.4
    FLAP_POWER: float = -8.5
    PIPE_SPEED: float = 4.5
    PIPE_SPAWN_TIME: int = 1500
    PIPE_GAP: int = 200

    COLOR_BG: Tuple[int, int, int] = (18, 18, 24)
    COLOR_PRIMARY: Tuple[int, int, int] = (52, 152, 219)
    COLOR_SUCCESS: Tuple[int, int, int] = (46, 204, 113)
    COLOR_ACCENT: Tuple[int, int, int] = (241, 196, 15)
    COLOR_DANGER: Tuple[int, int, int] = (231, 76, 60)
    COLOR_TEXT: Tuple[int, int, int] = (245, 246, 250)
    COLOR_TEXT_MUTED: Tuple[int, int, int] = (127, 143, 166)
    COLOR_PANEL: Tuple[int, int, int] = (30, 30, 40)

    @classmethod
    def get_scaled_size(cls, current_res: Tuple[int, int]) -> Tuple[float, float]:
        scale_x = current_res[0] / cls.BASE_WIDTH
        scale_y = current_res[1] / cls.BASE_HEIGHT
        return scale_x, scale_y