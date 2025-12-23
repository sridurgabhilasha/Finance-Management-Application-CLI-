import sqlite3
import hashlib
import os
from .init import DB_PATH

def hash_password(password):
    """Hash a password using SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(username, password):
    """Register a new user."""
    password_hash = hash_password(password)
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO users (username, password_hash) VALUES (?, ?)', (username, password_hash))
        conn.commit()
        conn.close()
        return True, "User registered successfully."
    except sqlite3.IntegrityError:
        return False, "Username already exists."
    except Exception as e:
        return False, str(e)

def login_user(username, password):
    """Authenticate a user."""
    password_hash = hash_password(password)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM users WHERE username = ? AND password_hash = ?', (username, password_hash))
    user = cursor.fetchone()
    conn.close()
    if user:
        return True, user[0]  # Return user ID
    else:
        return False, "Invalid username or password."
