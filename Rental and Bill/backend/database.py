import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'rental_blossoms.db')

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Create expenses table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            room TEXT NOT NULL,
            type TEXT NOT NULL,
            amount REAL NOT NULL
        )
    ''')
    
    # Check if table is empty, if so, populate with initial data
    cursor.execute('SELECT COUNT(*) FROM expenses')
    count = cursor.fetchone()[0]
    
    if count == 0:
        initial_data = [
            ('01/06/26', 'Room A', 'Electricity Bill', 1200.0),
            ('01/06/26', 'Room B', 'Water Bill', 800.0),
            ('01/06/26', 'Room C', 'Internet', 300.0),
            ('01/06/26', 'Room D', 'Gas Bill', 500.0),
            ('01/06/26', 'Room E', 'Cleaning', 200.0)
        ]
        cursor.executemany('''
            INSERT INTO expenses (date, room, type, amount)
            VALUES (?, ?, ?, ?)
        ''', initial_data)
        
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
    print("Database initialized.")
