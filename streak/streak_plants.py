import tkinter as tk
import datetime
import os
import json
import pathlib

SAVE_FILE = pathlib.Path(__file__).parent / "streak_data.json"

class PlantTracker:
    # widget that visually represents a daily streak as a growing plant
    def __init__(self, parent, width=100, height=220):
        # colors
        self.colors = {
            "cream": "#F6E8B1",
            "sage": "#B0CC99",
            "brown": "#89725B",
            "lime": "#B7CA79",
            "dark_green": "#677E52",
        }
        self.parent = parent
        self.width = width
        self.height = height
        self.streak = 0
        self.last_date = None
        self._load_streak()

        # internal frame
        self.frame = tk.Frame(parent, bg=self.colors["cream"])

        # canvas that lives inside our frame
        self.canvas = tk.Canvas(self.frame, width=self.width, height=self.height,
                                bg=self.colors["cream"], highlightthickness=0)
        self.canvas.pack(padx=6, pady=6)

        self.update_growth()

    def _load_streak(self):
        try:
            if os.path.exists(SAVE_FILE):
                with open(SAVE_FILE, "r") as f:
                    data = json.load(f)
                    raw_streak = int(data.get("streak", 0))
                    self.last_date = data.get("last_date")

                    # clamp raw streak
                    if raw_streak > 20 or raw_streak < 0:
                        self.streak = 0
                    else:
                        self.streak = raw_streak

                    # validate against last_date
                    if self.last_date:
                        last_date_obj = datetime.date.fromisoformat(self.last_date)
                        delta_days = (datetime.date.today() - last_date_obj).days

                        if delta_days == 1 and self.streak == 20:
                            # yesterday was 20 -> today streak resets to 0
                            self.streak = 0
                        elif delta_days > 1 or delta_days < 0:
                            # missed days or future date -> reset
                            self.streak = 0
                    # save the updated streak if it changes
                    self._save_streak()
                    return self.streak
        except Exception as e:
            print("Error loading streak file:", e)
            self.streak = 0
            self.last_date = None

    def _save_streak(self):
        # save current streak and last activity date to JSON file
        try:
            with open(SAVE_FILE, "w") as f:
                json.dump({
                    "streak": int(self.streak),
                    "last_date": self.last_date
                }, f)
        except Exception as e:
            print("Error saving streak file:", e)

    def record_activity(self):
        today = datetime.date.today()
        if self.last_date:
            last_date_obj = datetime.date.fromisoformat(self.last_date)
            delta_days = (today - last_date_obj).days

            if delta_days == 0:
                # already played today
                return
            elif delta_days >= 1:
                self.streak += 1  # after pre-processing, increment normally
        else:
            self.streak = 1  # first activity ever

        self.last_date = today.isoformat()
        # cap at 20
        if self.streak > 20:
            self.streak = 20

        self._save_streak()
        self.update_growth()

    def update_growth(self):
        # redraws the plant on the canvas based on current streak value
        c = self.canvas
        if not c.winfo_exists():
            return
        c.delete("all")
        h = self.height

        # soil
        c.create_rectangle(10, h - 20, self.width - 10, h - 2, fill=self.colors["brown"], outline="")

        # stem
        stem_height = min(160, self.streak * 8)  # 8px/day, max 160 (20 days)
        cx = self.width // 2
        base_y = h - 20
        c.create_line(cx, base_y, cx, base_y - stem_height, width=4, fill=self.colors["dark_green"])

        # leaves every ~16px
        for i in range(0, stem_height, 16):
            y = base_y - i
            if (i // 16) % 2 == 0:
                c.create_oval(cx - 20, y - 5, cx, y + 5, fill=self.colors["dark_green"], outline="")
            else:
                c.create_oval(cx, y - 5, cx + 20, y + 5, fill=self.colors["dark_green"], outline="")

        # streak label
        c.create_text(40, 195 + 10, text=f"{self.streak}/20", fill=self.colors["dark_green"],
                      font=("Helvetica", 10, "bold"))



