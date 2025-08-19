# main.py
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
from flashcards import FlashcardManager
from game_memory import MemoryGame
from game_race import RaceGame
from deep_translator import GoogleTranslator

class FlashcardApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Interactive Vocabulary Flashcards")
        self.flashcard_manager = FlashcardManager()
        self.setup_main_menu()

    def setup_main_menu(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="Vocabulary Flashcards", font=("Helvetica", 18, "bold")).pack(pady=10)

        tk.Button(self.root, text="Play Memory Game", width=25, command=self.launch_memory_game).pack(pady=5)
        tk.Button(self.root, text="Play Race Game", width=25, command=self.launch_game_race).pack(pady=5)

        tk.Button(self.root, text="Manage Flashcards", width=25, command=self.manage_flashcards).pack(pady=5)
        tk.Button(self.root, text="Exit", width=25, command=self.root.quit).pack(pady=20)

    def launch_memory_game(self):
        for w in self.root.winfo_children():
            w.destroy()

        flashcards = self.flashcard_manager.get_all_flashcards()
        if flashcards:
            MemoryGame(self.root, flashcards, on_exit=self.setup_main_menu)
        else:
            messagebox.showinfo("No Flashcards", "Add flashcards before playing.")

    def launch_game_race(self):
        flashcards = self.flashcard_manager.get_all_flashcards()
        if flashcards:
            RaceGame(self.root, flashcards)
        else:
            messagebox.showinfo("No Flashcards", "Add flashcards before playing.")

    def manage_flashcards(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="Manage Flashcards", font=("Helvetica", 16)).pack(pady=10)

        flashcards = self.flashcard_manager.get_all_flashcards()
        for fc in flashcards:
            frame = tk.Frame(self.root)
            frame.pack(pady=2)

            tk.Label(frame, text=f"{fc[0]}. {fc[1]} → {fc[2]}", width=40, anchor="w").pack(side="left")

            tk.Button(frame, text="Edit", command=lambda f=fc: self.edit_flashcard(f)).pack(side="left", padx=5)
            tk.Button(frame, text="Delete", command=lambda f=fc: self.delete_flashcard(f[0])).pack(side="left")

        tk.Button(self.root, text="Add New Flashcard", command=self.add_flashcard_with_translation).pack(pady=10)
        tk.Button(self.root, text="Back to Main Menu", command=self.setup_main_menu).pack(pady=5)

    def add_flashcard_with_translation(self):
        popup = tk.Toplevel(self.root)
        popup.title("Add Flashcard")

        tk.Label(popup, text="Enter term (word to translate):").pack(pady=5)
        term_entry = tk.Entry(popup, width=30)
        term_entry.pack(pady=5)

        tk.Label(popup, text="Select language:").pack(pady=5)
        languages = [
            "french", "german", "spanish", "italian",
            "portuguese", "russian", "japanese", "korean", "chinese (simplified)"
        ]
        lang_var = tk.StringVar()
        lang_dropdown = ttk.Combobox(popup, textvariable=lang_var, values=languages, state="readonly", width=30)
        lang_dropdown.set("french")
        lang_dropdown.pack(pady=5)

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

        tk.Button(popup, text="Translate and Save", command=translate_and_save).pack(pady=10)
        tk.Button(popup, text="Cancel", command=popup.destroy).pack(pady=2)

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
    root.geometry("920x720")  # optional, gibt dem Grid Platz
    app = FlashcardApp(root)
    root.mainloop()
