import sqlite3

conn = sqlite3.connect('data.db')
curr = conn.cursor()
curr.execute('SELECT * FROM users')

records = curr.fetchall()

for record in records:
    print(record)
