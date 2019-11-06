from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin
from datetime import timedelta, datetime
from app import app

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
    shift_id = db.Column(db.Integer(),db.ForeignKey('work_shifts.id'), nullable=False)
    last_updated = db.Column(db.DateTime(), default=datetime.now())
    salary_type_id = db.Column(db.Integer(),db.ForeignKey('salary_type.id'), nullable=False)
    is_admin = db.Column(db.String(25), default=False)

class Employee_attendance(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    business_date = db.Column(db.DateTime(), default = datetime.now().strftime("%x"))
    employee_id = db.Column(db.Integer())
    time_in = db.Column(db.Time(), default=datetime.now().time())
    time_out = db.Column(db.Time(), default=datetime.now().time())
    employee_status_id = db.Column(db.Integer(),db.ForeignKey('employee_status.id'), nullable=False)
    date_created = db.Column(db.DateTime(), default=datetime.now())
    last_updated = db.Column(db.DateTime(), default=datetime.now())
    penalty = db.Column(db.Integer())

class work_shifts(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    shift_name = db.Column(db.String())
    time_in = db.Column(db.Time())
    time_out = db.Column(db.Time())
    reference = db.relationship('Employees', backref='work_shifts' , lazy='joined')

class Employee_status(db.Model):
    id =  db.Column(db.Integer, primary_key = True)
    description = db.Column(db.String())
    reference = db.relationship('Employee_attendance', backref='employee_status' , lazy='joined')

class Salary_type(db.Model):
    id =  db.Column(db.Integer, primary_key = True)
    type_definition = db.Column(db.String())
    reference = db.relationship('Employees', backref='salary_type' , lazy='joined')