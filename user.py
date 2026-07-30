import sqlite3
from flask_bcrypt import Bcrypt

class User:
	def __init__(self, username, userEmail, hashed_pw):
		self.username = username
		self.userEmail = userEmail
		self.hashed_pw = hashed_pw

	def create_user(self):
		with sqlite3.connect('deliAudit.db', isolation_level=None) as conn:
			cursor = conn.cursor()
			cursor.execute('INSERT INTO users VALUES (NULL, ?, ?, ?)', (self.username, self.userEmail, self.hashed_pw))
			conn.commit()
		conn.close()

def get_hashed_pw(username):
	with sqlite3.connect('deliAudit.db', isolation_level=None) as conn:
		cursor = conn.cursor()
		cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
		return cursor.fetchall()[0][3]
