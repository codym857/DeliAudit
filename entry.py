import sqlite3
import item

class Entry:
	def __init__(self, auditID, itemID, unitCostSnap, extendedCost):
		self.auditID = auditID
		self.itemID = itemID
		self.category = item.read_category_from_itemID(itemID)[0][0]
		self.unitCostSnap = unitCostSnap
		self.extendedCost = extendedCost

	def create_entry(self):
		with sqlite3.connect('deliAudit.db', isolation_level=None) as conn:
			cursor = conn.cursor()
			cursor.execute('INSERT INTO auditEntries VALUES (NULL, ?, ?, ?, ?, ?)', (self.auditID, self.itemID, self.category, self.unitCostSnap, self.extendedCost))
			conn.commit()
		conn.close()

	#read item number by entry number

	#read extended cost by entry number

	#edit item number

	#edit unit cost

	#edit extended cost

	#delete entry

def read_entries_by_audit(auditID):
	with sqlite3.connect('deliAudit.db', isolation_level=None) as conn:
		cursor = conn.cursor()
		cursor.execute('SELECT * FROM auditEntries WHERE auditID = ?', (auditID,))
		return cursor.fetchall()

