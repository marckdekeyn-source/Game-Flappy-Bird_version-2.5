# 🚀 Flappy Bird Remake v2.5 - Professional Python Edition

[![Python Version](https://img.shields.io/badge/python-3.12%2B-blue.svg)](https://www.python.org)
[![Pygame](https://img.shields.io/badge/pygame-2.6.1-green.svg)](https://www.pygame.org)
[![Architecture](https://img.shields.io/badge/Architecture-Clean%20OOP-orange.svg)]()
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://opensource.org/licenses/MIT)

## 📌 Asal-Usul Proyek & Rekayasa Ulang (Project History)
Proyek ini merupakan **arsitektur ulang berskala besar (Total Refactoring)** dari basis kode monolitik awal yang berada di repositori resmi **[LaOdhe16/Projek-Game-Flappy-Bird](https://github.com/LaOdhe16/Projek-Game-Flappy-Bird)**. 

Pada versi lawas (`v1.0/app.py`), seluruh logika permainan, data, *rendering*, dan audio digabungkan dalam satu berkas tunggal (*Spaghetti Code*). Versi **v2.5** ini dibangun kembali secara mandiri dari dasar (*from scratch*) untuk menerapkan pemisahan tugas modular yang ketat sesuai dengan standar industri pengembangan perangkat lunak.

---

## ✨ Fitur Utama (Core Features)

* **Sistem Koleksi Skin Burung:** Mekanik kustomisasi karakter yang mendukung pergantian skin secara *real-time* (Default, Blue, Red, dan Golden Bird dengan efek *glow*).
* **Parallax Background Engine:** Sistem visual berlapis yang mensimulasikan ilusi kedalaman bergerak (*seamless looping scrolling*) memisahkan awan, gunung, dan tanah.
* **Sistem Penyimpanan Otomatis (I/O JSON):** Progres skor tertinggi (*high score*), preferensi pengaturan volume, dan statistik permainan tersimpan secara persisten di `save/save.json`.
* **Dashboard Analitik & Statistik:** Melacak data bermain pemain secara komprehensif (total permainan, pipa yang dilewati, rata-rata skor, hingga kalkulasi waktu bermain).
* **Sistem Pencapaian (Achievements Unlocker):** Pelacakan *milestone* prestasi otomatis yang terintegrasi dengan animasi *popup banner notification* di dalam game.
* **Juiciness & Game Feel Effects:** Dilengkapi dengan efek getaran layar (*Screen Shake*) saat terjadi benturan, sistem partikel dinamis (*Particle Burst*) saat melompat atau mendapat poin, serta *drop shadow text*.
* **Procedural Audio Fallback:** Menggunakan sintesis gelombang audio prosedural (pustaka `math` & `array` bawaan) untuk memastikan game tidak akan *crash* saat inisialisasi awal walaupun file fisik audio absen.

---

## 📁 Struktur Modul Proyek (Clean Architecture)

```text
Projek-Game-Flappy-Bird/
│
├── main.py              # Entry-point / Gerbang utama eksekusi game (Menggantikan app.py lama)
├── game.py              # Core Game Engine (State Machine Controller)
├── game_config.py       # Global configuration, data warna, dan resolusi
├── save_manager.py      # Secure JSON Data File I/O handler
├── ui.py                # Komponen UI Reusable (Custom Button & Slider)
├── animation.py         # Particle system & Parallax background controller
├── skin.py              # Central database palet warna skin karakter
├── achievement.py       # Logika kalkulasi milestone & popup notification
├── statistics.py        # Pengolah data statistik dan analitik
├── bird.py              # Entitas kinematika burung dan logika rotasi
├── pipe.py              # Entitas rintangan pipa (AABB Collision Box)
│
├── assets/              # Tempat penyimpanan aset gambar (.png) & suara (.wav)
└── save/
    └── save.json        # Berkas data JSON lokal progres bermain pemain