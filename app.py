from flask import Flask, render_template, request, redirect, url_for
import entry
import item
import audit
from entry import Entry
from audit import Audit
from item import Item
import database
from datetime import datetime

app = Flask(__name__)

database.create_tables()

@app.route('/home', methods=["POST", "GET"])
@app.route('/', methods=["POST", "GET"])
def home():
	if request.method == "POST":
		storeNumber = request.form["storeNumber"]
		newAudit = Audit(storeNumber)
		newAudit.create_audit()
		auditID = audit.read_audit_from_store(storeNumber)[-1][0]
		return redirect(url_for('entries', auditID=auditID))

	return render_template('home.html')

@app.route('/audits/<auditID>')
def audits(auditID):
	currentAudit = audit.read_audit_from_auditID(auditID)
	storeID = currentAudit[1]
	auditDate = datetime.strptime(str(currentAudit[2]), "%Y%m%d").strftime("%B %d, %Y")
	categorySums = audit.read_audit_by_categories(auditID)
	return render_template('audit.html', auditID = auditID, categorySums = categorySums, storeID = storeID, auditDate = auditDate)

@app.route('/entries/<auditID>', methods=["POST", "GET"])
def entries(auditID):
	
	results = ('', '', '', '', '')
	currentAudit = audit.read_audit_from_auditID(auditID)
	storeID = currentAudit[1]
	auditDate = datetime.strptime(str(currentAudit[2]), "%Y%m%d").strftime("%B %d, %Y")
	searching = False

	if request.method == "POST":
		itemQuery = request.form["itemQuery"]
		results = item.read_items_by_partial(itemQuery)
		searching = True

	auditEntries = entry.read_entries_by_audit(auditID)
	return render_template('entries.html', auditID = auditID, auditEntries = auditEntries, results = results, storeID = storeID, auditDate = auditDate, searching = searching)

@app.route('/record', methods=["POST", "GET"])
def record():
	if request.method == "POST":
		itemID = request.form["itemID"]
		quantity = request.form["quantity"]
		auditID = (request.form["auditID"])[:-1]
		unitCostSnap = (item.read_unitCost_from_itemID(itemID))[0][0]
		extendedCost = round(unitCostSnap * float(quantity), 2)
		newEntry = Entry(int(auditID), itemID, unitCostSnap, extendedCost)
		newEntry.create_entry()

	return redirect(url_for('entries', auditID=auditID))

@app.route('/finalize', methods=["POST", "GET"])
def finalize():
	if request.method == "POST":
		auditID = request.form["auditID"]

	return redirect(url_for('audits', auditID=auditID))

@app.route('/searchAudits', methods=["POST", "GET"])
def searchAudits():
	if request.method == "POST":
		storeNumber = request.form["storeNumber"]
		searchAudits = audit.read_audit_from_store(storeNumber)
		return render_template('searchAudits.html', storeID=storeNumber, searchAudits=searchAudits)

@app.route('/itemEntry', methods=["POST", "GET"])
def itemEntry():
	if request.method == "POST":
		description = request.form["description"]
		category = request.form["category"]
		unitCost = request.form["unitCost"]
		unitType = request.form["unitType"]

		newItem = Item(description, category, unitCost, unitType)
		newItem.create_item()

	return render_template('itemEntry.html')

if(__name__ == '__main__'):
	app.run(host='0.0.0.0', port=5000, debug=True)