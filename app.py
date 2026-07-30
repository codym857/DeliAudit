from flask import Flask, render_template, request, redirect, url_for, session, flash
import entry
import item
import audit
import user
from entry import Entry
from audit import Audit
from item import Item
import database
from datetime import datetime
from flask_bcrypt import Bcrypt
from user import User

app = Flask(__name__)
bcrypt = Bcrypt(app)
app.secret_key = '192b9bdd22ab9ed4d12e236c78afcb9a393ec15f71bbf5dc987d54727823bcbf'

database.create_tables()

@app.route('/home', methods=["POST", "GET"])
@app.route('/', methods=["POST", "GET"])
def home():
	inSession = False

	if session:
		inSession = True

	if request.method == "POST":
		storeNumber = request.form["storeNumber"]
		newAudit = Audit(storeNumber)
		newAudit.create_audit()
		auditID = audit.read_audit_from_store(storeNumber)[-1][0]
		return redirect(url_for('entries', auditID=auditID))

	return render_template('home.html', inSession=inSession)

@app.route('/audits/<auditID>')
def audits(auditID):
	if session:
		currentAudit = audit.read_audit_from_auditID(auditID)
		storeID = currentAudit[1]
		auditDate = datetime.strptime(str(currentAudit[2]), "%Y%m%d").strftime("%B %d, %Y")
		categorySums = audit.read_audit_by_categories(auditID)
		return render_template('audit.html', auditID = auditID, categorySums = categorySums, storeID = storeID, auditDate = auditDate)
	return redirect(url_for('home'))

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

@app.route('/register', methods=['GET', 'POST'])
def register():
	if request.method == "POST":
		username = request.form["username"]
		userEmail = request.form["userEmail"]
		unhashed_pw = request.form["unhashed_pw"]
		hashed_pw = bcrypt.generate_password_hash(unhashed_pw).decode('utf-8')
		newUser = User(username=username, userEmail=userEmail, hashed_pw=hashed_pw)
		newUser.create_user()
		return redirect(url_for('login'))
	return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == "POST":
		username = request.form["username"]
		unhashed_pw = request.form["unhashed_pw"]
		hashed_pw = user.get_hashed_pw(username)
		if(bcrypt.check_password_hash(hashed_pw, unhashed_pw)):
			session[username] = username
			return redirect(url_for('home'))
		return render_template('login.html')

	return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

@app.route('/upload', methods=['GET', 'POST'])
def upload():
	if request.method == "POST":
		if "file" not in request.files:
			flash("No file part found.")
			return redirect(url_for('itemEntry'))

		file = request.files["file"]

		if file.filename == "":
			flash("No file selected.")
			return redirect(url_for('itemEntry'))

		if file and (file.filename.endswith(".xlsx") or file.filename.endswith(".xls")):
			try:
				database.import_items_database(file.stream)
				flash(f"Successfully uploaded and imported data from {file.filename}")
				return redirect(url_for('itemEntry'))
			except Exception as e:
				flash(f"An error occurred while processing data: {str(e)}")
				return redirect(url_for('itemEntry'))
		else:
			flash("Invalid file format. Please upload an Excel (.xlsx or .xls) file.")
			return redirect(url_for('itemEntry'))

# if(__name__ == '__main__'):
# 	app.run(host='0.0.0.0', port=5000, debug=True)

if(__name__ == '__main__'):
	app.run()