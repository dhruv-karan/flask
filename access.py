import sqlite3

conn = sqlite3.connect('db.sqlite')
c = conn.cursor()
c.execute("SELECT * FROM review")
results = c.fetchall()
conn.close()
print(results)