"""
Save Manager Module
Menangani sistem I/O data pemain berbasis JSON secara aman.
"""
import os
import json
from typing import Dict, Any

class SaveManager:
    def __init__(self, filename: str = "save/save.json"):
        self.filename = filename
        self.default_data: Dict[str, Any] = {
            "high_score": 0,
            "settings": {
                "music_volume": 0.8,
                "sfx_volume": 0.6,
                "resolution": [1280, 720],
                "fullscreen": False,
                "fps_limit": 60
            },
            "statistics": {
                "games_played": 0,
                "pipes_passed": 0,
                "play_time": 0.0,
                "average_score": 0.0
            },
            "skins": {
                "current": "Default",
                "unlocked": ["Default"]
            },
            "achievements": {
                "First Flight": False,
                "Rookie": False,
                "Skilled": False,
                "Expert": False,
                "Master Bird": False
            }
        }
        self.data = self.load_data()

    def load_data(self) -> Dict[str, Any]:
        if not os.path.exists("save"):
            os.makedirs("save")
        
        if not os.path.exists(self.filename):
            self.save_data(self.default_data)
            return self.default_data
        
        try:
            with open(self.filename, 'r') as f:
                return json.load(f)
        except Exception:
            return self.default_data

    def save_data(self, data: Dict[str, Any] = None) -> None:
        if data is not None:
            self.data = data
        with open(self.filename, 'w') as f:
            json.dump(self.data, f, indent=4)

    def reset_progress(self) -> None:
        self.data = self.default_data.copy()
        self.save_data()