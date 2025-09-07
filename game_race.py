import tkinter as tk
from tkinter import messagebox
from tkinter import font
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
    def __init__(self, root, parent, flashcards, on_exit=None, on_streak=None):
        # initializes the race game window with UI components and game logic
        self.root = root
        self.parent = parent
        self.flashcards = flashcards or []
        self.on_exit = on_exit
        self.on_streak = on_streak

        # remember original root state to restore after exit
        self._original_bg = self.root.cget("bg")
        self._original_title = self.root.title()

        # exit early if no flashcards are provided
        if not self.flashcards:
            messagebox.showinfo(
                "No flashcards",
                "No flashcards found. Add some before playing.",
                parent=self.parent
            )
            return

        # Theme
        self.colors = {
            "cream": "#F7F6F0",
            "brown": "#8B5E3C",
            "sage": "#C8E3B0",
            "lime": "#A8D08D",
            "dark_green": "#4A6340"
        }

        # Track/ UI colors derived from palette
        self.bg = self.colors["cream"]
        self.track_bg = "#E6F0D9"
        self.accent = "#C8E3B0"
        self.finish_color = "#6A8F56"
        self.char_color = self.colors["dark_green"]

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
        self.running = False
        self.start_time = time.time()
        self.moves = 0
        self.time_elapsed = 0
        self.correct_terms = []
        self.current_flashcard = None
        self.question_start_time = None

        # after() bookkeeping
        self._after_jobs = set()
        self._opponent_after_id = None
        self._timeout_after_id = None

        # load ASCII characters
        self.player_art = get_ascii_art("cat")
        self.opponent_art = get_ascii_art("dog")

        # container: only child of root while game is active (use pack here)
        self.container = tk.Frame(self.root, bg=self.colors["cream"])  # isolate layout
        self.container.pack(fill="both", expand=True)

        # build UI and start
        self._build_ui()
        # ensure the container is on top and realized before drawing
        self.container.update_idletasks()
        self.container.tkraise()
        # delay placing characters and start_race so canvas is mapped
        self._after(100, self._place_characters)
        self._after(250, self.start_race)

    # -------------------------- layout -----------------------------------
    def _build_ui(self):
        # sets up all UI components including canvas, labels and buttons
        for w in self.container.winfo_children():
            w.destroy()
        self.root.title("FlashPlay - Race Game")
        self.root.configure(bg=self.colors["cream"])

        # grid inside container; root uses pack -> no pack/ grid mixing
        self.container.grid_rowconfigure(2, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        header = tk.Frame(self.container, bg=self.colors["cream"], pady=12)
        header.grid(row=0, column=0, sticky="ew")
        title_font = font.Font(family="Helvetica", size=24, weight="bold")
        # Title
        tk.Label(
            header,
            text="🏁Race Game",
            font=title_font,
            bg=self.colors["cream"],
            fg=self.colors["dark_green"],
        ).pack()

        # info bar (moves & timer)
        info = tk.Frame(self.container, bg=self.colors["cream"])
        info.grid(row=1, column=0, sticky="ew", pady=(0, 6))
        info_font = font.Font(family="Helvetica", size=12)
        self.moves_label = tk.Label(
            info, text="Moves: 0", font=info_font, bg=self.colors["cream"], fg=self.colors["dark_green"]
        )
        self.time_label = tk.Label(
            info, text="Time: 0s", font=info_font, bg=self.colors["cream"], fg=self.colors["dark_green"]
        )
        self.moves_label.pack(side="left", padx=16)
        self.time_label.pack(side="right", padx=16)

        # game frame (racetrack)
        self.game_frame = tk.Frame(self.container, bg=self.track_bg)
        self.game_frame.grid(row=2, column=0, sticky="nsew", padx=12, pady=12)

        self.canvas = tk.Canvas(
            self.game_frame,
            width=self.canvas_width,
            height=self.canvas_height,
            bg=self.track_bg,
            highlightthickness=0,
        )
        self.canvas.pack(fill="both", expand=True, padx=10, pady=10)

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

        # term label (row 3)
        self.term_label = tk.Label(
            self.container,
            text="",
            font=("Helvetica", 32, "bold"),
            bg=self.colors["cream"],
            fg="#4a6340",
            wraplength=1000,
            justify="center",
        )
        self.term_label.grid(row=3, column=0, pady=(6, 6))

        # entry + submit (row 4)
        entry_frame = tk.Frame(self.container, bg=self.colors["cream"])
        entry_frame.grid(row=4, column=0, pady=(0, 12))
        self.answer_entry = tk.Entry(entry_frame, font=("Helvetica", 20), width=30)
        self.answer_entry.pack(side="left", padx=(0, 10))
        self.answer_entry.bind("<Return>", lambda e: self.submit_answer())
        self.submit_btn = self.create_styled_button(
            entry_frame, "Submit", self.submit_answer, width=15, is_primary=True, side="left", padx=8, pady=0
        )

        # info label
        self.info_label = tk.Label(
            self.container,
            text="Answer as fast as you can! (≤8s = faster)",
            font=("Helvetica", 12),
            bg=self.colors["cream"],
            fg=self.colors["dark_green"],
        )
        self.info_label.grid(row=5, column=0, pady=(0, 6))

        # controls (row 6)
        self.control_frame = tk.Frame(self.container, bg=self.colors["cream"])  # row 3
        self.control_frame.grid(row=6, column=0, sticky="ew", pady=(0, 12))
        self._build_controls()
        self.root.update_idletasks()
        self.root.minsize(self.canvas_width + 100, self.canvas_height + 300)

    def _build_controls(self):
        for w in self.control_frame.winfo_children():
            w.destroy()
        button_font = font.Font(family="Helvetica", size=11, weight="bold")

        # Create a container frame to hold both buttons
        button_container = tk.Frame(self.control_frame, bg=self.colors["cream"])
        button_container.pack(expand=True)

        def card_button(parent, text, command):
            outer = tk.Frame(parent, bg=self.colors["brown"])
            inner = tk.Frame(outer, bg=self.colors["sage"])
            btn = tk.Button(
                inner,
                text=text,
                font=button_font,
                bg=self.colors["sage"],
                fg=self.colors["dark_green"],
                activebackground=self.colors["lime"],
                activeforeground=self.colors["dark_green"],
                relief="flat",
                bd=0,
                padx=18,
                pady=10,
                cursor="hand2",
                command=command,
            )
            btn.pack(expand=True, fill="both", padx=2, pady=2)
            inner.pack(expand=True, fill="both", padx=3, pady=3)
            outer.pack(side="left", padx=10)

            def on_enter(_):
                btn.configure(bg=self.colors["lime"])
                inner.configure(bg=self.colors["lime"])

            def on_leave(_):
                btn.configure(bg=self.colors["sage"])
                inner.configure(bg=self.colors["sage"])

            btn.bind("<Enter>", on_enter)
            btn.bind("<Leave>", on_leave)
            return btn

        self.play_again_btn = card_button(button_container, "🔄 New Game", self.reset_game)
        card_button(button_container, "← Back to Menu", self.return_to_main_menu)

    def create_styled_button(self, parent, text, command, width=25, is_primary=True,
                             side="top", padx=0, pady=8):
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

        # initial positions
        self.player_x = self.start_x
        self.opponent_x = self.start_x

        # clear previous items if any
        for attr in ("player_item", "opponent_item", "player_label", "opponent_label"):
            if getattr(self, attr, None):
                self.canvas.delete(getattr(self, attr))

        font_size = 9
        label_font_size = 14
        label_offset = 60  # distance below ASCII art

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
        self.start_time = time.time()
        self.moves = 0
        self.time_elapsed = 0
        self.correct_terms = []
        self._update_moves_label()
        self.time_label.config(text="Time: 0s")

        # schedule flows
        self.next_flashcard()
        self._schedule_opponent_move()
        self.update_timer()

    def next_flashcard(self):
        # picks the next flashcard, avoiding repetition of the last one

        if not self.running or not self.flashcards:
            return

        # cancel previous timeout
        if self._timeout_after_id is not None:
            try:
                self.root.after_cancel(self._timeout_after_id)
            except Exception:
                pass
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
        self._timeout_after_id = self._after(8000, self._timeout_answer_penalty)

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
            self._check_winner_or_continue()
            # next question
            self.next_flashcard()

    def submit_answer(self):
        # handles answer submission and moves the player if correct
        if not self.running or not self.current_flashcard:
            return

        # cancel timeout
        if self._timeout_after_id is not None:
            try:
                self.root.after_cancel(self._timeout_after_id)
            except Exception:
                pass
            self._timeout_after_id = None

        user = self.answer_entry.get().strip()
        correct = self.current_flashcard[2].strip()

        if not user:
            messagebox.showinfo(
                "No answer",
                "Please enter a translation (or Close to stop).",
                parent=self.root
            )
            return

        # track move
        self.moves += 1
        self._update_moves_label()

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
            self._after(20, lambda: step(i + 1))

        step(0)

    def _schedule_opponent_move(self):
        # schedules periodic movement of the opponent
        if not self.running:
            return
        self._opponent_move_once()
        self._opponent_after_id = self._after(self.opponent_tick_ms, self._schedule_opponent_move)

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
            self._end_game("You win! 🎉")
        elif self.opponent_x + margin >= self.finish_x:
            self._end_game("Opponent wins. Try again!")

    def _end_game(self, message=""):
        self.running = False

        # cancel timers
        if self._opponent_after_id:
            try:
                self.root.after_cancel(self._opponent_after_id)
            except Exception:
                pass
            self._opponent_after_id = None

        if self._timeout_after_id:
           try:
                self.root.after_cancel(self._timeout_after_id)
           except Exception:
                pass
           self._timeout_after_id = None

        for jid in list(self._after_jobs):
            try:
                self.root.after_cancel(jid)
            except Exception:
                pass
            self._after_jobs.discard(jid)

        # disable entry, enable play again
        try:
            if self.answer_entry.winfo_exists():
                self.answer_entry.config(state='disabled')
        except Exception:
            pass
        try:
            if self.play_again_btn.winfo_exists():
                self.play_again_btn.config(state='normal')
        except Exception:
            pass

        # Notify player with message (if provided)
        if message:
            self._game_over_popup(message)

        # Update streak
        if self.on_streak:
            self.on_streak(success=True)

    def _game_over(self, message=''):
        if message: messagebox.showinfo('Game Over', message, parent=self.root)
        if self.on_streak: self.on_streak(success=True)
        self._end_game()

    def _game_over_popup(self, message=''):
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

        # Create popup window
        popup = tk.Toplevel(self.root)
        popup.transient(self.root)
        popup.grab_set()
        popup.configure(bg=self.colors["cream"])
        popup.title("Game Complete!")
        popup.resizable(False, False)

        # Set fixed size and center the window
        w, h = 400, 300
        x = self.root.winfo_rootx() + (self.root.winfo_width() - w) // 2
        y = self.root.winfo_rooty() + (self.root.winfo_height() - h) // 2
        popup.geometry(f"{w}x{h}+{x}+{y}")

        # Stats label (centered)
        stats_label = tk.Label(
            popup,
            text=stats,
            font=("Helvetica", 14, "bold"),
            bg=self.colors["cream"],
            fg=self.colors["dark_green"],
            justify="center",
            wraplength=360
        )
        stats_label.place(relx=0.5, rely=0.35, anchor="center")

        button_container = tk.Frame(popup, bg=self.colors["cream"])
        button_container.place(relx=0.5, rely=0.8, anchor="center")

        btn_font = font.Font(family="Helvetica", size=11, weight="bold")

        def create_popup_button(parent, text, command):
            outer = tk.Frame(parent, bg=self.colors["brown"])
            inner = tk.Frame(outer, bg=self.colors["sage"])
            btn = tk.Button(
                inner,
                text=text,
                font=btn_font,
                bg=self.colors["sage"],
                fg=self.colors["dark_green"],
                activebackground=self.colors["lime"],
                activeforeground=self.colors["dark_green"],
                relief="flat",
                bd=0,
                padx=18,
                pady=10,
                cursor="hand2",
                command=command,
            )
            btn.pack(expand=True, fill="both", padx=2, pady=2)
            inner.pack(expand=True, fill="both", padx=3, pady=3)
            outer.pack(side="left", padx=10)

            def on_enter(_):
                btn.configure(bg=self.colors["lime"])
                inner.configure(bg=self.colors["lime"])

            def on_leave(_):
                btn.configure(bg=self.colors["sage"])
                inner.configure(bg=self.colors["sage"])

            btn.bind("<Enter>", on_enter)
            btn.bind("<Leave>", on_leave)
            return btn

        def restart_and_close():
            popup.destroy()
            self.reset_game()

        def menu_and_close():
            popup.destroy()
            self.return_to_main_menu()

        btn_row = tk.Frame(popup, bg=self.colors["cream"])
        btn_row.place(relx=0.5, rely=0.8, anchor="center")
        create_popup_button(btn_row, "🔄 New Game", restart_and_close)
        create_popup_button(btn_row, "← Back to Menu", menu_and_close)

        # keyboard shortcuts
        popup.bind('<Return>', lambda e: restart_and_close())
        popup.bind('<Escape>', lambda e: menu_and_close())

        popup.focus_set()
        popup.wait_window()

    # -------------------- utilities -------------------- #
    def _after(self, ms, fn):
        jid = None
        def wrapper():
            self._after_jobs.discard(jid)
            fn()
        jid = self.root.after(ms, wrapper)
        self._after_jobs.add(jid)
        return jid

    def _update_moves_label(self):
        if self.moves_label and self.moves_label.winfo_exists():
            self.moves_label.config(text=f"Moves: {self.moves}")

    def _cleanup(self):
        self.running = False
        if self._opponent_after_id:
            try:
                self.root.after_cancel(self._opponent_after_id)
            except Exception:
                pass
            self._opponent_after_id = None
        if self._timeout_after_id:
            try:
                self.root.after_cancel(self._timeout_after_id)
            except Exception:
                pass
            self._timeout_after_id = None
        for jid in list(self._after_jobs):
            try:
                self.root.after_cancel(jid)
            except Exception:
                pass
            self._after_jobs.discard(jid)


    # root-level cleanup
    def return_to_main_menu(self):
        # cleanup and restore the root app window
        self._cleanup()
        try:
            self.container.destroy()
        except Exception:
            pass
        self.root.configure(bg=self._original_bg)
        self.root.title(self._original_title)

        if callable(self.on_exit):
            self.on_exit()

    def reset_game(self):
        # resets the game to initial state for a new race
        self._cleanup()
        self.start_time = time.time()
        self.moves = 0
        self._update_moves_label()
        if self.answer_entry and self.answer_entry.winfo_exists():
            self.answer_entry.config(state="normal")
            self.answer_entry.delete(0, tk.END)
        if self.info_label and self.info_label.winfo_exists():
            self.info_label.config(text="Answer as fast as you can! (≤8s = faster)")
        self._place_characters()
        # start fresh race
        self._after(300, self.start_race)

    def update_timer(self):
        if not self.running:
            return
        self.time_elapsed += 1
        if self.time_label.winfo_exists():
            self.time_label.config(text=f"Time: {self.time_elapsed}s")
            self._after(1000, self.update_timer) # update every 1s





