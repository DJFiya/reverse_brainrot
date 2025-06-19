import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QPushButton, QHBoxLayout
from PyQt6.QtCore import QTimer, Qt, QEvent

DEBUG = True

class ReverseBrainrotApp(QWidget):
    BADGE_TIERS = [
        ("None", 0),
        ("Copper", 10),
        ("Bronze", 25),
        ("Silver", 50),
        ("Gold", 100),
        ("Platinum", 250),
        ("Diamond", 500),
        ("Emerald", 1000)
    ]

    # XP thresholds for levels
    LEVEL_THRESHOLDS = [
        (1, 0),
        (2, 50),
        (3, 120),
        (4, 210),
        (5, 320),
        (6, 460),
        (7, 630),
        (8, 830),
        (9, 1060),
        (10, 1320),
    ]

    def __init__(self):
        super().__init__()

        self.setWindowTitle("reverse_brainrot")
        self.setGeometry(300, 300, 350, 400)

        self.focused = True
        self.coins = 0
        self.xp = 0
        self.level = 1
        self.penalty_accumulated = 0
        self.badge_index = 0

        self.init_ui()
        self.init_timers()

    def init_ui(self):
        main_layout = QVBoxLayout()
        top_bar = QHBoxLayout()

        top_bar.addStretch()

        self.badge_label = QLabel(self.BADGE_TIERS[self.badge_index][0])
        self.badge_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTop)
        self.badge_label.setStyleSheet("""
            font-weight: bold;
            font-size: 14px;
            padding: 6px 12px;
            border-radius: 8px;
            background-color: #ccc;
            color: #333;
            min-width: 80px;
        """)
        top_bar.addWidget(self.badge_label)

        main_layout.addLayout(top_bar)

        self.pet_label = QLabel("🐣")  # Placeholder Tamagotchi emoji
        self.pet_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.pet_label.setStyleSheet("font-size: 100px;")

        self.status_label = QLabel(f"Level: {self.level} | XP: {self.xp} | Coins: {self.coins}")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setStyleSheet("font-size: 16px;")

        self.reward_button = QPushButton("Claim Reward")
        self.reward_button.setEnabled(False)
        self.reward_button.clicked.connect(self.claim_reward)

        main_layout.addWidget(self.pet_label)
        main_layout.addWidget(self.status_label)
        main_layout.addWidget(self.reward_button)

        self.setLayout(main_layout)

    def init_timers(self):
        self.focus_timer = QTimer()
        self.focus_timer.timeout.connect(self.focus_tick)
        self.focus_timer.start(1000)

        self.penalty_timer = QTimer()
        self.penalty_timer.timeout.connect(self.penalty_tick)
        self.penalty_timer.setInterval(1000)

    def focus_tick(self):
        if self.focused:
            if DEBUG:
                print("focused")
            # Gain XP and coins proportional to current level
            self.xp += 5
            self.coins += self.level
            self.update_level()
            self.check_reward_availability()
            self.update_status()

    def penalty_tick(self):
        if not self.focused:
            if DEBUG:
                print("unfocused")
            self.penalty_accumulated += 1
            # Lose XP on penalty ticks
            self.xp = max(0, self.xp - 10)
            if self.penalty_accumulated >= 5:
                self.penalty_accumulated = 0
            self.update_level()
            self.check_reward_availability()
            self.update_status()

    def update_level(self):
        # Find highest level where XP >= threshold
        new_level = 1
        for lvl, thresh in reversed(self.LEVEL_THRESHOLDS):
            if self.xp >= thresh:
                new_level = lvl
                break

        if new_level != self.level:
            if DEBUG:
                print(f"Level changed: {self.level} -> {new_level}")
            self.level = new_level

    def check_reward_availability(self):
        next_tier = self.badge_index + 1
        if next_tier < len(self.BADGE_TIERS):
            cost = self.BADGE_TIERS[next_tier][1]
            tier_name = self.BADGE_TIERS[next_tier][0]
            if self.coins >= cost:
                self.reward_button.setEnabled(True)
            else:
                self.reward_button.setEnabled(False)
            self.reward_button.setText(f"Claim {tier_name} Badge ({cost} coins)")
        else:
            self.reward_button.setEnabled(False)
            self.reward_button.setText("Max tier reached")

    def claim_reward(self):
        next_tier = self.badge_index + 1
        if next_tier >= len(self.BADGE_TIERS):
            if DEBUG:
                print("No more tiers available.")
            self.reward_button.setEnabled(False)
            return

        cost = self.BADGE_TIERS[next_tier][1]
        if self.coins >= cost:
            self.coins -= cost
            self.badge_index = next_tier
            self.update_badge()
            self.reward_button.setEnabled(False)
            self.update_status()
            if DEBUG:
                print(f"Upgraded to {self.BADGE_TIERS[self.badge_index][0]} badge.")

    def update_badge(self):
        badge_name = self.BADGE_TIERS[self.badge_index][0]
        colors = { # Temporarily stored here, will be more dynamic later, this is prototype.
            "None": "#ccc",
            "Copper": "#b87333",
            "Bronze": "#cd7f32",
            "Silver": "#c0c0c0",
            "Gold": "#ffd700",
            "Platinum": "#e5e4e2",
            "Diamond": "#b9f2ff",
            "Emerald": "#50c878"
        }
        color = colors.get(badge_name, "#ccc")
        self.badge_label.setText(badge_name)
        self.badge_label.setStyleSheet(f"""
            font-weight: bold;
            font-size: 14px;
            padding: 6px 12px;
            border-radius: 8px;
            background-color: {color};
            color: #222;
            min-width: 80px;
        """)

    def update_status(self):
        self.status_label.setText(f"Level: {self.level} | XP: {self.xp} | Coins: {self.coins}")

    def changeEvent(self, event):
        if event.type() == QEvent.Type.ActivationChange:
            if self.isActiveWindow():
                if DEBUG:
                    print("Window activated (focused)")
                self.focused = True
                self.penalty_timer.stop()
            else:
                if DEBUG:
                    print("Window deactivated (unfocused)")
                self.focused = False
                self.penalty_timer.start()
            self.update_status()
        super().changeEvent(event)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ReverseBrainrotApp()
    window.show()
    sys.exit(app.exec())
