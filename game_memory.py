import tkinter as tk
from tkinter import messagebox, font
import random
import time
import math


class RoundedCard(tk.Canvas):
    def __init__(self, master, width, height, bg, inner_rim_color, outer_rim_color, radius=18):
        super().__init__(master, width=width, height=height, bd=0, highlightthickness=0, bg=master['bg'])
        self.radius = radius
        self.bg_color = bg
        self.inner_rim_color = inner_rim_color
        self.outer_rim_color = outer_rim_color
        self.shadow_color = "#89725B"
        self._inner_pad = 12
        self._outer_rim_id = None
        self._inner_rim_id = None
        self._shadow_id = None
        self._window_id = None

        self.button = tk.Button(
            self,
            text="",
            font=("Helvetica", 12, "bold"),
            bg=bg,
            fg="#677E52",
            activebackground=bg,
            activeforeground="#677E52",
            relief="flat",
            bd=0,
            cursor="hand2",
            wraplength=0,
            justify="center",
            anchor="center",
        )
        self._redraw(width, height)

    @staticmethod
    def _round_points(x1, y1, x2, y2, r):
        return [
            x1 + r, y1,
            x2 - r, y1,
            x2, y1,
            x2, y1 + r,
            x2, y2 - r,
            x2, y2,
            x2 - r, y2,
            x1 + r, y2,
            x1, y2,
            x1, y2 - r,
            x1, y1 + r,
            x1, y1,
        ]

    def _redraw(self, width, height):
        self.config(width=width, height=height)

        # Clear existing elements
        if self._shadow_id is not None:
            self.delete(self._shadow_id)
        if self._outer_rim_id is not None:
            self.delete(self._outer_rim_id)
        if self._inner_rim_id is not None:
            self.delete(self._inner_rim_id)

        # Draw shadow (offset by 4 pixels)
        shadow_pts = self._round_points(4, 4, width + 2, height + 2, self.radius)
        self._shadow_id = self.create_polygon(
            shadow_pts, smooth=True, fill=self.shadow_color, outline="", width=0
        )

        # Draw outer rim
        outer_pts = self._round_points(2, 2, width - 2, height - 2, self.radius)
        self._outer_rim_id = self.create_polygon(
            outer_pts, smooth=True, fill=self.outer_rim_color, outline="", width=0
        )

        # Draw inner rim (card background)
        inner_pts = self._round_points(6, 6, width - 6, height - 6, self.radius - 4)
        self._inner_rim_id = self.create_polygon(
            inner_pts, smooth=True, fill=self.inner_rim_color, outline="", width=0
        )

        # Draw main card background
        card_pts = self._round_points(10, 10, width - 10, height - 10, self.radius - 8)
        self._card_bg_id = self.create_polygon(
            card_pts, smooth=True, fill=self.bg_color, outline="", width=0
        )

        inner_w = max(1, width - self._inner_pad * 2)
        inner_h = max(1, height - self._inner_pad * 2)
        if self._window_id is None:
            self._window_id = self.create_window(
                width // 2, height // 2, window=self.button, width=inner_w, height=inner_h
            )
        else:
            self.coords(self._window_id, width // 2, height // 2)
            self.itemconfigure(self._window_id, width=inner_w, height=inner_h)

    def resize(self, width, height):
        self._redraw(width, height)

    def set_card_colors(self, bg_color, inner_rim_color, outer_rim_color):
        self.bg_color = bg_color
        self.inner_rim_color = inner_rim_color
        self.outer_rim_color = outer_rim_color
        self.itemconfig(self._card_bg_id, fill=bg_color)
        self.itemconfig(self._inner_rim_id, fill=inner_rim_color)
        self.itemconfig(self._outer_rim_id, fill=outer_rim_color)


class MemoryGame:
    def __init__(self, root, flashcards, on_exit=None):
        self.root = root
        self.flashcards = flashcards  # list of (id, term, translation)
        self.on_exit = on_exit

        # remember original root state to restore after exit
        self._original_bg = self.root.cget("bg")
        self._original_title = self.root.title()

        # Theme
        self.colors = {
            "cream": "#F6E8B1",
            "sage": "#B0CC99",
            "brown": "#89725B",
            "lime": "#B7CA79",
            "dark_green": "#677E52",
        }

        # container: only child of root while game is active (use pack here)
        self.container = tk.Frame(self.root, bg=self.colors["cream"])  # isolate layout
        self.container.pack(fill="both", expand=True)

        # State
        self.cards = []
        self.card_widgets = []
        self.flipped_cards = []
        self.matched_pairs = set()
        self.moves = 0
        self.start_time = time.time()
        self.game_frame = None
        self.control_frame = None

        # Animation / timers
        self.flip_animation_running = False
        self._after_jobs = set()  # track after() ids for clean cancel
        self._layout_job = None

        # Build UI within container
        self._build_layout()
        self.reset_board()

        # Bind resize on container (not root) to avoid global churn
        self._resize_bind_id = self.container.bind("<Configure>", self._on_resize)

    def _fit_single_line(self, button, max_width_px):
        txt = button.cget("text") or ""
        if not txt:
            return
        f = font.Font(font=button.cget("font"))
        fam = f.actual("family")
        size = f.actual("size") or 12
        button.configure(wraplength=0, anchor="center", justify="center")
        while size >= 8:
            f.configure(size=size)
            if f.measure(txt) <= max_width_px:
                break
            size -= 1
        button.configure(font=(fam, size, "bold"))

    # -------------------------- layout -----------------------------------
    def _build_layout(self):
        # clear container only (never touch other root content)
        for w in self.container.winfo_children():
            w.destroy()
        self.root.title("FlashPlay - Memory Game")
        self.root.configure(bg=self.colors["cream"])

        # grid inside container; root uses pack -> no pack/grid mixing
        self.container.grid_rowconfigure(2, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        header = tk.Frame(self.container, bg=self.colors["cream"], pady=12)
        header.grid(row=0, column=0, sticky="ew")
        title_font = font.Font(family="Helvetica", size=24, weight="bold")
        tk.Label(
            header,
            text="🧠 Memory Game",
            font=title_font,
            bg=self.colors["cream"],
            fg=self.colors["dark_green"],
        ).pack()

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

        self.game_frame = tk.Frame(self.container, bg=self.colors["cream"])  # row 2
        self.game_frame.grid(row=2, column=0, sticky="nsew", padx=12, pady=12)

        self.control_frame = tk.Frame(self.container, bg=self.colors["cream"])  # row 3
        self.control_frame.grid(row=3, column=0, sticky="ew", pady=(0, 12))
        self._build_controls()

    def _build_controls(self):
        for w in self.control_frame.winfo_children():
            w.destroy()
        button_font = font.Font(family="Helvetica", size=11, weight="bold")

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

        card_button(self.control_frame, "🔄 New Game", self.reset_game)
        card_button(self.control_frame, "← Back to Menu", self.return_to_main_menu)

    # --------------------------- data ------------------------------------
    def _prepare_cards(self):
        if not self.flashcards:
            messagebox.showinfo("No cards", "You don't have any flashcards yet.")
            return False
        # max 10 pairs, at least 1 (if available)
        max_pairs = min(10, len(self.flashcards))
        num_pairs = max_pairs  # later you can expose this as difficulty
        selected = random.sample(self.flashcards, num_pairs)

        self.cards = []
        for pid, term, translation in selected:
            self.cards.append({"content": term, "pair_id": pid, "type": "term"})
            self.cards.append({"content": translation, "pair_id": pid, "type": "translation"})
        random.shuffle(self.cards)
        return True

    # --------------------------- board -----------------------------------
    def reset_board(self):
        for w in self.game_frame.winfo_children():
            w.destroy()
        self.card_widgets.clear()
        self.flipped_cards.clear()
        self.matched_pairs.clear()
        self.moves = 0
        self.start_time = time.time()
        if not self._prepare_cards():
            return
        self._create_grid()
        self._layout_cards()
        self.update_timer()
        self.moves_label.config(text=f"Moves: {self.moves}")

    @staticmethod
    def _best_grid(n):
        # nearly square, cap columns at 6
        best = (1, n)
        min_diff = 999
        for cols in range(2, min(6, n) + 1):
            rows = math.ceil(n / cols)
            diff = abs(rows - cols)
            if rows * cols >= n and diff < min_diff:
                min_diff = diff
                best = (rows, cols)
        return best

    def _create_grid(self):
        for r in range(12):
            self.game_frame.grid_rowconfigure(r, weight=0)
        for c in range(12):
            self.game_frame.grid_columnconfigure(c, weight=0)

        n = len(self.cards)
        rows, cols = self._rows, self._cols = self._best_grid(n)

        for i in range(n):
            r, c = divmod(i, cols)
            # Default state: lime inner rim, sage outer rim, brown shadow
            card = RoundedCard(
                self.game_frame,
                width=160,
                height=110,
                bg=self.colors["lime"],  # background when face down
                inner_rim_color=self.colors["lime"],  # inner rim
                outer_rim_color=self.colors["sage"],  # outer rim
                radius=18,
            )
            card.grid(row=r, column=c, padx=8, pady=8, sticky="nsew")
            self.game_frame.grid_rowconfigure(r, weight=1)
            self.game_frame.grid_columnconfigure(c, weight=1)

            btn = card.button
            btn.config(command=lambda idx=i: self.on_card_click(idx))

            def mk_hover(b=btn, cnv=card):
                def on_enter(_):
                    if not self.flip_animation_running and b.cget("text") == "":
                        # Hover state: sage inner rim, dark green outer rim
                        b.configure(bg=self.colors["sage"])
                        cnv.set_card_colors(self.colors["sage"], self.colors["sage"], self.colors["dark_green"])

                def on_leave(_):
                    if not self.flip_animation_running and b.cget("text") == "":
                        # Normal state: lime inner rim, sage outer rim
                        b.configure(bg=self.colors["lime"])
                        cnv.set_card_colors(self.colors["lime"], self.colors["lime"], self.colors["sage"])

                return on_enter, on_leave

            enter, leave = mk_hover()
            btn.bind("<Enter>", enter)
            btn.bind("<Leave>", leave)

            self.card_widgets.append({
                "button": btn,
                "canvas": card,
                "flipped": False,
                "matched": False,
            })

    def _available_area(self):
        self.root.update_idletasks()
        w = self.game_frame.winfo_width()
        h = self.game_frame.winfo_height()
        if w <= 1 or h <= 1:
            w = max(420, self.root.winfo_width() - 24)
            h = max(320, self.root.winfo_height() - 180)
        return w, h

    def _layout_cards(self):
        n = len(self.cards)
        rows, cols = self._rows, self._cols
        area_w, area_h = self._available_area()
        gap = 16  # consistent spacing
        card_w = max(100, (area_w - (cols + 1) * gap) // max(1, cols))
        card_h = max(80, (area_h - (rows + 1) * gap) // max(1, rows))

        # keep aspect ~ 1.45 (w/h)
        ratio = 1.45
        if card_w / max(1, card_h) > ratio:
            card_w = int(card_h * ratio)
        else:
            card_h = int(card_w / ratio)

        for wdg in self.card_widgets:
            cur_w = wdg["canvas"].winfo_width()
            cur_h = wdg["canvas"].winfo_height()
            if abs(cur_w - card_w) > 2 or abs(cur_h - card_h) > 2:
                wdg["canvas"].resize(card_w, card_h)

    def _on_resize(self, _evt):
        if self._layout_job:
            try:
                self.root.after_cancel(self._layout_job)
            except Exception:
                pass
        self._layout_job = self.root.after(120, self._layout_cards)

    def on_card_click(self, idx):
        if self.flip_animation_running:
            return
        cw = self.card_widgets[idx]
        if cw['flipped'] or cw["matched"]:
            return
        self._flip(idx, reveal=True)
        self.flipped_cards.append(idx)
        if len(self.flipped_cards) == 2:
            self.moves += 1
            self.moves_label.config(text=f"Moves: {self.moves}")
            self._after(600, self._check_match)

    def _animate_flip(self, canvas, to_face_callback):
        self.flip_animation_running = True
        total_frames = 8
        frame_ms = 22

        win_id = canvas._window_id
        start_w = canvas.itemcget(win_id, "width")
        try:
            start_w = int(start_w)
        except Exception:
            start_w = max(1, canvas.winfo_width() - 24)

        def set_inner_width(v):
            canvas.itemconfigure(win_id, width=max(1, int(v)))

        def shrink(frame=0):
            if frame <= total_frames:
                set_inner_width(start_w * (1 - frame / total_frames))
                self._after(frame_ms, lambda: shrink(frame + 1))
            else:
                to_face_callback()
                expand()

        def expand(frame=0):
            if frame <= total_frames:
                set_inner_width(start_w * (frame / total_frames))
                self._after(frame_ms, lambda: expand(frame + 1))
            else:
                self.flip_animation_running = False

        shrink()

    def _flip(self, idx, reveal=True):
        cw = self.card_widgets[idx]
        btn = cw["button"]
        canvas = cw["canvas"]

        def apply_face():
            if reveal:
                text = self.cards[idx]["content"]
                btn.configure(text=text)
                # Flipped state: keep lime inner rim, sage outer rim
                if self.cards[idx]["type"] == "term":
                    btn.configure(bg=self.colors["sage"], fg=self.colors["dark_green"])
                    canvas.set_card_colors(self.colors["sage"], self.colors["lime"], self.colors["sage"])
                else:
                    btn.configure(bg=self.colors["cream"], fg=self.colors["dark_green"])
                    canvas.set_card_colors(self.colors["cream"], self.colors["lime"], self.colors["sage"])
                cw["flipped"] = True
            else:
                # Back to face-down state: lime inner rim, sage outer rim
                btn.configure(text="", bg=self.colors["lime"], fg=self.colors["dark_green"])
                canvas.set_card_colors(self.colors["lime"], self.colors["lime"], self.colors["sage"])
                cw["flipped"] = False

        self._animate_flip(canvas, apply_face)

    def _check_match(self):
        if len(self.flipped_cards) != 2:
            return
        a, b = self.flipped_cards
        ca, cb = self.cards[a], self.cards[b]
        if ca["pair_id"] == cb["pair_id"] and ca["type"] != cb["type"]:
            for i in (a, b):
                cw = self.card_widgets[i]
                cw["matched"] = True
                cw["button"].configure(state="disabled")
                # Matched state: dark green inner rim, brown outer rim
                cw["canvas"].set_card_colors(cw["canvas"].bg_color, self.colors["dark_green"], self.colors["brown"])
            self.matched_pairs.add(ca["pair_id"])
            if self._is_won():
                self._after(500, self._game_over)
        else:
            self._after(300, lambda: (self._flip(a, reveal=False), self._flip(b, reveal=False)))
        self.flipped_cards.clear()

    def _is_won(self):
        total = len({c["pair_id"] for c in self.cards})
        return len(self.matched_pairs) == total

    def _game_over(self):
        elapsed = int(time.time() - self.start_time)
        msg = (
            "🎉 Congratulations! 🎉\n\n"
            f"You completed the memory game!\n\n"
            "📊 Your Stats:\n"
            f"• Moves: {self.moves}\n"
            f"• Time: {elapsed}s\n"
            f"• Pairs: {len(self.matched_pairs)}"
        )
        if messagebox.askquestion("Game Complete!", msg + "\n\nPlay again?") == "yes":
            self.reset_game()
        else:
            self.return_to_main_menu()

    # ------------------------ utilities / timers --------------------------
    def _after(self, ms, fn):
        jid = self.root.after(ms, lambda: (self._after_jobs.discard(jid), fn()))
        self._after_jobs.add(jid)
        return jid

    def _cleanup(self):
        # cancel scheduled jobs
        for jid in list(self._after_jobs):
            try:
                self.root.after_cancel(jid)
            except Exception:
                pass
        self._after_jobs.clear()
        # unbind resize
        try:
            if self._resize_bind_id:
                self.container.unbind("<Configure>", self._resize_bind_id)
        except Exception:
            pass

    def return_to_main_menu(self):
        self._cleanup()
        try:
            self.container.destroy()
        except Exception:
            pass
        # restore root state
        self.root.configure(bg=self._original_bg)
        self.root.title(self._original_title)

        if callable(self.on_exit):
            self.on_exit()
        else:
            # fallback view if no callback provided
            for w in self.root.winfo_children():
                w.destroy()
            tk.Label(self.root, text="Thanks for playing!", font=("Helvetica", 16),
                     bg=self.colors["cream"], fg=self.colors["dark_green"]).pack(expand=True)

    def reset_game(self):
        self.reset_board()

    def update_timer(self):
        if hasattr(self, "time_label"):
            elapsed_time = int(time.time() - self.start_time)
            self.time_label.config(text=f"Time: {elapsed_time}s")
            if not self._is_won():
                self._after(1000, self.update_timer)


