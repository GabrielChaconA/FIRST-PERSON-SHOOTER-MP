# SHOOTER-3D

An action-packed 3D first-person shooter (FPS) survival game built in Python using the **Ursina Engine**. Battle against waves of iconic creatures (Creepers, Skeletons, Endermen, Wardens, and Withers) in a modular codebase.


## 🚀 Installation & Requirements

### Prerequisites
* **Python 3.8 or higher** installed on your system.

### Dependencies
Install the required packages by running:

```bash
pip install -r requirements.txt
```

---

## 🎮 How to Play

Run the main script from the root directory of the project:

```bash
python src/main.py
```

### Controls
* **W, A, S, D**: Movement
* **SHIFT**: Sprint (consumes stamina)
* **C**: Slide (quick slide on the ground)
* **LEFT CLICK**: Shoot
* **ESC**: Quit game immediately

---

## ⚔️ Game Modes
1. **ROUNDS (Normal)**:
   - Survive consecutive waves of enemies with scaling difficulty.
   - Early rounds spawn basic enemies, while higher rounds introduce elite monsters.
2. **HARD**:
   - Spawns all elite monsters (including Withers and Wardens) right from the start in high quantities.

---

## 📁 Project Structure

The codebase is organized modularly for easy extension:

```text
SHOOTER-3D/
│
├── Capturas/             # Game screenshots
├── Modelos_3d/           # 3D models and textures (.glb, .obj, .mtl)
├── src/
│   ├── main.py           # Application entry point
│   └── juego/
│       ├── logica.py     # Main loop coordinator, damage, collisions, and state
│       ├── entidades/    # Player, weapon, and enemy entity classes
│       ├── escena/       # Window, level map (laundry.glb), and lighting setup
│       ├── interfaz/     # Main menu and in-game HUD (health, stamina, ammo)
│       └── sistemas/     # Movement limits, wave spawning, ammo, and firing systems
│
├── .gitignore            # Git exclusion rules
└── requirements.txt      # Python dependencies list
```
---

## 📸 Screenshots

### Main Menu
![Main Menu](Capturas/Menu.png)

### Gameplay - Round 1
![Gameplay Round 1](Capturas/Ronda%201.png)

### Ammo Box Collection
![Ammo Boxes](Capturas/Municiones.png)

### Hard Mode Chaos
![Hard Mode](Capturas/Ronda%20dificil.png)

---
