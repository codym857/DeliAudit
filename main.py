import sqlite3
import database
import audit
import item
import entry
from audit import Audit
from item import Item
from entry import Entry


database.create_tables()

userInput = input('Enter Audit ID: ')
print(entry.read_entries_by_audit(userInput))

# while True:
# 	userInput = input('Enter Audit ID: ')
# 	#Quit
# 	if(userInput == 'q'):
# 		break
# 	# elif(userInput == 'rc'):
# 		# userInput = input('>')
# 		# print(item.read_unitCost_from_itemID(userInput)[0][0])
# 	else:
# 		auditID = userInput
# 		itemID = input('Enter Item ID: ')
# 		quantity = input('Enter quantity: ')

# 		unitCostSnap = (item.read_unitCost_from_itemID(itemID))[0][0]
# 		extendedCost = round(unitCostSnap * float(quantity), 2)
# 		newEntry = Entry(auditID, itemID, unitCostSnap, extendedCost)
# 		newEntry.create_entry()


	# # Read AuditIDs from store number
	# elif(userInput == 'rs'):
	# 	userInput = input('>')
	# 	for i in audit.read_audit_from_store(userInput):
	# 		print(i[0])
	# # Read auditIDs from date	
	# elif(userInput == 'rd'):
	# 	userInput = input('>')
	# 	for i in audit.read_audit_from_date(userInput):
	# 		print(i[0])
	# # delete audit
	# elif(userInput == 'd'):
	# 	userInput = input('>')
	# 	delAuditValues = userInput.split(',')
	# 	delAudit = Audit(delAuditValues[0], delAuditValues[1])
	# 	delAudit.delete_audit()
	# # create audit
	# else:
	# 	newAuditValues = userInput.split(',')
	# 	newAudit = Audit(newAuditValues[0], newAuditValues[1])
	# 	newAudit.create_audit()