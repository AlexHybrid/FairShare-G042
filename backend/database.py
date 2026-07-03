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
            amount REAL NOT NULL,
            payment_method TEXT,
            category TEXT,
            notes TEXT,
            receipt_path TEXT,
            is_recurring INTEGER DEFAULT 0,
            status TEXT DEFAULT 'Pending'
        )
    ''')
    
    # Migration: Add columns if they don't exist
    columns = [row[1] for row in cursor.execute('PRAGMA table_info(expenses)').fetchall()]
    if 'payment_method' not in columns:
        cursor.execute('ALTER TABLE expenses ADD COLUMN payment_method TEXT')
    if 'category' not in columns:
        cursor.execute('ALTER TABLE expenses ADD COLUMN category TEXT')
    if 'notes' not in columns:
        cursor.execute('ALTER TABLE expenses ADD COLUMN notes TEXT')
    if 'receipt_path' not in columns:
        cursor.execute('ALTER TABLE expenses ADD COLUMN receipt_path TEXT')
    if 'is_recurring' not in columns:
        cursor.execute('ALTER TABLE expenses ADD COLUMN is_recurring INTEGER DEFAULT 0')
    if 'status' not in columns:
        cursor.execute('ALTER TABLE expenses ADD COLUMN status TEXT DEFAULT "Pending"')
    
    # Check if table is empty, if so, populate with initial data
    cursor.execute('SELECT COUNT(*) FROM expenses')
    count = cursor.fetchone()[0]
    
    if count == 0:
        initial_data = [
            ('01/06/26', 'Room A', 'Electricity Bill', 1200.0, 'Cash', 'Utilities', '', '', 0, 'Paid'),
            ('01/06/26', 'Room B', 'Water Bill', 800.0, 'Cash', 'Utilities', '', '', 0, 'Paid'),
            ('01/06/26', 'Room C', 'Internet', 300.0, 'Bank Transfer', 'Utilities', '', '', 0, 'Paid'),
            ('01/06/26', 'Room D', 'Gas Bill', 500.0, 'Cash', 'Utilities', '', '', 0, 'Paid'),
            ('01/06/26', 'Room E', 'Cleaning', 200.0, 'Cash', 'Maintenance', '', '', 0, 'Paid')
        ]
        cursor.executemany('''
            INSERT INTO expenses (date, room, type, amount, payment_method, category, notes, receipt_path, is_recurring, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', initial_data)
        
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
    print("Database initialized.")
