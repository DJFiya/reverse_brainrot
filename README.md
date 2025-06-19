# reverse_brainrot

**A Focus Tamagotchi — Python PyQt Prototype**

---

## Overview

**reverse_brainrot** is a fun and simple gamified productivity app built with Python and PyQt6. It encourages you to stay focused on the app window — your digital Tamagotchi gains experience (XP) and levels up the longer you keep the app in focus, and loses XP if you switch away. As your level and coins increase, you can unlock and upgrade badges that showcase your progress.

This project is currently in **prototype** stage, with core mechanics implemented and a clean, adaptable UI designed for easy future expansion.

---

## Key Features

- **Focus tracking:** Detects when the app window is active or inactive to reward or penalize the user.
- **XP and Leveling System:** Gain XP and level up while focused; lose XP when unfocused.
- **Coin accumulation:** Earn coins based on your current level over time.
- **Badge progression:** Unlock badges by spending coins; badges visually reflect your achievements.
- **Dynamic UI:** Simple yet visually clear badge display and status information.
- **Expandable:** Designed with future features in mind (more badges, rewards, art, animations).

---

## Technologies Used

- Python 3.8+
- PyQt6 for the user interface and event handling

---

## How It Works

- The app runs a timer that checks every second whether the app window is focused.
- While focused, XP and coins increase gradually.
- If you switch away from the app, penalty timers start decreasing your XP and potentially your level.
- Coins can be spent on badge upgrades, which display in the top-right corner.
- Badge tiers range from "None" to "Emerald," each with a coin cost.

---

## Usage

1. Run the app with Python:
   ```bash
   python reverse_brainrot.py
