import sqlite3

conn = sqlite3.connect('users.db')
cursor = conn.cursor()

cursor.execute("DROP TABLE IF EXISTS users")

cursor.execute('''
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
)
''')

conn.commit()
conn.close()






