from flask import Flask, redirect, url_for, request,render_template,jsonify,make_response
from datetime import timedelta, datetime
from flask_restful import Resource, Api
from flask_login import LoginManager, UserMixin, login_user,logout_user,current_user, login_required
from flask_sqlalchemy import SQLAlchemy
import re

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost:3306/tura12$userdb'
app.config['SQLALCHEMY_ECHO'] = True
app.secret_key = 'shhhh...iAmASecret!'
login_manager = LoginManager()
login_manager.init_app(app)
db = SQLAlchemy(app)

class Employees(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(75))
    last_name = db.Column(db.String(75))
    email = db.Column(db.String(75),unique=True) 
    username = db.Column(db.String(50),unique=True) 
    password = db.Column(db.String(100))
    age = db.Column(db.Integer(),nullable=True)
    address = db.Column(db.String(75))
    contact_number = db.Column(db.String(11))
    date_created = db.Column(db.DateTime(), default=datetime.now())
    rate = db.Column(db.Integer(),nullable=False)
    shift_id = db.Column(db.Integer(),nullable=False)
    last_updated = db.Column(db.DateTime(), default=datetime.now())
    salary_type_id = db.Column(db.Integer(),nullable=False)
    is_admin = db.Column(db.String(25), default=False)

@login_manager.user_loader
def load_user(user_id):
    return Employees.query.get(int(user_id))

@app.route('/')
def index():
	user = Employees.query.filter_by(username='TURA12',password='vandal12').first()
	login_user(user)
	return 'You are now logged in'

@app.route('/logout')
@login_required
def logout():
	logout_user()
	return "You are now logged out"

@app.route('/login')
def login():
	return render_template('login.html')

@app.route('/login/auth',methods=['POST','GET'])
def login_auth():
	if request.method == 'POST':
		username = request.form['uname']
		password = request.form['pword']
		print(username)
		print(password)
		user = Employees.query.filter_by(username=username,password=password).first()
		print(user.id)
		print(user.username)
		print(user.password)
		login_user(user)
	else:
		print("request method is not post")
	return redirect(url_for('home'))

@app.route('/signUp')
def signup():
    """Renders the about page."""
    return render_template(
        'signup.html',
        title='Sign up Page',
        year=datetime.now().year
	)

@app.route('/signUp_auth',methods = ['POST','GET'])
def signup_auth():
	if request.method == 'POST':
		userName = request.form['uname']
		passWord = request.form['pword']
		firstName = request.form['fname']
		lastName = request.form['lname']
		confirmPassword = request.form['pwordConf']
		age = request.form['age']
		email = request.form['email']
		contact_number = request.form['contact_number']
		address = request.form['address']
		rate = request.form['rate']
		shift_id = request.form['shiftId']
		salary_type = request.form['salaryType']
		is_admin = request.form['admin_rights']
		emailcheck = re.search('.+@.+\.[com|net]',email)
		if emailcheck:
			print(emailcheck)
		else:
			print("Invalid Email Entered")
			return "Invalid email Entered"
		if passWord == confirmPassword:
			user = Employees(first_name=firstName,
        					 last_name=lastName,
        					 username=userName,
        					 password=passWord,
        					 age=int(age),
        					 email=email,
        					 contact_number=contact_number,
        					 address=address,
        					 rate=int(rate),
        					 shift_id=int(shift_id),
        					 salary_type_id=int(salary_type),
        					 is_admin=is_admin
        					 )
			db.session.add(user)
			db.session.commit()
			return "User Added Successfully"
		else:
			print("Invalid Email Entered")
			return "The entered passwords did not match"

@app.route('/home')
@login_required
def home():
	return 'The Current user is ' + current_user.username

if __name__ == '__main__':
	app.run(debug=True)