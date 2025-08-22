import tkinter as tk
from tkinter import messagebox, simpledialog, ttk, font
from flashcards import FlashcardManager
from game_memory import MemoryGame
from game_race import RaceGame
from deep_translator import GoogleTranslator


class FlashcardApp:
    def __init__(self, root):
        self.root = root
        self.root.title("FlashPlay - Interactive Vocabulary Learning")

        # Apply the same color scheme as your memory game
        self.colors = {
            "cream": "#F6E8B1",
            "sage": "#B0CC99",
            "brown": "#89725B",
            "lime": "#B7CA79",
            "dark_green": "#677E52",
        }

        # Set the main window background
        self.root.configure(bg=self.colors["cream"])

        self.flashcard_manager = FlashcardManager()
        self.setup_main_menu()

    def create_styled_button(self, parent, text, command, width=25, is_primary=True):
        """Create a button with the same styling as your memory game"""
        # Container for the button
        button_container = tk.Frame(parent, bg=self.colors["cream"])
        button_container.pack(pady=8)

        # Shadow/outer layer (brown)
        outer_frame = tk.Frame(button_container, bg=self.colors["brown"])
        outer_frame.pack()

        # Button background layer
        bg_color = self.colors["sage"] if is_primary else self.colors["lime"]
        inner_frame = tk.Frame(outer_frame, bg=bg_color)
        inner_frame.pack(padx=3, pady=3)

        # Actual button
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

        # Hover effects
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
        """Create smaller buttons for inline actions (Edit, Delete, etc.)"""
        # Small button container
        btn_container = tk.Frame(parent, bg=self.colors["cream"])
        btn_container.pack(side=side, padx=padx)

        # Shadow layer
        shadow_frame = tk.Frame(btn_container, bg=self.colors["brown"])
        shadow_frame.pack()

        # Button background
        bg_frame = tk.Frame(shadow_frame, bg=self.colors["lime"])
        bg_frame.pack(padx=2, pady=2)

        # Button
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

        # Hover effects
        def on_enter(_):
            btn.configure(bg=self.colors["sage"])
            bg_frame.configure(bg=self.colors["sage"])

        def on_leave(_):
            btn.configure(bg=self.colors["lime"])
            bg_frame.configure(bg=self.colors["lime"])

        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)

        return btn

    def create_flashcard_item(self, parent, flashcard):
        """Create a styled flashcard item for the management view"""
        # Main container with card-like styling
        card_container = tk.Frame(parent, bg=self.colors["brown"])
        card_container.pack(fill="x", padx=20, pady=4)

        # Inner card
        card_inner = tk.Frame(card_container, bg=self.colors["sage"])
        card_inner.pack(fill="x", padx=2, pady=2)

        # Content area
        content_frame = tk.Frame(card_inner, bg=self.colors["cream"])
        content_frame.pack(fill="x", padx=3, pady=3)

        # Flashcard text
        text_frame = tk.Frame(content_frame, bg=self.colors["cream"])
        text_frame.pack(side="left", fill="x", expand=True, padx=10, pady=8)

        card_font = font.Font(family="Helvetica", size=11, weight="bold")
        tk.Label(
            text_frame,
            text=f"{flashcard[0]}. {flashcard[1]} → {flashcard[2]}",
            font=card_font,
            bg=self.colors["cream"],
            fg=self.colors["dark_green"],
            anchor="w",
            wraplength=400
        ).pack(side="left", fill="x", expand=True)

        # Button frame
        button_frame = tk.Frame(content_frame, bg=self.colors["cream"])
        button_frame.pack(side="right", padx=10, pady=5)

        # Edit and Delete buttons
        self.create_small_button(button_frame, "✏️ Edit", lambda: self.edit_flashcard(flashcard))
        self.create_small_button(button_frame, "🗑️ Delete", lambda: self.delete_flashcard(flashcard[0]))

    def setup_main_menu(self):
        # Clear the window
        for widget in self.root.winfo_children():
            widget.destroy()

        # Set window background
        self.root.configure(bg=self.colors["cream"])

        # Main container
        main_frame = tk.Frame(self.root, bg=self.colors["cream"])
        main_frame.pack(fill="both", expand=True, padx=30, pady=30)

        # Title section
        title_frame = tk.Frame(main_frame, bg=self.colors["cream"])
        title_frame.pack(pady=(20, 30))

        # App icon/emoji
        icon_font = font.Font(family="Helvetica", size=36)
        icon_label = tk.Label(
            title_frame,
            text="📚",
            font=icon_font,
            bg=self.colors["cream"]
        )
        icon_label.pack()

        # Main title
        title_font = font.Font(family="Helvetica", size=24, weight="bold")
        title_label = tk.Label(
            title_frame,
            text="FlashPlay",
            font=title_font,
            bg=self.colors["cream"],
            fg=self.colors["dark_green"]
        )
        title_label.pack(pady=(5, 0))

        # Subtitle
        subtitle_font = font.Font(family="Helvetica", size=14)
        subtitle_label = tk.Label(
            title_frame,
            text="Interactive Vocabulary Learning",
            font=subtitle_font,
            bg=self.colors["cream"],
            fg=self.colors["brown"]
        )
        subtitle_label.pack(pady=(2, 20))

        # Button section
        button_frame = tk.Frame(main_frame, bg=self.colors["cream"])
        button_frame.pack(pady=20)

        # Game buttons (primary style)
        self.create_styled_button(button_frame, "🧠 Play Memory Game", self.launch_memory_game, is_primary=True)
        self.create_styled_button(button_frame, "🏃 Play Race Game", self.launch_game_race, is_primary=True)

        # Management button (secondary style)
        self.create_styled_button(button_frame, "⚙️ Manage Flashcards", self.manage_flashcards, is_primary=False)

        # Exit button (secondary style, smaller)
        self.create_styled_button(button_frame, "❌ Exit", self.root.quit, width=15, is_primary=False)

    def launch_memory_game(self):
        for w in self.root.winfo_children():
            w.destroy()

        flashcards = self.flashcard_manager.get_all_flashcards()
        if flashcards:
            MemoryGame(self.root, flashcards, on_exit=self.setup_main_menu)
        else:
            messagebox.showinfo("No Flashcards", "Add flashcards before playing.")
            self.setup_main_menu()

    def launch_game_race(self):
        flashcards = self.flashcard_manager.get_all_flashcards()
        if flashcards:
            RaceGame(self.root, flashcards)
        else:
            messagebox.showinfo("No Flashcards", "Add flashcards before playing.")

    def manage_flashcards(self):
        # Clear the window
        for widget in self.root.winfo_children():
            widget.destroy()

        # Set background
        self.root.configure(bg=self.colors["cream"])

        # Main container
        main_frame = tk.Frame(self.root, bg=self.colors["cream"])
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Header
        header_frame = tk.Frame(main_frame, bg=self.colors["cream"])
        header_frame.pack(fill="x", pady=(10, 20))

        # Title
        title_font = font.Font(family="Helvetica", size=20, weight="bold")
        tk.Label(
            header_frame,
            text="📝 Manage Flashcards",
            font=title_font,
            bg=self.colors["cream"],
            fg=self.colors["dark_green"]
        ).pack()

        # Scrollable frame for flashcards
        canvas = tk.Canvas(main_frame, bg=self.colors["cream"], highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.colors["cream"])

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Pack scrollable area
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Add flashcards
        flashcards = self.flashcard_manager.get_all_flashcards()

        if not flashcards:
            # No flashcards message
            no_cards_frame = tk.Frame(scrollable_frame, bg=self.colors["cream"])
            no_cards_frame.pack(pady=50)

            empty_font = font.Font(family="Helvetica", size=14)
            tk.Label(
                no_cards_frame,
                text="📭 No flashcards yet!\nAdd your first flashcard to get started.",
                font=empty_font,
                bg=self.colors["cream"],
                fg=self.colors["brown"],
                justify="center"
            ).pack()
        else:
            # Display flashcards
            for fc in flashcards:
                self.create_flashcard_item(scrollable_frame, fc)

        # Bottom controls
        control_frame = tk.Frame(main_frame, bg=self.colors["cream"])
        control_frame.pack(fill="x", pady=(20, 10))

        # Center the control buttons
        button_container = tk.Frame(control_frame, bg=self.colors["cream"])
        button_container.pack()

        # Control buttons
        self.create_styled_button(button_container, "➕ Add New Flashcard", self.add_flashcard_with_translation,
                                  width=20, is_primary=True)
        self.create_styled_button(button_container, "← Back to Main Menu", self.setup_main_menu, width=20,
                                  is_primary=False)

    def add_flashcard_with_translation(self):
        # Create styled popup
        popup = tk.Toplevel(self.root)
        popup.title("Add Flashcard")
        popup.configure(bg=self.colors["cream"])
        popup.resizable(False, False)
        popup.transient(self.root)
        popup.grab_set()

        # Center the popup
        popup.geometry("400x350")
        x = self.root.winfo_rootx() + (self.root.winfo_width() - 400) // 2
        y = self.root.winfo_rooty() + (self.root.winfo_height() - 350) // 2
        popup.geometry(f"400x350+{x}+{y}")

        # Main container with card styling
        main_container = tk.Frame(popup, bg=self.colors["brown"])
        main_container.pack(fill="both", expand=True, padx=6, pady=6)

        outer_frame = tk.Frame(main_container, bg=self.colors["sage"])
        outer_frame.pack(fill="both", expand=True, padx=2, pady=2)

        inner_frame = tk.Frame(outer_frame, bg=self.colors["cream"])
        inner_frame.pack(fill="both", expand=True, padx=4, pady=4)

        # Title
        title_font = font.Font(family="Helvetica", size=16, weight="bold")
        tk.Label(
            inner_frame,
            text="📝 Add New Flashcard",
            font=title_font,
            bg=self.colors["cream"],
            fg=self.colors["dark_green"]
        ).pack(pady=(15, 20))

        # Term entry
        tk.Label(
            inner_frame,
            text="Enter term (word to translate):",
            font=("Helvetica", 11, "bold"),
            bg=self.colors["cream"],
            fg=self.colors["dark_green"]
        ).pack(pady=(5, 2))

        term_entry = tk.Entry(
            inner_frame,
            width=35,
            font=("Helvetica", 11),
            bg=self.colors["lime"],
            fg=self.colors["dark_green"],
            insertbackground=self.colors["dark_green"],
            relief="flat",
            bd=5
        )
        term_entry.pack(pady=(0, 15))

        # Language selection
        tk.Label(
            inner_frame,
            text="Select target language:",
            font=("Helvetica", 11, "bold"),
            bg=self.colors["cream"],
            fg=self.colors["dark_green"]
        ).pack(pady=(5, 2))

        languages = [
            "french", "german", "spanish", "italian",
            "portuguese", "russian", "japanese", "korean", "chinese (simplified)"
        ]

        lang_var = tk.StringVar()

        # Style the combobox
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('Custom.TCombobox',
                        fieldbackground=self.colors["lime"],
                        background=self.colors["sage"],
                        bordercolor=self.colors["sage"],
                        arrowcolor=self.colors["dark_green"])

        lang_dropdown = ttk.Combobox(
            inner_frame,
            textvariable=lang_var,
            values=languages,
            state="readonly",
            width=32,
            font=("Helvetica", 11),
            style='Custom.TCombobox'
        )
        lang_dropdown.set("french")
        lang_dropdown.pack(pady=(0, 20))

        # Button functions
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
                self.flashcard_manager.add_flashcard(term, confirmed)
                popup.destroy()
                self.manage_flashcards()

        # Buttons
        button_frame = tk.Frame(inner_frame, bg=self.colors["cream"])
        button_frame.pack(pady=(10, 15))

        # Create popup buttons
        save_container = tk.Frame(button_frame, bg=self.colors["cream"])
        save_container.pack(side="left", padx=10)

        save_outer = tk.Frame(save_container, bg=self.colors["brown"])
        save_outer.pack()

        save_inner = tk.Frame(save_outer, bg=self.colors["sage"])
        save_inner.pack(padx=2, pady=2)

        save_btn = tk.Button(
            save_inner,
            text="🌐 Translate and Save",
            font=("Helvetica", 10, "bold"),
            bg=self.colors["sage"],
            fg=self.colors["dark_green"],
            relief="flat",
            bd=0,
            padx=15,
            pady=8,
            cursor="hand2",
            command=translate_and_save
        )
        save_btn.pack(padx=3, pady=3)

        # Cancel button
        cancel_container = tk.Frame(button_frame, bg=self.colors["cream"])
        cancel_container.pack(side="right", padx=10)

        cancel_outer = tk.Frame(cancel_container, bg=self.colors["brown"])
        cancel_outer.pack()

        cancel_inner = tk.Frame(cancel_outer, bg=self.colors["lime"])
        cancel_inner.pack(padx=2, pady=2)

        cancel_btn = tk.Button(
            cancel_inner,
            text="❌ Cancel",
            font=("Helvetica", 10, "bold"),
            bg=self.colors["lime"],
            fg=self.colors["dark_green"],
            relief="flat",
            bd=0,
            padx=15,
            pady=8,
            cursor="hand2",
            command=popup.destroy
        )
        cancel_btn.pack(padx=3, pady=3)

        # Focus on the term entry
        term_entry.focus_set()

    def edit_flashcard(self, flashcard):
        new_term = simpledialog.askstring("Edit Flashcard", "Edit term:", initialvalue=flashcard[1])
        if not new_term:
            return
        new_translation = simpledialog.askstring("Edit Flashcard", "Edit translation:", initialvalue=flashcard[2])
        if not new_translation:
            return
        self.flashcard_manager.update_flashcard(flashcard[0], new_term, new_translation)
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