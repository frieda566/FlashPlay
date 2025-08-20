# game_race.py
import tkinter as tk
from tkinter import messagebox
import random
import time
import io
import sys
from ascii_art_TNH import ascii_art

def get_ascii_art(name: str, placeholder: str = "") -> str:
    buf = io.StringIO()
    # Redirect stdout to buffer
    old = sys.stdout
    sys.stdout = buf
    try:
        ascii_art(name)
    except Exception:
        art = placeholder
    else:
        art = buf.getvalue()
    finally:
        sys.stdout = old
    return art or placeholder

class RaceGame:
    def __init__(self, parent, flashcards):
        self.parent = parent
        self.flashcards = flashcards or []
        if not self.flashcards:
            messagebox.showinfo("No flashcards", "No flashcards found. Add some before playing.", parent=self.parent)
            return

        self.window = tk.Toplevel(self.parent)
        self.window.title("Flashcard Race Game")
        self.window.geometry("1200x800")
        self.window.configure(bg="#F7F6F0")

        self.bg = "#F7F6F0"
        self.track_bg = "#E6F0D9"
        self.accent = "#C8E3B0"
        self.finish_color = "#6A8F56"
        self.char_color = "red"

        self.canvas_width = 1100
        self.canvas_height = 420
        self.start_x = 30
        self.finish_x = 920
        self.lane_y_player = 110
        self.lane_y_opponent = 280
        self.lane_half_height = 40

        self.opponent_speed_tick = 70
        self.opponent_tick_ms = 8000  # Opponent moves every 8 seconds
        self.player_fast = 120
        self.player_slow = 60
        self.running = True

        self.player_art = get_ascii_art("cat")
        self.opponent_art = get_ascii_art("dog")

        self._build_ui()

        self.player_x = self.start_x
        self.opponent_x = self.start_x
        self.current_flashcard = None
        self.question_start_time = None
        self._opponent_after_id = None
        self._timeout_after_id = None

        self._place_characters()
        self.window.after(200, self.start_race)

    def _build_ui(self):
        top_frame = tk.Frame(self.window, bg=self.track_bg)
        top_frame.pack(fill="both", expand=False, padx=20, pady=(12, 6))

        self.canvas = tk.Canvas(
            top_frame,
            width=self.canvas_width,
            height=self.canvas_height,
            bg=self.track_bg,
            highlightthickness=0,
        )
        self.canvas.pack(padx=20, pady=8)

        self.canvas.create_text(self.start_x - 10, 20, text="START", anchor="w", font=("Helvetica", 10, "bold"))
        self.canvas.create_line(self.finish_x + 40, 0, self.finish_x + 40, self.canvas_height, fill=self.finish_color, width=4)

        for cy in (self.lane_y_player, self.lane_y_opponent):
            top = cy - self.lane_half_height
            bot = cy + self.lane_half_height
            self.canvas.create_line(
                10, top, self.canvas_width - 10, top,
                fill='#c7c7c7', width=2, dash=(10,8)
            )
            self.canvas.create_line(
                10, bot, self.canvas_width - 10, bot,
                fill='#c7c7c7', width=2, dash=(10,8)
            )

        bottom_frame = tk.Frame(self.window, bg=self.bg)
        bottom_frame.pack(fill="both", expand=True, padx=40, pady=(6, 12))

        self.term_label = tk.Label(
            bottom_frame,
            text="",
            font=("Helvetica", 32, "bold"),
            bg=self.bg,
            fg="#4a6340",
            wraplength=1000,
            justify="center"
        )
        self.term_label.pack(pady=(20, 10))

        entry_frame = tk.Frame(bottom_frame, bg=self.bg)
        entry_frame.pack(pady=8)

        self.answer_entry = tk.Entry(entry_frame, font=("Helvetica", 20), width=30)
        self.answer_entry.pack(side="left", padx=(0, 10))
        self.answer_entry.bind("<Return>", lambda e: self.submit_answer())

        submit_btn = tk.Button(entry_frame, text="Submit", command=self.submit_answer, font=("Helvetica", 14, 'bold'), bg=self.accent)
        submit_btn.pack(side="left")

        self.info_label = tk.Label(bottom_frame, text="Answer as fast as you can! (≤8s = faster)", font=("Helvetica", 12), bg=self.bg)
        self.info_label.pack(pady=(12, 0))

        control_frame = tk.Frame(bottom_frame, bg=self.bg)
        control_frame.pack(pady=18)

        self.play_again_btn = tk.Button(control_frame, text="Play Again", command=self.reset_game, state="disabled", font=('Helvetica', 14, 'bold'), bg=self.accent, fg='white', relief='flat', cursor='hand2', padx=10, pady=6)
        self.play_again_btn.pack(side="left", padx=8)

        close_btn = tk.Button(control_frame, text="Exit", command=self.close, font=('Helvetica', 14, 'bold'), bg=self.accent, fg='white', relief='flat', cursor='hand2', padx=12, pady=6)
        close_btn.pack(side="left", padx=10)

    def _place_characters(self):
        font_size = 9
        if getattr(self, "player_item", None):
            self.canvas.delete(self.player_item)
        if getattr(self, "opponent_item", None):
            self.canvas.delete(self.opponent_item)

        self.player_item = self.canvas.create_text(
            self.player_x,
            self.lane_y_player,
            text=self.player_art,
            anchor="w",
            font=("Courier", font_size),
            fill=self.char_color,
        )
        self.opponent_item = self.canvas.create_text(
            self.opponent_x,
            self.lane_y_opponent,
            text=self.opponent_art,
            anchor="w",
            font=("Courier", font_size),
            fill=self.char_color,
        )

        self.canvas.update()

    def start_race(self):
        self.running = True
        self.player_x = self.start_x
        self.opponent_x = self.start_x
        self._place_characters()
        self.next_flashcard()
        self._schedule_opponent_move()

    def next_flashcard(self):
        if not self.running:
            return

        if self._timeout_after_id is not None:
            self.window.after_cancel(self._timeout_after_id)
            self._timeout_after_id = None

        #Choose a different flashcard than last one
        prev_card = self.current_flashcard
        while True:
            card = random.choice(self.flashcards)
            if card != prev_card:
                break
        self.current_flashcard = card

        term = self.current_flashcard[1]
        self.term_label.config(text=f"{term}")

        self.answer_entry.config(state="normal")
        self.answer_entry.delete(0, tk.END)
        self.answer_entry.focus_set()
        self.question_start_time = time.time()

        self._timeout_after_id = self.window.after(8000, self._timeout_answer_penalty)

    def _timeout_answer_penalty(self):
        if not self.running:
            return
        if self.answer_entry.get().strip() == "":
            self.info_label.config(text=f"Time's up! Small advance penalty applied. Correct: {self.current_flashcard[2]}")
            self._animate_move(self.player_item, self.player_x, self.player_x + self.player_slow)
            self.player_x += self.player_slow
            # Do not advance flashcard, user can answer anytime

    def submit_answer(self):
        if not self.running or not self.current_flashcard:
            return

        if self._timeout_after_id is not None:
            self.window.after_cancel(self._timeout_after_id)
            self._timeout_after_id = None

        user = self.answer_entry.get().strip()
        correct = self.current_flashcard[2].strip()

        if user == "":
            messagebox.showinfo("No answer", "Please enter a translation (or Close to stop).", parent=self.window)
            return

        self.answer_entry.config(state="disabled")
        elapsed = time.time() - self.question_start_time

        if user.lower() == correct.lower():
            if elapsed <= 8:
                move_px = self.player_fast
                self.info_label.config(text=f"Correct! Quick answer (+{move_px}px).")
            else:
                move_px = self.player_slow
                self.info_label.config(text=f"Correct, but slow (+{move_px}px).")
            self._animate_move(self.player_item, self.player_x, self.player_x + move_px)
            self.player_x += move_px
        else:
            self.info_label.config(text=f"Incorrect. Correct answer: {correct}")

        self._check_winner_or_continue()

        # Show next flashcard immediately after answer
        self.next_flashcard()

    def _animate_move(self, item, from_x, to_x, duration_ms=300):
        steps = max(1, int(duration_ms // 20))
        dx = (to_x - from_x) / steps
        cur_x = from_x

        def step(i):
            nonlocal cur_x
            if i >= steps:
                self.canvas.coords(item, to_x, self.canvas.coords(item)[1])
                self.canvas.update()
                return
            cur_x += dx
            self.canvas.coords(item, cur_x, self.canvas.coords(item)[1])
            self.canvas.update()
            self.window.after(20, lambda: step(i + 1))

        step(0)

    def _schedule_opponent_move(self):
        if not self.running:
            return
        self._opponent_move_once()
        self._opponent_after_id = self.window.after(self.opponent_tick_ms, self._schedule_opponent_move)

    def _opponent_move_once(self):
        new_x = self.opponent_x + self.opponent_speed_tick
        self._animate_move(self.opponent_item, self.opponent_x, new_x, duration_ms=250)
        self.opponent_x = new_x
        self._check_winner_or_continue()

    def _check_winner_or_continue(self):
        margin = 30
        if self.player_x + margin >= self.finish_x:
            self.running = False
            self._end_game("You win! 🎉")
            return
        if self.opponent_x + margin >= self.finish_x:
            self.running = False
            self._end_game("Opponent (Dragon) wins. Try again!")
            return

    def _end_game(self, message):
        if self._opponent_after_id:
            try:
                self.window.after_cancel(self._opponent_after_id)
            except Exception:
                pass
            self._opponent_after_id = None

        messagebox.showinfo("Race Over", message, parent=self.window)
        self.play_again_btn.config(state="normal")
        self.answer_entry.config(state="disabled")

    def reset_game(self):
        self.play_again_btn.config(state="disabled")
        self.answer_entry.config(state="normal")
        self.info_label.config(text="Answer as fast as you can! (≤8s = faster)")
        self.player_x = self.start_x
        self.opponent_x = self.start_x
        self._place_characters()
        self.window.after(300, self.start_race)

    def close(self):
        if self._opponent_after_id:
            try:
                self.window.after_cancel(self._opponent_after_id)
            except Exception:
                pass
        self.window.destroy()
