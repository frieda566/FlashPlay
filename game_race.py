import tkinter as tk
from tkinter import messagebox
import random
import time
import io
import sys
from ascii_art_TNH import ascii_art


def get_ascii_art(name: str, placeholder: str = "") -> str:
    # generates ASCII art for a character - if generation fails, returns the placeholder
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
    # cleans out unwanted words from the ASCII art
    art = art.replace("meow", "").replace("woof", "")
    return art or placeholder


class RaceGame:
    def __init__(self, parent, flashcards):
        # initializes the race game window with UI components and game logic
        self.parent = parent
        self.flashcards = flashcards

        # exit early if no flashcards are provided
        if not self.flashcards:
            messagebox.showinfo(
                "No flashcards",
                "No flashcards found. Add some before playing.",
                parent=self.parent
            )
            return

        # window setup
        self.window = tk.Toplevel(self.parent)
        self.window.title("Flashcard Race Game")
        self.window.geometry("1200x800")
        self.window.configure(bg="#F6E8B1")

        # color palette for UI
        self.colors = {
            "cream": "#F7F6F0",
            "brown": "#8B5E3C",
            "sage": "#C8E3B0",
            "lime": "#A8D08D",
            "dark_green": "#4A6340"
        }

        # game UI and track parameters
        self.bg = "#F6E8B1"
        self.track_bg = "#E6F0D9"
        self.accent = "#C8E3B0"
        self.finish_color = "#6A8F56"
        self.char_color = "green"

        self.canvas_width = 1100
        self.canvas_height = 420
        self.start_x = 30
        self.finish_x = 920
        self.lane_y_player = 110
        self.lane_y_opponent = 280
        self.lane_half_height = 40

        # speed and timing parameters
        self.opponent_speed_tick = 70
        self.opponent_tick_ms = 8000  # Opponent moves every 8 seconds
        self.player_fast = 120
        self.player_slow = 60

        # game state
        self.running = True
        self.start_time = time.time()
        self.moves = 0
        self.correct_terms = []

        # load ASCII characters
        self.player_art = get_ascii_art("cat")
        self.opponent_art = get_ascii_art("dog")

        # build UI
        self._build_ui()

        # initial positions
        self.player_x = self.start_x
        self.opponent_x = self.start_x
        self.current_flashcard = None
        self.question_start_time = None
        self._opponent_after_id = None
        self._timeout_after_id = None

        # place characters on canvas
        self._place_characters()
        self.window.after(200, self.start_race)

    # -------------------- UI Methods -------------------- #
    def _build_ui(self):
        # sets up all UI components including canvas, labels and buttons

        # Title
        title_label = tk.Label(
            self.window,
            text="🏁Race Game",
            font=('Helvetica', 24, "bold"),
            bg=self.bg,
            fg=self.colors["dark_green"],
        )
        title_label.pack(pady=(20, 10))

        # top frame for racetrack
        top_frame = tk.Frame(self.window, bg=self.track_bg)
        top_frame.pack(fill="both", expand=False, padx=20, pady=(12, 6))

        # canvas for drawing racetrack and characters
        self.canvas = tk.Canvas(
            top_frame,
            width=self.canvas_width,
            height=self.canvas_height,
            bg=self.track_bg,
            highlightthickness=0,
        )
        self.canvas.pack(padx=20, pady=8)

        # draw start and finish lines
        self.canvas.create_text(
            self.start_x - 10, 20,
            text="START",
            anchor="w",
            font=("Helvetica", 10, "bold")
        )
        self.canvas.create_line(
            self.finish_x + 40, 0,
            self.finish_x + 40,
            self.canvas_height,
            fill=self.finish_color,
            width=4
        )

        # draw lane lines
        for cy in (self.lane_y_player, self.lane_y_opponent):
            top = cy - self.lane_half_height
            bot = cy + self.lane_half_height
            self.canvas.create_line(
                10, top, self.canvas_width - 10, top,
                fill='#c7c7c7', width=2, dash=(10, 8)
            )
            self.canvas.create_line(
                10, bot, self.canvas_width - 10, bot,
                fill='#c7c7c7', width=2, dash=(10, 8)
            )

        # bottom frame for flashcard and controls
        bottom_frame = tk.Frame(self.window, bg=self.bg)
        bottom_frame.pack(fill="both", expand=True, padx=40, pady=(6, 12))

        # flashcard term label
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

        # entry and submit button
        entry_frame = tk.Frame(bottom_frame, bg=self.bg)
        entry_frame.pack(pady=8)

        self.answer_entry = tk.Entry(entry_frame, font=("Helvetica", 20), width=30)
        self.answer_entry.pack(side="left", padx=(0, 10))
        self.answer_entry.bind("<Return>", lambda e: self.submit_answer())

        self.submit_btn = self.create_styled_button(
            entry_frame,
            "Submit",
            self.submit_answer,
            width=15,  # adjust width so it doesn’t look oversized
            is_primary=True,  # styled like "Play Again" and "Exit"
            side="left",
            padx=8,
            pady=0
        )

        # info label
        self.info_label = tk.Label(
            bottom_frame,
            text="Answer as fast as you can! (≤8s = faster)",
            font=("Helvetica", 12),
            bg=self.bg
        )
        self.info_label.pack(pady=(12, 0))

        # control buttons (New Game, Back to Menu)
        control_frame = tk.Frame(bottom_frame, bg=self.bg)
        control_frame.pack(pady=18)

        self.play_again_btn = self.create_styled_button(
            control_frame,
            "🔄New Game",
            self.reset_game, width=15,
            is_primary=True,
            side="left",
            padx=8,
            pady=0
        )

        self.back_btn = self.create_styled_button(
            control_frame, "← Back to Menu",
            self.back_to_menu,
            width=15,
            is_primary=True,
            side="left",
            padx=8,
            pady=0
        )

    def create_styled_button(self, parent, text, command, width=25, is_primary=True,
                             side="top", padx=0, pady=8):
        # creates a multi-layered styled button with shadow effect
        import tkinter.font as font

        # outer container frame
        button_container = tk.Frame(parent, bg=self.colors["cream"])
        button_container.pack(side=side, padx=padx, pady=pady)

        # shadow frame
        outer_frame = tk.Frame(button_container, bg=self.colors["brown"])
        outer_frame.pack()

        # inner frame
        bg_color = self.colors["sage"] if is_primary else self.colors["lime"]
        inner_frame = tk.Frame(outer_frame, bg=bg_color)
        inner_frame.pack(padx=3, pady=3)

        # actual button
        button_font = font.Font(family="Helvetica", size=12, weight="bold")
        btn = tk.Button(
            inner_frame,
            text=text,
            font=button_font,
            bg=bg_color,
            fg=self.colors["dark_green"],
            activebackground=self.colors["lime"] if is_primary else self.colors["sage"],
            activeforeground=self.colors["dark_green"],
            relief="flat",
            bd=0,
            width=width,
            pady=6,
            cursor="hand2",
            command=command
        )
        btn.pack(padx=4, pady=4)
        return btn

    # -------------------- Game Logic -------------------- #
    def _place_characters(self):
        # draws player and opponent ASCII art and labels on the canvas

        font_size = 9
        label_font_size = 14
        label_offset = 60  # distance below ASCII art

        # remove previous items if they exist
        for attr in ("player_item", "opponent_item", "player_label", "opponent_label"):
            if getattr(self, attr, None):
                self.canvas.delete(getattr(self, attr))

        # draw ASCII art for player and opponent
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

        # draw labels below each character with color scheme
        self.player_label = self.canvas.create_text(
            self.player_x,
            self.lane_y_player + label_offset,
            text="You",
            anchor="w",
            font=("Helvetica", label_font_size, "bold"),
            fill=self.char_color  # same green as ASCII art
        )
        self.opponent_label = self.canvas.create_text(
            self.opponent_x,
            self.lane_y_opponent + label_offset,
            text="Your Opponent",
            anchor="w",
            font=("Helvetica", label_font_size, "bold"),
            fill=self.finish_color  # soft earthy green to match scheme
        )

        self.canvas.update()

    def start_race(self):
        # resets positions and starts the race with first flashcard
        self.running = True
        self.player_x = self.start_x
        self.opponent_x = self.start_x
        self._place_characters()
        self.next_flashcard()
        self._schedule_opponent_move()

    def next_flashcard(self):
        # picks the next flashcard, avoiding repetition of the last one

        if not self.running:
            return

        # cancel previous timeout
        if self._timeout_after_id is not None:
            self.window.after_cancel(self._timeout_after_id)
            self._timeout_after_id = None

        # pick a new flashcard different from previous
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

        # schedule timeout penalty after 8 seconds
        self._timeout_after_id = self.window.after(8000, self._timeout_answer_penalty)

    def _timeout_answer_penalty(self):
        # applies a small advance penalty if player does not answer in time

        if not self.running:
            return
        if self.answer_entry.get().strip() == "":
            self.info_label.config(
                text=f"Time's up! Small advance penalty applied. Correct: {self.current_flashcard[2]}"
            )
            self._animate_move(self.player_item, self.player_x, self.player_x + self.player_slow)
            self.player_x += self.player_slow

    def submit_answer(self):
        # handles answer submission and moves the player if correct
        if not self.running or not self.current_flashcard:
            return

        # cancel timeout
        if self._timeout_after_id is not None:
            self.window.after_cancel(self._timeout_after_id)
            self._timeout_after_id = None

        user = self.answer_entry.get().strip()
        correct = self.current_flashcard[2].strip()

        if not user:
            messagebox.showinfo(
                "No answer",
                "Please enter a translation (or Close to stop).",
                parent=self.window
            )
            return

        # track move
        self.moves += 1

        self.answer_entry.config(state="disabled")
        elapsed = time.time() - self.question_start_time

        # correct answer
        if user.lower() == correct.lower():
            # track correct flashcard before next_flashcard()
            self.correct_terms.append(self.current_flashcard[0])

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

        # show next flashcard immediately after answer
        self.next_flashcard()

    def _animate_move(self, item, from_x, to_x, duration_ms=300):
        # animates the movement of a canvas item smoothly
        steps = max(1, int(duration_ms // 20))
        dx = (to_x - from_x) / steps
        cur_x = from_x

        def step(i):
            nonlocal cur_x
            # if the canvas or window has been destroyed, stop animation
            if not self.running or not self.canvas.winfo_exists():
                return

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
        # schedules periodic movement of the opponent
        if not self.running:
            return
        self._opponent_move_once()
        self._opponent_after_id = self.window.after(self.opponent_tick_ms, self._schedule_opponent_move)

    def _opponent_move_once(self):
        # moves the opponent a single step forward
        new_x = self.opponent_x + self.opponent_speed_tick
        self._animate_move(self.opponent_item, self.opponent_x, new_x, duration_ms=250)
        self.opponent_x = new_x
        self._check_winner_or_continue()

    def _check_winner_or_continue(self):
        # checks if player or opponent has crossed the finish line
        margin = 30
        if self.player_x + margin >= self.finish_x:
            self.running = False
            self._end_game("You win! 🎉")
            return
        elif self.opponent_x + margin >= self.finish_x:
            self.running = False
            self._end_game("Opponent wins. Try again!")
            return

    def _game_over(self):
        # displays final stats in a message box
        elapsed = int(time.time() - self.start_time)
        stats = (
            "🎉 Congratulations! 🎉\n\n"
            "You completed the memory game!\n\n"
            "📊 Your Stats:\n"
            f"• Moves: {self.moves}\n"
            f"• Time: {elapsed}s\n"
            f"• Correct Terms: {len(self.correct_terms)}"
        )
        messagebox.showinfo("Game Over", stats, parent=self.window)

    def _end_game(self, message):
        # stops the game and shows a game over message
        if self._opponent_after_id:
            try:
                self.window.after_cancel(self._opponent_after_id)
            except Exception:
                pass
            self._opponent_after_id = None

        messagebox.showinfo("Race Over", message, parent=self.window)
        self.play_again_btn.config(state="normal")
        self.answer_entry.config(state="disabled")

        # call game over stats
        self._game_over()

    def reset_game(self):
        # resets the game to initial state for a new race
        self.play_again_btn.config(state="disabled")
        self.answer_entry.config(state="normal")
        self.info_label.config(text="Answer as fast as you can! (≤8s = faster)")
        self.player_x = self.start_x
        self.opponent_x = self.start_x
        self._place_characters()
        self.window.after(300, self.start_race)

    def back_to_menu(self):
        # returns to main menu

        # cancel timers (like in close)
        if hasattr(self, "_opponent_after_id") and self._opponent_after_id:
            try:
                self.window.after_cancel(self._opponent_after_id)
            except Exception:
                pass
            self._opponent_after_id = None

        if hasattr(self, "_timeout_after_id") and self._timeout_after_id:
            try:
                self.window.after_cancel(self._timeout_after_id)
            except Exception:
                pass
            self._timeout_after_id = None

        # show the parent window (main menu) again
        if self.parent is not None:
            try:
                self.parent.deiconify()
            except Exception:
                pass

        # close this game window
        self.window.destroy()


