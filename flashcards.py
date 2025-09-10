import sqlite3
import os
from tkinter import messagebox

class FlashcardManager:
    def __init__(self, db_path="db/flashcards.db"):
        #Ensure the db/ folder exists so SQLite can create the database file
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        # connect to the SQLite database (creates file if it doesn't exist)
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        # ensure the flashcards table exists
        self.create_table()

    def create_table(self):
        # create the flashcards table if it does not already exist
        self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS flashcards (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    term TEXT NOT NULL,
                    translation TEXT NOT NULL
                )
            ''')
        self.conn.commit()

    def add_flashcard(self, term: str, translation: str):
        # insert a new flashcard into the database
        self.cursor.execute(
            'INSERT INTO flashcards (term, translation) VALUES (?, ?)', (term, translation)
        )
        self.conn.commit()

    def update_flashcard(self, flashcard_id: int, new_term: str, new_translation: str):
        # update an existing flashcard's term and translation by ID
        self.cursor.execute(
            'UPDATE flashcards SET term = ?, translation = ? WHERE id = ?',
            (new_term, new_translation, flashcard_id)
        )
        self.conn.commit()

    def delete_flashcard(self, flashcard_id: int):
        # delete a flashcard by ID
        self.cursor.execute('DELETE FROM flashcards WHERE id = ?', (flashcard_id,))
        self.conn.commit()

    def load_flashcards(self):
        # retrieve all flashcards (id, term, translation)
        self.cursor.execute('SELECT id, term, translation FROM flashcards')
        return self.cursor.fetchall()

    def get_flashcard_count(self) -> int:
        # return the total number of flashcards in the database
        self.cursor.execute('SELECT COUNT(*) FROM flashcards')
        return self.cursor.fetchone()[0]

    def ensure_flashcards_exist(self, parent=None) -> bool:
        # check if any flashcards exist - if none exist, show messagebox and return False
        if self.get_flashcard_count() == 0:
            if parent:
                messagebox.showinfo(
                    "No flashcards",
                    f"No flashcards found. Please add some before playing.",
                    parent=parent
                )
            return False
        return True

    def clear_flashcards(self):
        # delete all flashcards
        self.cursor.execute('DELETE FROM flashcards')
        self.conn.commit()

    def get_all_flashcards(self):
        # fetch all flashcards
        self.cursor.execute('SELECT id, term, translation FROM flashcards')
        return self.cursor.fetchall()

    def close(self):
        # close the database connection
        self.conn.close()