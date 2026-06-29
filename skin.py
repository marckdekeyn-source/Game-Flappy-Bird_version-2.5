"""
Skin System Module
Mengelola palet warna kustom dan logika visual untuk koleksi burung.
"""
from typing import Tuple, Dict

class SkinSystem:
    # Palet warna skin burung (R, G, B)
    SKINS: Dict[str, Tuple[int, int, int]] = {
        "Default": (241, 196, 15), # Kuning
        "Blue": (52, 152, 219),    # Biru
        "Red": (231, 76, 60),      # Merah
        "Golden": (255, 215, 0)    # Emas (Glow)
    }
    
    @classmethod
    def get_color(cls, name: str) -> Tuple[int, int, int]:
        """Mengembalikan warna RGB berdasarkan nama skin, fallback ke Default jika tidak ditemukan."""
        return cls.SKINS.get(name, cls.SKINS["Default"])