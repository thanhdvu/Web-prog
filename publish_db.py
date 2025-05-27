import sqlite3
import os

db_path = os.path.abspath('instance/yonsei.db')

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS found_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        prdt_cl_nm TEXT,
        start_ymd TEXT,
        prdt_nm TEXT,
        ubuilding TEXT,
        description TEXT,
        image_path TEXT
    );
''')

conn.commit()
conn.close()
