# 🚀 Flappy Bird Remake v2.5 - Professional Python Edition

[![Python Version](https://img.shields.io/badge/python-3.12%2B-blue.svg)](https://www.python.org)
[![Pygame](https://img.shields.io/badge/pygame-2.6.1-green.svg)](https://www.pygame.org)
[![Architecture](https://img.shields.io/badge/Architecture-Clean%20OOP-orange.svg)]()
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://opensource.org/licenses/MIT)

---

# 📌 Project History

This project is a **large-scale architecture refactor (Total Refactoring)** of the original monolithic codebase from the official repository:

> https://github.com/LaOdhe16/Projek-Game-Flappy-Bird

The original version (`v1.0/app.py`) contained all game logic, rendering, audio, UI, and data management inside a single file, making it difficult to maintain and extend.

Version **v2.5** has been completely rebuilt **from scratch** with a modular architecture following **Object-Oriented Programming (OOP)** principles and modern software engineering practices.

---

# ✨ Core Features

## 🎨 Bird Skin System

Customize your bird using multiple unlockable skins.

- Default Bird
- Blue Bird
- Red Bird
- Golden Bird (Glow Effect)

Supports **real-time skin switching**.

---

## 🌄 Parallax Background Engine

A seamless multi-layer scrolling background featuring:

- Clouds
- Mountains
- Ground

Creates a smooth illusion of depth.

---

## 💾 Auto Save System

Player progress is automatically stored inside:

```
save/save.json
```

Saved data includes:

- High Score
- Settings
- Volume
- Selected Skin
- Statistics

---

## 📊 Statistics Dashboard

Track your gameplay including:

- Total Games
- Highest Score
- Average Score
- Pipes Passed
- Total Play Time

---

## 🏆 Achievement System

Automatic achievement tracking with animated popup notifications.

Example achievements:

- First Flight
- 10 Pipes
- 25 Pipes
- 50 Pipes
- Score Master

---

## ✨ Game Feel Improvements

Extra polish for a better player experience.

Includes:

- Screen Shake
- Particle Effects
- Drop Shadow Text
- Smooth Animations

---

## 🔊 Procedural Audio Fallback

If audio files are missing, the game automatically generates procedural sound using Python's built-in libraries.

No crashes during startup.

---

# 📁 Project Structure

```text
Projek-Game-Flappy-Bird/
│
├── main.py              # Main Entry Point
├── game.py              # Game State Machine
├── game_config.py       # Global Configuration
├── save_manager.py      # JSON Save Handler
├── ui.py                # UI Components
├── animation.py         # Particle & Background Engine
├── skin.py              # Skin Database
├── achievement.py       # Achievement Logic
├── bird.py              # Bird Entity
├── pipe.py              # Pipe Entity
│
├── assets/
│   ├── images/
│   └── sounds/
│
└── save/
    └── save.json
```

---

# ⌨️ Game Controls

| Key | Action |
|------|--------|
| **SPACE** | Jump |
| **ESC** | Pause / Resume |
| **P** | Pause / Resume |
| **Mouse Click** | Navigate Menu |
| **Mouse Drag** | Adjust Volume Slider |

---

# 🛠️ Installation

## Requirements

- Python 3.12+
- Git
- Pygame 2.6+

---

## Clone Repository

### HTTPS

```bash
git clone https://github.com/marckdekeyn-source/Projek-Game-Flappy-Bird.git
```

### SSH

```bash
git clone git@github.com:marckdekeyn-source/Projek-Game-Flappy-Bird.git
```

### GitHub CLI

```bash
gh repo clone marckdekeyn-source/Projek-Game-Flappy-Bird
```

---

## Enter Project Directory

```bash
cd Projek-Game-Flappy-Bird
```

---

## Install Dependencies

```bash
pip install pygame
```

Or install from requirements:

```bash
pip install -r requirements.txt
```

---

## Run the Game

```bash
python main.py
```

---

# 📸 Screenshots

## 🏠 Main Menu
<img width="852" height="747" alt="image" src="https://github.com/user-attachments/assets/bf7b8ee9-03e6-4b80-9f09-e6d461265426" />



Modern main menu featuring quick access to Play, Statistics, Achievements, Bird Collection, and Settings.
```

---

## 🎮 Gameplay

<img width="1581" height="893" alt="Screenshot 2026-06-29 171053" src="https://github.com/user-attachments/assets/f5c76146-89dc-4b3e-ae59-e681d141fc01" />


Smooth gameplay powered by the Parallax Background Engine, particle effects, bird rotation, and improved collision detection.

```

---

## 📊 Statistics Dashboard
<img width="1367" height="622" alt="image" src="https://github.com/user-attachments/assets/ad2062bb-aa55-4947-a0e4-d0d2c8901266" />

Track your progress throughout every game session.

Statistics include:

- Highest Score
- Average Score
- Games Played
- Pipes Passed
- Total Play Time

## Settings

<img width="1112" height="625" alt="image" src="https://github.com/user-attachments/assets/a3c2edbb-323e-4382-9bc6-7ec0fde95dd8" />


# 🚀 Roadmap

- [ ] Moving Pipes
- [ ] Vertical Pipes
- [ ] Local Multiplayer
- [ ] Online Leaderboard
- [ ] Cloud Save
- [ ] Daily Challenges
- [ ] Controller Support
- [ ] Fullscreen Mode
- [ ] More Bird Skins
- [ ] Seasonal Themes
- [ ] New Soundtracks

---

# 👨‍💻 Contributors

## Original Project

**LaOdhe16**

Project Owner & Lead Developer

Original Flappy Bird Version (v1.0)

---

## Refactored Version

**marckdekeyn-source**

Core Contributor

Software Architect

Object-Oriented Refactoring

UI/UX Improvements

Gameplay Enhancements

Version 2.5

---

# 📜 License

This project is licensed under the **MIT License**.

Feel free to:

- Use
- Modify
- Learn from
- Fork
- Build your own version

for educational and portfolio purposes.

---

# ⭐ Support

If you enjoy this project, consider giving it a **⭐ Star** on GitHub.

It helps the project reach more developers and motivates future improvements.

---

## ❤️ Thanks for Playing!

Happy Coding and Have Fun!
```
