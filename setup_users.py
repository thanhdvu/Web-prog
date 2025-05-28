import sqlite3
import os

users_db_path = os.path.abspath('users.db') 

conn = sqlite3.connect('users_db_path')
cursor = conn.cursor()

cursor.execute("DROP TABLE IF EXISTS users")

cursor.execute('''
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    reset_token TEXT,
    token_expiration TEXT
)
''')

conn.commit()
conn.close()






