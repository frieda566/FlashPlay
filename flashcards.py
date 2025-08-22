# flashcard.py
import sqlite3
import os
from tkinter import messagebox

class FlashcardManager:
    def __init__(self, db_path='db/flashcards.db'):
        #Ensure the db/ folder exists
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS flashcards (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                term TEXT NOT NULL,
                translation TEXT NOT NULL
            )
        ''')
        self.conn.commit()

    def add_flashcard(self, term: str, translation: str):
        self.cursor.execute(
            'INSERT INTO flashcards (term, translation) VALUES (?, ?)', (term, translation)
        )
        self.conn.commit()

    def update_flashcard(self, flashcard_id: int, new_term: str, new_translation: str):
        self.cursor.execute(
            'UPDATE flashcards SET term = ?, translation = ? WHERE id = ?',
            (new_term, new_translation, flashcard_id)
        )
        self.conn.commit()

    def delete_flashcard(self, flashcard_id: int):
        self.cursor.execute('DELETE FROM flashcards WHERE id = ?', (flashcard_id,))
        self.conn.commit()

    def load_flashcards(self):
        self.cursor.execute('SELECT id, term, translation FROM flashcards')
        return self.cursor.fetchall()

    def get_flashcard_count(self) -> int:
        self.cursor.execute('SELECT COUNT(*) FROM flashcards')
        return self.cursor.fetchone()[0]

    def ensure_flashcards_exist(self, parent=None) -> bool:
        #Check if any flashcards exist. If none, show messagebox and return False.
        if self.get_flashcard_count() == 0:
            if parent:
                messagebox.showinfo(
                    'No flashcards',
                    f'No flashcards found. Please add some before playing.',
                    parent=parent
                )
            return False
        return True

    def clear_flashcards(self):
        self.cursor.execute('DELETE FROM flashcards')
        self.conn.commit()

    def get_all_flashcards(self):
        self.cursor.execute('SELECT id, term, translation FROM flashcards')
        return self.cursor.fetchall()

    def close(self):
        #Close the database connection
        self.conn.close()
