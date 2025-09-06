import tkinter as tk
import datetime
import os
import json

SAVE_FILE = "streak_data.json"


class PlantTracker:
    def __init__(self, parent, side="left", streak_days=None):
        self.parent = parent
        self.canvas = tk.Canvas(parent, width=80, height=200, bg="#F6E8B1", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.streak_days = streak_days or 0
        self.side = side
        self.last_date = None
        self.load_progress()
        self.update_growth()

    def load_progress(self):
        if os.path.exists(SAVE_FILE):
            try:
                with open(SAVE_FILE, "r") as f:
                    data = json.load(f)
                    self.streak = data.get("streak", 0)
                    self.last_date = datetime.date.fromisoformat(data.get("last_date"))
            except Exception:
                self.streak = 0
                self.last_date = None

        today = datetime.date.today()
        if self.last_date is None:
            self.last_date = today
            self.save_progress()
        else:
            if today > self.last_date:
                days_diff = (today - self.last_date).days
                if days_diff == 1:
                    self.streak += 1
                elif days_diff > 1:
                    # skipped a day -> streak does not grow further
                    pass
                self.last_date = today
                if self.streak >= 21:
                    self.streak = 0
                self.save_progress()

    def save_progress(self):
        """Save streak progress"""
        with open(SAVE_FILE, "w") as f:
            json.dump({
                "streak": self.streak,
                "last_date": self.last_date.isoformat()
            }, f)

    def update_growth(self):
        """Redraw the plant based on current streak"""
        self.canvas.delete("all")

        # draw soil
        self.canvas.create_rectangle(10, 180, 70, 190, fill="#654321", outline="")

        # base stem
        stem_height = min(160, self.streak * 8)  # grows 8px per day up to 20 days
        self.canvas.create_line(40, 180, 40, 180 - stem_height, width=4, fill="#228B22")

        # draw leaves every few streak steps
        for i in range(0, stem_height, 16):
            x = 40
            y = 180 - i
            if (i // 16) % 2 == 0:
                self.canvas.create_oval(x - 20, y - 5, x, y + 5, fill="#2E8B57", outline="")
            else:
                self.canvas.create_oval(x, y - 5, x + 20, y + 5, fill="#2E8B57", outline="")

        # show streak number
        self.canvas.create_text(40, 195, text=f"{self.streak}/20", fill="#333", font=("Helvetica", 10, "bold"))

