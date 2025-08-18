# flashcard.py
import sqlite3
import os

class FlashcardManager:
    def __init__(self, db_path='db/flashcards.db'):
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

    def add_flashcard(self, term, translation):
        self.cursor.execute('INSERT INTO flashcards (term, translation) VALUES (?, ?)', (term, translation))
        self.conn.commit()

    def delete_flashcard(self, flashcard_id):
        self.cursor.execute('DELETE FROM flashcards WHERE id = ?', (flashcard_id,))
        self.conn.commit()

    def get_all_flashcards(self):
        self.cursor.execute('SELECT * FROM flashcards')
        return self.cursor.fetchall()

    def update_flashcard(self, flashcard_id, new_term, new_translation):
        self.cursor.execute('UPDATE flashcards SET term = ?, translation = ? WHERE id = ?',
                            (new_term, new_translation, flashcard_id))
        self.conn.commit()

    def get_flashcard_by_id(self, flashcard_id):
        self.cursor.execute('SELECT * FROM flashcards WHERE id = ?', (flashcard_id,))
        return self.cursor.fetchone()

    def close(self):
        self.conn.close()
