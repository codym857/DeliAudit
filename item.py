import sqlite3

class Item:
	#init
	def __init__(self, description, category, unitCost, unitType):
		self.description = str(description)
		self.category = int(category)
		self.unitCost = float(unitCost)
		self.unitType = str(unitType)

	#create new item
	def create_item(self):
		with sqlite3.connect('deliAudit.db', isolation_level=None) as conn:
			cursor = conn.cursor()
			cursor.execute('INSERT INTO items VALUES (NULL, ?, ?, ?, ?)', (self.description, self.category, self.unitCost, self.unitType))
			conn.commit()
		conn.close()

	#add to item master list

	#read item appearances in a single audit

	#read item description from item number

	#read item number from description

	#read item category from item number


	#read unit type in master item list by item number

	#edit description by item number

	#edit category by item number

	#edit unit cost by item number

	#edit unit type by item number

	#delete item

#read item unit cost from item number
def read_unitCost_from_itemID(itemID):
	with sqlite3.connect('deliAudit.db', isolation_level=None) as conn:
		cursor = conn.cursor()
		cursor.execute('SELECT unitCost FROM items WHERE itemID = ?', (itemID,))
		return cursor.fetchall()

def read_category_from_itemID(itemID):
	with sqlite3.connect('deliAudit.db', isolation_level=None) as conn:
		cursor = conn.cursor()
		cursor.execute('SELECT category FROM items WHERE itemID = ?', (itemID,))
		return cursor.fetchall()

def read_items_by_partial(partial):
	with sqlite3.connect('deliAudit.db', isolation_level=None) as conn:
		cursor = conn.cursor()
		cursor.execute('SELECT * FROM items WHERE description LIKE ?', (f"%{partial}%",))
		return cursor.fetchall()