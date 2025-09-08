import tkinter as tk
import datetime, os, json

SAVE_FILE = "streak_data.json"

class PlantTracker:
    def __init__(self, parent, width=100, height=220, streak_days=None):
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
        self.last_date = None
        self._load_streak()

        # internal frame (this is what you grid into your main layout)
        self.frame = tk.Frame(parent, bg="#F6E8B1")  # no pack here — parent will grid(self.frame,...)

        # canvas lives inside our frame and we pack it here (pack only inside our own frame)
        self.canvas = tk.Canvas(self.frame, width=self.width, height=self.height,
                                bg="#F6E8B1", highlightthickness=0)
        self.canvas.pack(padx=6, pady=6)


        self.streak = self._load_streak()

        # draw initial plant
        self.update_growth()

    @staticmethod
    def _load_streak():
        try:
            if os.path.exists(SAVE_FILE):
                with open(SAVE_FILE, "r") as f:
                    data = json.load(f)
                    return int(data.get("streak", 0))
        except Exception:
            pass
        return 0

    def _save_streak(self):
        try:
            with open(SAVE_FILE, "w") as f:
                json.dump({"streak": int(self.streak),
                           "last_date": datetime.date.today().isoformat()}, f)
        except Exception:
            pass

    def set_streak(self, new_value):
        try:
            self.streak = int(new_value)
        except Exception:
            self.streak = 0
        self._save_streak()
        self.update_growth()

    def update_growth(self):
        c = self.canvas
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
        # show streak number slightly below the soil
        self.canvas.create_text(40, 195 + 10, text=f"{self.streak}/20", fill=self.colors["dark_green"], font=("Helvetica", 10, "bold"))




