import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout, QPushButton,
    QHBoxLayout, QProgressBar
)
from PyQt6.QtCore import QTimer, Qt, QEvent
from PyQt6.QtGui import QFont

DEBUG = True

class GameConfig:
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

    XP_GAIN = 5
    PENALTY_XP_LOSS = 10
    PENALTY_RESET_TICKS = 5

    PET_STAGES = [
        (1, "🐣"),    # Baby
        (3, "🐥"),    # Hatchling
        (5, "🐤"),    # Chick
        (7, "🦜"),    # Parrot
        (10, "🐉")    # Dragon
    ]


class ReverseBrainrotApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("reverse_brainrot")
        self.setGeometry(300, 300, 400, 450)
        self.setStyleSheet("background-color: #121212; color: #eeeeee;")

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

        self.badge_label = QLabel(GameConfig.BADGE_TIERS[self.badge_index][0])
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

        self.pet_label = QLabel()
        self.pet_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.pet_label.setStyleSheet("font-size: 100px;")
        main_layout.addWidget(self.pet_label)

        self.status_label = QLabel()
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setStyleSheet("font-size: 16px;")
        main_layout.addWidget(self.status_label)

        self.xp_bar = QProgressBar()
        self.xp_bar.setStyleSheet("""
            QProgressBar {
                background-color: #333;
                border: 1px solid #666;
                border-radius: 6px;
                height: 18px;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #50c878;
            }
        """)
        main_layout.addWidget(self.xp_bar)

        self.reward_button = QPushButton("Claim Reward")
        self.reward_button.setEnabled(False)
        self.reward_button.clicked.connect(self.claim_reward)
        main_layout.addWidget(self.reward_button)

        self.setLayout(main_layout)
        self.update_status()
        self.update_pet_stage()

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
            self.xp += GameConfig.XP_GAIN
            self.coins += self.level
            self.update_level()
            self.check_reward_availability()
            self.update_status()

    def penalty_tick(self):
        if not self.focused:
            if DEBUG:
                print("unfocused")
            self.penalty_accumulated += 1
            self.xp = max(0, self.xp - GameConfig.PENALTY_XP_LOSS)
            if self.penalty_accumulated >= GameConfig.PENALTY_RESET_TICKS:
                self.penalty_accumulated = 0
            self.update_level()
            self.check_reward_availability()
            self.update_status()

    def update_level(self):
        new_level = 1
        for lvl, thresh in reversed(GameConfig.LEVEL_THRESHOLDS):
            if self.xp >= thresh:
                new_level = lvl
                break

        if new_level != self.level:
            if DEBUG:
                print(f"Level changed: {self.level} -> {new_level}")
            self.level = new_level
            self.update_pet_stage()

    def check_reward_availability(self):
        next_tier = self.badge_index + 1
        if next_tier < len(GameConfig.BADGE_TIERS):
            cost = GameConfig.BADGE_TIERS[next_tier][1]
            tier_name = GameConfig.BADGE_TIERS[next_tier][0]
            self.reward_button.setEnabled(self.coins >= cost)
            self.reward_button.setText(f"Claim {tier_name} Badge ({cost} coins)")
        else:
            self.reward_button.setEnabled(False)
            self.reward_button.setText("Max tier reached")

    def claim_reward(self):
        next_tier = self.badge_index + 1
        if next_tier >= len(GameConfig.BADGE_TIERS):
            if DEBUG:
                print("No more tiers available.")
            self.reward_button.setEnabled(False)
            return

        cost = GameConfig.BADGE_TIERS[next_tier][1]
        if self.coins >= cost:
            self.coins -= cost
            self.badge_index = next_tier
            self.update_badge()
            self.reward_button.setEnabled(False)
            self.update_status()
            if DEBUG:
                print(f"Upgraded to {GameConfig.BADGE_TIERS[self.badge_index][0]} badge.")

    def update_badge(self):
        badge_name = GameConfig.BADGE_TIERS[self.badge_index][0]
        colors = {
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

    def update_pet_stage(self):
        for level_req, emoji in reversed(GameConfig.PET_STAGES):
            if self.level >= level_req:
                self.pet_label.setText(emoji)
                break

    def update_status(self):
        self.status_label.setText(f"Level: {self.level} | XP: {self.xp} | Coins: {self.coins}")
        self.update_xp_bar()

    def update_xp_bar(self):
        current = self.xp
        for i, (level, threshold) in enumerate(GameConfig.LEVEL_THRESHOLDS):
            if level == self.level:
                current_level_thresh = threshold
                next_level_thresh = (
                    GameConfig.LEVEL_THRESHOLDS[i + 1][1]
                    if i + 1 < len(GameConfig.LEVEL_THRESHOLDS)
                    else threshold + 100
                )
                break
        self.xp_bar.setRange(0, next_level_thresh - current_level_thresh)
        self.xp_bar.setValue(current - current_level_thresh)

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
    app.setFont(QFont("Segoe UI", 10))
    window = ReverseBrainrotApp()
    window.show()
    sys.exit(app.exec())
