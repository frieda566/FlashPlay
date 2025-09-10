import tkinter as tk
from tkinter import messagebox, simpledialog, ttk, font
from flashcards import FlashcardManager
from game_memory import MemoryGame
from game_race import RaceGame
from deep_translator import GoogleTranslator
from streak_plants import PlantTracker

class FlashcardApp:
    def __init__(self, root):
        self.root = root
        self.root.title("FlashPlay - Interactive Vocabulary Learning")

        # Farben
        self.colors = {
            "cream": "#F6E8B1",
            "sage": "#B0CC99",
            "brown": "#89725B",
            "lime": "#B7CA79",
            "dark_green": "#677E52",
        }
        self.root.configure(bg=self.colors["cream"])

        # Constants
        self.SEARCH_CARD_WIDTH = 520
        self.SEARCH_CARD_HEIGHT = 92
        self.FLASHCARD_CARD_WIDTH = 680
        self.FLASHCARD_CARD_HEIGHT = 88
        self.BUTTON_COLUMN_WIDTH = 210  # Platz rechts für Edit/Delete

        self.flashcard_manager = FlashcardManager()
        self.search_var = None
        self.all_flashcards = []
        self.filtered_flashcards = []
        self.scrollable_frame = None
        self._canvas_window = None
        self.streak_days = 0

        self.setup_main_menu()

    # UI from buttons
    def create_styled_button(self, parent, text, command, width=25, is_primary=True):
        button_container = tk.Frame(parent, bg=self.colors["cream"])
        button_container.pack(pady=8)

        outer_frame = tk.Frame(button_container, bg=self.colors["brown"])
        outer_frame.pack()

        bg_color = self.colors["sage"] if is_primary else self.colors["lime"]
        inner_frame = tk.Frame(outer_frame, bg=bg_color)
        inner_frame.pack(padx=3, pady=3)

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
            pady=12,
            cursor="hand2",
            command=command
        )
        btn.pack(padx=4, pady=4)

        def on_enter(_):
            hover_color = self.colors["lime"] if is_primary else self.colors["sage"]
            btn.configure(bg=hover_color)
            inner_frame.configure(bg=hover_color)

        def on_leave(_):
            btn.configure(bg=bg_color)
            inner_frame.configure(bg=bg_color)

        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        return btn

    def create_small_button(self, parent, text, command, side="left", padx=5):
        btn_container = tk.Frame(parent, bg=self.colors["cream"])
        btn_container.pack(side=side, padx=padx)

        shadow_frame = tk.Frame(btn_container, bg=self.colors["brown"])
        shadow_frame.pack()

        bg_frame = tk.Frame(shadow_frame, bg=self.colors["lime"])
        bg_frame.pack(padx=2, pady=2)

        small_font = font.Font(family="Helvetica", size=10, weight="bold")
        btn = tk.Button(
            bg_frame,
            text=text,
            font=small_font,
            bg=self.colors["lime"],
            fg=self.colors["dark_green"],
            activebackground=self.colors["sage"],
            activeforeground=self.colors["dark_green"],
            relief="flat",
            bd=0,
            padx=12,
            pady=6,
            cursor="hand2",
            command=command
        )
        btn.pack(padx=2, pady=2)

        def on_enter(_):
            btn.configure(bg=self.colors["sage"])
            bg_frame.configure(bg=self.colors["sage"])

        def on_leave(_):
            btn.configure(bg=self.colors["lime"])
            bg_frame.configure(bg=self.colors["lime"])

        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        return btn

    def create_styled_scrollbar(self, parent):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "Custom.Vertical.TScrollbar",
            background=self.colors["sage"],
            troughcolor=self.colors["cream"],
            bordercolor=self.colors["brown"],
            arrowcolor=self.colors["dark_green"],
            darkcolor=self.colors["brown"],
            lightcolor=self.colors["lime"],
        )
        return ttk.Scrollbar(parent, orient="vertical", style="Custom.Vertical.TScrollbar")

    def increase_streak(self, success=True):
        if success:
            self.streak_days = min(self.streak_days + 1, 20)
        else:
            self.streak_days = 0
        # redraw main menu to refresh the plants
        self.setup_main_menu()

    # screens
    def setup_main_menu(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        self.root.configure(bg=self.colors["cream"])

        main_frame = tk.Frame(self.root, bg=self.colors["cream"])
        main_frame.pack(fill="both", expand=True, padx=30, pady=30)

        title_frame = tk.Frame(main_frame, bg=self.colors["cream"])
        title_frame.grid(row=0, column=0, columnspan=3, pady=(20, 30))  # grid inside main_frame
        icon_font = font.Font(family="Helvetica", size=36)
        tk.Label(title_frame, text="📚", font=icon_font, bg=self.colors["cream"]).pack()
        title_font = font.Font(family="Helvetica", size=24, weight="bold")
        tk.Label(title_frame, text="FlashPlay", font=title_font,
                 bg=self.colors["cream"], fg=self.colors["dark_green"]).pack(pady=(5, 0))
        subtitle_font = font.Font(family="Helvetica", size=14)
        tk.Label(title_frame, text="Interactive Vocabulary Learning", font=subtitle_font,
                 bg=self.colors["cream"], fg=self.colors["brown"]).pack(pady=(2, 20))

        # configure columns: left plant, center buttons, right plant
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=2)
        main_frame.grid_columnconfigure(2, weight=1)

        self._left_plant = PlantTracker(main_frame, width=120, height=240)
        self._left_plant.frame.grid(row=1, column=0, sticky="n", padx=10, pady=6)

        button_frame = tk.Frame(main_frame, bg=self.colors["cream"])
        button_frame.grid(row=1, column=1, padx=10, pady=6, sticky="n")

        self.create_styled_button(button_frame, "🧠 Play Memory Game", self.launch_memory_game, is_primary=True)
        self.create_styled_button(button_frame, "🏃 Play Race Game", self.launch_game_race, is_primary=True)
        self.create_styled_button(button_frame, "⚙️ Manage Flashcards", self.manage_flashcards, is_primary=False)
        self.create_styled_button(button_frame, "ℹ️ Info", self.info, is_primary=False)
        self.create_styled_button(button_frame, "❌ Exit", self.root.quit, width=15, is_primary=False)

        self._right_plant = PlantTracker(main_frame, width=120, height=240)
        self._right_plant.frame.grid(row=1, column=2, sticky="n", padx=10, pady=6)

    def info(self):
        # Create and display an info window with explanatory text from separate file
        try:
            import info
            print("✓ Successfully imported info module")

            # Check if the function exists
            if hasattr(info, 'get_app_info'):
                info_text = info.get_app_info()
                print("✓ Successfully got app info from function")
            else:
                print("✗ get_app_info function not found in info module")
                # Try alternative attribute names
                if hasattr(info, 'INFO_TEXT'):
                    info_text = info.INFO_TEXT
                    print("✓ Found INFO_TEXT variable instead")
                else:
                    print("✗ No INFO_TEXT variable found either")
                    raise AttributeError("No info content found")

        except ImportError as e:
            print(f"✗ Could not import info module: {e}")
            messagebox.showerror("Import Error",
                                 f"Could not import info module: {str(e)}\n\nMake sure info.py is in the same folder as main.py")
            return
        except AttributeError as e:
            print(f"✗ Attribute error: {e}")
            messagebox.showerror("Content Error", f"Info module found but content missing: {str(e)}")
            return
        except Exception as e:
            print(f"✗ Unexpected error: {e}")
            messagebox.showerror("Unexpected Error", f"Unexpected error loading info: {str(e)}")
            return

        # Create a new window
        info_window = tk.Toplevel(self.root)
        info_window.title("FlashPlay - Information & Help")
        info_window.geometry("700x600")
        info_window.configure(bg=self.colors["cream"])
        info_window.resizable(True, True)
        info_window.minsize(500, 400)

        # Center the window
        x = self.root.winfo_rootx() + (self.root.winfo_width() - 700) // 2
        y = self.root.winfo_rooty() + (self.root.winfo_height() - 600) // 2
        info_window.geometry(f"700x600+{x}+{y}")
        info_window.transient(self.root)
        info_window.grab_set()

        # Create main container with existing styling
        main_container = tk.Frame(info_window, bg=self.colors["brown"])
        main_container.pack(fill="both", expand=True, padx=6, pady=6)

        outer_frame = tk.Frame(main_container, bg=self.colors["sage"])
        outer_frame.pack(fill="both", expand=True, padx=2, pady=2)

        inner_frame = tk.Frame(outer_frame, bg=self.colors["cream"])
        inner_frame.pack(fill="both", expand=True, padx=4, pady=4)

        # Title
        title_font = font.Font(family="Helvetica", size=18, weight="bold")
        title_label = tk.Label(
            inner_frame,
            text="📖 FlashPlay - Information & Help",
            font=title_font,
            bg=self.colors["cream"],
            fg=self.colors["dark_green"]
        )
        title_label.pack(pady=(15, 20))

        # Create scrollable text area
        text_container = tk.Frame(inner_frame, bg=self.colors["cream"])
        text_container.pack(fill="both", expand=True, pady=(0, 15))

        canvas = tk.Canvas(text_container, bg=self.colors["cream"], highlightthickness=0)
        scrollbar = self.create_styled_scrollbar(text_container)
        scrollbar.config(command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        text_frame = tk.Frame(canvas, bg=self.colors["cream"])
        canvas_window = canvas.create_window((0, 0), window=text_frame, anchor="nw")

        # Create text label with the imported content
        text_content = tk.Label(
            text_frame,
            text=info_text.strip(),
            font=("Helvetica", 11),
            bg=self.colors["cream"],
            fg=self.colors["dark_green"],
            justify="left",
            anchor="nw",
            wraplength=650
        )
        text_content.pack(fill="both", expand=True, padx=15, pady=15)

        # Scroll region and resize handling
        def update_scroll_region(event=None):
            canvas.configure(scrollregion=canvas.bbox("all"))

        def resize_text_frame(event):
            canvas.itemconfig(canvas_window, width=event.width)
            new_wraplength = max(300, event.width - 50)
            text_content.configure(wraplength=new_wraplength)
            canvas.after_idle(update_scroll_region)

        text_frame.bind("<Configure>", update_scroll_region)
        canvas.bind("<Configure>", resize_text_frame)

        # Mouse wheel scrolling
        def on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        # Bind to multiple widgets for better scrolling
        canvas.bind("<MouseWheel>", on_mousewheel)
        info_window.bind("<MouseWheel>", on_mousewheel)
        text_container.bind("<MouseWheel>", on_mousewheel)
        inner_frame.bind("<MouseWheel>", on_mousewheel)
        main_container.bind("<MouseWheel>", on_mousewheel)

        # Close button with existing styling
        button_container = tk.Frame(inner_frame, bg=self.colors["cream"])
        button_container.pack(pady=(15, 10))

        close_outer = tk.Frame(button_container, bg=self.colors["brown"])
        close_outer.pack()

        close_inner = tk.Frame(close_outer, bg=self.colors["lime"])
        close_inner.pack(padx=3, pady=3)

        close_font = font.Font(family="Helvetica", size=12, weight="bold")
        close_btn = tk.Button(
            close_inner,
            text="✓ Close",
            font=close_font,
            bg=self.colors["lime"],
            fg=self.colors["dark_green"],
            activebackground=self.colors["sage"],
            activeforeground=self.colors["dark_green"],
            relief="flat",
            bd=0,
            width=15,
            pady=8,
            cursor="hand2",
            command=info_window.destroy
        )
        close_btn.pack(padx=4, pady=4)

        # Hover effects
        def on_enter(event):
            close_btn.configure(bg=self.colors["sage"])
            close_inner.configure(bg=self.colors["sage"])

        def on_leave(event):
            close_btn.configure(bg=self.colors["lime"])
            close_inner.configure(bg=self.colors["lime"])

        close_btn.bind("<Enter>", on_enter)
        close_btn.bind("<Leave>", on_leave)

        info_window.focus_set()
        info_window.after_idle(update_scroll_region)

    def manage_flashcards(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        self.root.configure(bg=self.colors["cream"])

        main_frame = tk.Frame(self.root, bg=self.colors["cream"])
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        header_frame = tk.Frame(main_frame, bg=self.colors["cream"])
        header_frame.pack(fill="x", pady=(10, 0))

        title_font = font.Font(family="Helvetica", size=20, weight="bold")
        tk.Label(
            header_frame, text="📝 Manage Flashcards",
            font=title_font, bg=self.colors["cream"], fg=self.colors["dark_green"]
        ).pack()

        # Top controls
        control_frame = tk.Frame(main_frame, bg=self.colors["cream"])
        control_frame.pack(fill="x", pady=(10, 0))

        buttons_row = tk.Frame(control_frame, bg=self.colors["cream"])
        buttons_row.pack()

        # Add / Back
        def mk_btn(text, bg, command):
            outer = tk.Frame(buttons_row, bg=self.colors["brown"])
            outer.pack(side="left", padx=5)
            inner = tk.Frame(outer, bg=bg)
            inner.pack(padx=3, pady=3)
            btn = tk.Button(
                inner, text=text, font=("Helvetica", 12, "bold"),
                bg=bg, fg=self.colors["dark_green"], relief="flat", bd=0,
                width=20, pady=12, cursor="hand2", command=command
            )
            btn.pack(padx=4, pady=4)
            return btn, inner

        add_btn, add_inner = mk_btn("➕ Add New Flashcard", self.colors["sage"], self.add_flashcard_with_translation)
        back_btn, back_inner = mk_btn("← Back to Main Menu", self.colors["lime"], self.setup_main_menu)

        add_btn.bind("<Enter>", lambda e: (add_btn.config(bg=self.colors["lime"]), add_inner.config(bg=self.colors["lime"])))
        add_btn.bind("<Leave>", lambda e: (add_btn.config(bg=self.colors["sage"]), add_inner.config(bg=self.colors["sage"])))
        back_btn.bind("<Enter>", lambda e: (back_btn.config(bg=self.colors["sage"]), back_inner.config(bg=self.colors["sage"])))
        back_btn.bind("<Leave>", lambda e: (back_btn.config(bg=self.colors["lime"]), back_inner.config(bg=self.colors["lime"])))

        # Searchbar
        self.search_var = tk.StringVar()
        self.search_var.trace('w', self.filter_flashcards)

        search_container = tk.Frame(main_frame, bg=self.colors["cream"])
        search_container.pack(pady=(10, 20))

        search_card = tk.Frame(search_container, bg=self.colors["brown"],
                               width=self.SEARCH_CARD_WIDTH, height=self.SEARCH_CARD_HEIGHT)
        search_card.pack()
        search_card.pack_propagate(False)

        search_inner = tk.Frame(search_card, bg=self.colors["sage"])
        search_inner.pack(fill="both", expand=True, padx=2, pady=2)

        search_content = tk.Frame(search_inner, bg=self.colors["cream"])
        search_content.pack(fill="both", expand=True, padx=4, pady=4)

        tk.Label(
            search_content, text="🔍 Search Flashcards",
            font=("Helvetica", 12, "bold"),
            bg=self.colors["cream"], fg=self.colors["dark_green"]
        ).pack(pady=(5, 3))

        tk.Entry(
            search_content, textvariable=self.search_var, width=50, font=("Helvetica", 11),
            bg=self.colors["lime"], fg=self.colors["dark_green"],
            insertbackground=self.colors["dark_green"], relief="flat", bd=5
        ).pack(pady=(0, 8))

        # Scrollable list
        scrollable_container = tk.Frame(main_frame, bg=self.colors["cream"])
        scrollable_container.pack(fill="both", expand=True, pady=(10, 20))

        canvas = tk.Canvas(scrollable_container, bg=self.colors["cream"], highlightthickness=0)
        scrollbar = self.create_styled_scrollbar(scrollable_container)
        scrollbar.config(command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.scrollable_frame = tk.Frame(canvas, bg=self.colors["cream"])
        self._canvas_window = canvas.create_window((0, 0), window=self.scrollable_frame, anchor="n")

        def _update_scrollregion(_):
            canvas.configure(scrollregion=canvas.bbox("all"))
        self.scrollable_frame.bind("<Configure>", _update_scrollregion)

        # Inner-Frame-width
        def _resize_inner(evt):
            canvas.itemconfig(self._canvas_window, width=evt.width)
        canvas.bind("<Configure>", _resize_inner)

        import platform

        def _on_mousewheel(event):
            system = platform.system()
            if system == 'Darwin':  # Mac
                canvas.yview_scroll(-1 * event.delta, "units")
            else:  # Windows, Linux
                canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        def _on_button_4(event):
            canvas.yview_scroll(-1, "units")

        def _on_button_5(event):
            canvas.yview_scroll(1, "units")

        canvas.bind('<Enter>', lambda e: canvas.focus_set())
        canvas.bind("<MouseWheel>", _on_mousewheel)
        canvas.bind("<Button-4>", _on_button_4)
        canvas.bind("<Button-5>", _on_button_5)

        # Fetch all flashcards and display them
        self.all_flashcards = self.flashcard_manager.get_all_flashcards()
        self.update_flashcard_display()

    # Card item
    def create_flashcard_item(self, parent, flashcard):
        row = tk.Frame(parent, bg=self.colors["cream"])
        row.pack(fill="x", pady=4)

        # actual cards centered
        card_outer = tk.Frame(row, bg=self.colors["brown"],
                              width=self.FLASHCARD_CARD_WIDTH, height=self.FLASHCARD_CARD_HEIGHT)
        card_outer.pack()
        card_outer.pack_propagate(False)

        card_inner = tk.Frame(card_outer, bg=self.colors["sage"])
        card_inner.pack(fill="both", expand=True, padx=2, pady=2)

        content = tk.Frame(card_inner, bg=self.colors["cream"])
        content.pack(fill="both", expand=True, padx=3, pady=3)

        # text aligned left
        text_frame = tk.Frame(content, bg=self.colors["cream"])
        text_frame.pack(side="left", fill="both", expand=True, padx=10, pady=8)

        wrap_len = max(120, self.FLASHCARD_CARD_WIDTH - self.BUTTON_COLUMN_WIDTH - 40)

        tk.Label(
            text_frame,
            text=f"{flashcard[1]} → {flashcard[2]}",
            font=("Helvetica", 11, "bold"),
            bg=self.colors["cream"],
            fg=self.colors["dark_green"],
            anchor="w",
            justify="left",
            wraplength=wrap_len
        ).pack(side="left", fill="x", expand=True)

        # buttons flashcards
        buttons = tk.Frame(
            content,
            bg=self.colors["cream"],
            width=self.BUTTON_COLUMN_WIDTH,
            height=self.FLASHCARD_CARD_HEIGHT - 20  # z.B. 68 bei Höhe 88
        )
        buttons.pack(side="right", padx=10, pady=5)
        buttons.pack_propagate(False)

        self.create_small_button(buttons, "✏️ Edit", lambda: self.edit_flashcard(flashcard))
        self.create_small_button(buttons, "🗑️ Delete", lambda: self.delete_flashcard(flashcard[0]))

    # Data & actions
    def update_flashcard_display(self):
        if not self.scrollable_frame:
            return
        for w in self.scrollable_frame.winfo_children():
            w.destroy()

        query = self.search_var.get().lower().strip() if self.search_var else ""
        if query:
            self.filtered_flashcards = [fc for fc in self.all_flashcards
                                        if query in fc[1].lower() or query in fc[2].lower()]
        else:
            self.filtered_flashcards = self.all_flashcards[:]

        if not self.filtered_flashcards:
            empty = tk.Frame(self.scrollable_frame, bg=self.colors["cream"])
            empty.pack(pady=50)
            tk.Label(
                empty,
                text=("🔍 No flashcards found!" if query else
                      "📭 No flashcards yet!\nAdd your first flashcard to get started."),
                font=("Helvetica", 14),
                bg=self.colors["cream"], fg=self.colors["brown"], justify="center"
            ).pack()
            return

        for fc in self.filtered_flashcards:
            self.create_flashcard_item(self.scrollable_frame, fc)

    def filter_flashcards(self, *args):
        if self.scrollable_frame is not None:
            self.update_flashcard_display()

    def launch_memory_game(self):
        for w in self.root.winfo_children():
            w.destroy()
        flashcards = self.flashcard_manager.get_all_flashcards()
        if flashcards:
            MemoryGame(
                self.root,
                flashcards,
                on_exit=self.setup_main_menu,
                on_streak=self.increase_streak,
                left_plant=self._left_plant,
                right_plant=self._right_plant
            )
        else:
            messagebox.showinfo("No Flashcards", "Add flashcards before playing.")
            self.setup_main_menu()

    def launch_game_race(self):
        for w in self.root.winfo_children():
            w.destroy()
        flashcards = self.flashcard_manager.get_all_flashcards()
        if flashcards:
            RaceGame(
                self.root,
                self, flashcards,
                on_exit=self.setup_main_menu,
                on_streak=self.increase_streak,
                left_plant=self._left_plant,
                right_plant=self._right_plant
            )
        else:
            messagebox.showinfo("No Flashcards", "Add flashcards before playing.")

    def check_duplicate_flashcard(self, term, translation, exclude_id=None):
        flashcards = self.flashcard_manager.get_all_flashcards()
        t = term.lower().strip()
        tr = translation.lower().strip()
        for f in flashcards:
            if exclude_id and f[0] == exclude_id:
                continue
            if (f[1].lower().strip() == t or f[2].lower().strip() == tr or
                f[1].lower().strip() == tr or f[2].lower().strip() == t):
                return True
        return False

    def add_flashcard_with_translation(self):
        popup = tk.Toplevel(self.root)
        popup.title("Add Flashcard")
        popup.configure(bg=self.colors["cream"])
        popup.resizable(False, False)
        popup.transient(self.root)
        popup.grab_set()

        popup.geometry("400x350")
        x = self.root.winfo_rootx() + (self.root.winfo_width() - 400) // 2
        y = self.root.winfo_rooty() + (self.root.winfo_height() - 350) // 2
        popup.geometry(f"400x350+{x}+{y}")

        main_container = tk.Frame(popup, bg=self.colors["brown"])
        main_container.pack(fill="both", expand=True, padx=6, pady=6)

        outer = tk.Frame(main_container, bg=self.colors["sage"])
        outer.pack(fill="both", expand=True, padx=2, pady=2)

        inner = tk.Frame(outer, bg=self.colors["cream"])
        inner.pack(fill="both", expand=True, padx=4, pady=4)

        tk.Label(inner, text="📝 Add New Flashcard",
                 font=("Helvetica", 16, "bold"),
                 bg=self.colors["cream"], fg=self.colors["dark_green"]).pack(pady=(15, 20))

        tk.Label(inner, text="Enter term (word to translate):",
                 font=("Helvetica", 11, "bold"),
                 bg=self.colors["cream"], fg=self.colors["dark_green"]).pack(pady=(5, 2))

        term_entry = tk.Entry(inner, width=35, font=("Helvetica", 11),
                              bg=self.colors["lime"], fg=self.colors["dark_green"],
                              insertbackground=self.colors["dark_green"], relief="flat", bd=5)
        term_entry.pack(pady=(0, 15))

        tk.Label(inner, text="Select target language:",
                 font=("Helvetica", 11, "bold"),
                 bg=self.colors["cream"], fg=self.colors["dark_green"]).pack(pady=(5, 2))

        languages = ["french", "german", "spanish", "italian",
                     "portuguese", "russian", "japanese", "korean", "chinese (simplified)"]

        style = ttk.Style()
        style.theme_use('clam')
        style.configure('Custom.TCombobox',
                        fieldbackground=self.colors["lime"],
                        background=self.colors["sage"],
                        bordercolor=self.colors["sage"],
                        arrowcolor=self.colors["dark_green"])
        lang_var = tk.StringVar()
        ddl = ttk.Combobox(inner, textvariable=lang_var, values=languages,
                           state="readonly", width=32, font=("Helvetica", 11), style='Custom.TCombobox')
        ddl.set("french")
        ddl.pack(pady=(0, 20))

        def translate_and_save():
            term = term_entry.get().strip()
            language = lang_var.get().strip().lower()
            if not term:
                messagebox.showwarning("Missing Input", "Please enter a term.")
                return
            try:
                translated = GoogleTranslator(source='auto', target=language).translate(term)
            except Exception as e:
                messagebox.showerror("Translation Error", f"Error translating word:\n{e}")
                return

            confirmed = simpledialog.askstring(
                "Confirm Translation",
                f"Translation of '{term}' in {language}:", initialvalue=translated
            )
            if confirmed:
                confirmed = confirmed.strip()
                if self.check_duplicate_flashcard(term, confirmed):
                    messagebox.showwarning("Duplicate Flashcard",
                                           "A flashcard with this term or translation already exists!")
                    return
                self.flashcard_manager.add_flashcard(term, confirmed)
                popup.destroy()
                self.manage_flashcards()

        btn_row = tk.Frame(inner, bg=self.colors["cream"])
        btn_row.pack(pady=(10, 15))

        def mk_small(text, bg, cmd):
            outer = tk.Frame(btn_row, bg=self.colors["brown"])
            outer.pack(side="left", padx=10)
            inner = tk.Frame(outer, bg=bg)
            inner.pack(padx=2, pady=2)
            btn = tk.Button(inner, text=text, font=("Helvetica", 10, "bold"),
                            bg=bg, fg=self.colors["dark_green"], relief="flat", bd=0,
                            padx=15, pady=8, cursor="hand2", command=cmd)
            btn.pack(padx=3, pady=3)
            return btn

        mk_small("🌐 Translate and Save", self.colors["sage"], translate_and_save)
        mk_small("❌ Cancel", self.colors["lime"], popup.destroy)

        term_entry.focus_set()

    def edit_flashcard(self, flashcard):
        new_term = simpledialog.askstring("Edit Flashcard", "Edit term:", initialvalue=flashcard[1])
        if not new_term:
            return
        new_translation = simpledialog.askstring("Edit Flashcard", "Edit translation:", initialvalue=flashcard[2])
        if not new_translation:
            return
        if self.check_duplicate_flashcard(new_term.strip(), new_translation.strip(), exclude_id=flashcard[0]):
            messagebox.showwarning("Duplicate Flashcard", "A flashcard with this term or translation already exists!")
            return
        self.flashcard_manager.update_flashcard(flashcard[0], new_term.strip(), new_translation.strip())
        self.manage_flashcards()

    def delete_flashcard(self, flashcard_id):
        if messagebox.askyesno("Delete", "Are you sure you want to delete this flashcard?"):
            self.flashcard_manager.delete_flashcard(flashcard_id)
            self.manage_flashcards()


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("920x720")
    app = FlashcardApp(root)
    root.mainloop()
