import sqlite3
import os

conn = sqlite3.connect('db.sqlite')

c = conn.cursor()
c.execute('CREATE TABLE review'\
			'(input TEXT,feedback INTEGER,predict_percentage TEXT,mortality INT, date TEXT)')

ex1 = '123123123421'

c.execute('INSERT INTO review'\
		"(input,feedback,predict_percentage,mortality,date) VALUES "\
		"(?,?,?,?,DATETIME('now'))",(ex1,1,'23.2',0))

conn.commit()
conn.close()
