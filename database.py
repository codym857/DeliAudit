import sqlite3

def create_tables():
	with sqlite3.connect('deliAudit.db', isolation_level=None) as conn:
		cursor = conn.cursor()
		cursor.execute
		cursor.execute("""CREATE TABLE IF NOT EXISTS items (itemID INTEGER PRIMARY KEY AUTOINCREMENT, description TEXT NOT NULL,
															category INTEGER NOT NULL, unitCost REAL NOT NULL,
															unitType TEXT NOT NULL) STRICT""")
		cursor.execute("""CREATE TABLE IF NOT EXISTS audits (auditID INTEGER PRIMARY KEY AUTOINCREMENT, storeID INTEGER NOT NULL, 
															auditDate INTEGER NOT NULL) STRICT""")
		cursor.execute("""CREATE TABLE IF NOT EXISTS auditEntries (entryID INTEGER PRIMARY KEY AUTOINCREMENT, auditID INTEGER NOT NULL,
																  itemID INTEGER NOT NULL, category INTEGER NOT NULL, unitCostSnap REAL NOT NULL,
																  extendedCost REAL NOT NULL, FOREIGN KEY (auditID) REFERENCES audits(auditID)) STRICT""")
		cursor.execute("""CREATE TABLE IF NOT EXISTS users (userID INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT NOT NULL, 
															userEmail TEXT NOT NULL, hashed_pw TEXT NOT NULL) STRICT""")
		conn.commit()
	conn.close()