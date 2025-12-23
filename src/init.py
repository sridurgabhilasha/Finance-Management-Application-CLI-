import sqlite3
import os

DB_PATH = 'finance.db'

def initialize_database():
    """Initialize the database and create necessary tables."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
    ''')
    
    # Create categories table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL
        )
    ''')
    
    # Create transactions table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            type TEXT NOT NULL,  -- 'income' or 'expense'
            amount REAL NOT NULL,
            category_id INTEGER,
            description TEXT,
            date TEXT DEFAULT CURRENT_DATE,
            FOREIGN KEY (user_id) REFERENCES users (id),
            FOREIGN KEY (category_id) REFERENCES categories (id)
        )
    ''')
    
    # Insert default categories
    default_categories = ['Food', 'Rent', 'Salary', 'Entertainment', 'Transportation', 'Utilities', 'Healthcare', 'Other']
    for cat in default_categories:
        cursor.execute('INSERT OR IGNORE INTO categories (name) VALUES (?)', (cat,))
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    initialize_database()
