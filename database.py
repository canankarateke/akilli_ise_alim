import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

DB_NAME = 'recruitment.db'

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    conn.execute('''
    CREATE TABLE IF NOT EXISTS adaylar (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        isim TEXT DEFAULT 'İsimsiz Aday',
        deneyim INTEGER,
        egitim INTEGER,
        skill INTEGER,
        test_skoru INTEGER,
        tahmin_sonucu TEXT,
        tarih TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    conn.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE,
        username TEXT UNIQUE,
        password TEXT
    )
    """)
    conn.commit()
    conn.close()

def save_user(email, username, password):
    conn = sqlite3.connect(DB_NAME)
    hashed_pw = generate_password_hash(password)   # 🔑 şifre hashleniyor
    conn.execute("""
        INSERT INTO users (email, username, password)
        VALUES (?, ?, ?)
    """, (email, username, hashed_pw))
    conn.commit()
    conn.close()

def check_user(username_or_email, password):
    conn = get_db_connection()
    user = conn.execute(
        'SELECT * FROM users WHERE username = ? OR email = ?',
        (username_or_email, username_or_email)
    ).fetchone()
    conn.close()
    if user and check_password_hash(user['password'], password):  # 🔑 hash doğrulama
        return True
    return False
