"""
Audio System Module
Mengatur efek suara (SFX) dan musik latar dengan aman menggunakan sistem fallback prosedural.
"""
import pygame
import math
import array
from typing import Dict

class AudioSystem:
    def __init__(self, save_manager):
        self.save_manager = save_manager
        pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
        self.sounds: Dict[str, pygame.mixer.Sound] = {}
        
        self.music_volume = self.save_manager.data["settings"]["music_volume"]
        self.sfx_volume = self.save_manager.data["settings"]["sfx_volume"]
        
        self._generate_procedural_sounds()
        self.set_sfx_volume(self.sfx_volume)

    def _generate_procedural_sounds(self) -> None:
        """Membuat suara prosedural sintetis (Sine wave) jika file aset eksternal kosong."""
        def make_beep(freq: float, duration: float, type_wave: str = "sine") -> pygame.mixer.Sound:
            sample_rate = 22050
            n_samples = int(sample_rate * duration)
            buf = array.array('h', [0] * n_samples)
            for i in range(n_samples):
                t = float(i) / sample_rate
                if type_wave == "sine":
                    val = math.sin(2.0 * math.pi * freq * t)
                elif type_wave == "square":
                    val = 1.0 if math.sin(2.0 * math.pi * freq * t) > 0 else -1.0
                buf[i] = int(val * 32767 * 0.5)
            return pygame.mixer.Sound(buffer=buf)

        # Generate standard audio feedbacks
        self.sounds["jump"] = make_beep(450, 0.1)
        self.sounds["score"] = make_beep(880, 0.15)
        self.sounds["hit"] = make_beep(150, 0.3, "square")
        self.sounds["click"] = make_beep(600, 0.05)
        self.sounds["hover"] = make_beep(700, 0.02)
        self.sounds["achievement"] = make_beep(587.33, 0.4) # D5 Note

    def play_sfx(self, name: str) -> None:
        if name in self.sounds:
            self.sounds[name].play()

    def set_sfx_volume(self, vol: float) -> None:
        self.sfx_volume = vol
        for snd in self.sounds.values():
            snd.set_volume(vol)
        self.save_manager.data["settings"]["sfx_volume"] = vol
        self.save_manager.save_data()

    def set_music_volume(self, vol: float) -> None:
        self.music_volume = vol
        pygame.mixer.music.set_volume(vol)
        self.save_manager.data["settings"]["music_volume"] = vol
        self.save_manager.save_data()