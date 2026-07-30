import sqlite3
import item
from datetime import datetime

class Audit:
	def __init__(self, storeID):
		self.storeID = int(storeID)
		self.auditDate = int(datetime.now().strftime("%Y%m%d"))

	#create new audit
	def create_audit(self):
		with sqlite3.connect('deliAudit.db', isolation_level=None) as conn:
			cursor = conn.cursor()
			cursor.execute('INSERT INTO audits VALUES (NULL, ?, ?)', (self.storeID, self.auditDate))
			conn.commit()
		conn.close()

	#read audit number from store number

	#read date code from audit number

	#read store number from audit number

	#edit store number by audit number

	#edit date code by audit number

	#delete audit
	def delete_audit(self):
		with sqlite3.connect('deliAudit.db', isolation_level=None) as conn:
			cursor = conn.cursor()
			cursor.execute('DELETE FROM audits WHERE storeID = ? AND auditDate = ?', (self.storeID, self.auditDate))
			conn.commit()
		conn.close()

def read_audit_from_store(storeID):
	with sqlite3.connect('deliAudit.db', isolation_level=None) as conn:
		cursor = conn.cursor()
		cursor.execute('SELECT * FROM audits WHERE storeID = ?', (storeID,))
		return cursor.fetchall()

def read_audit_from_date(auditDate):
	with sqlite3.connect('deliAudit.db', isolation_level=None) as conn:
		cursor = conn.cursor()
		cursor.execute('SELECT auditID FROM audits WHERE auditDate = ?', (auditDate,))
		return cursor.fetchall()

def read_audit_by_categories(auditID):
	with sqlite3.connect('deliAudit.db', isolation_level=None) as conn:
		cursor = conn.cursor()

		categorySums = {}
		for i in (29, 30, 31, 32, 35, 45, 48):
			currentCatSum = 0.0
			currentCatValues = cursor.execute('SELECT extendedCost FROM auditEntries WHERE category = ? AND auditID = ?', (i, auditID)).fetchall()
			for j in currentCatValues:
				currentCatSum += j[0]
			categorySums[i] = f"{currentCatSum:,.2f}"

		return categorySums

def read_audit_from_auditID(auditID):
	with sqlite3.connect('deliAudit.db', isolation_level=None) as conn:
		cursor = conn.cursor()
		cursor.execute('SELECT * FROM audits WHERE auditID = ?', (auditID,))
		return cursor.fetchone()