from flask import Flask, redirect, url_for, request,render_template,jsonify,make_response
from datetime import timedelta, datetime
from flask_restful import Resource, Api
from flask_login import LoginManager, UserMixin, login_user,logout_user,current_user, login_required
from flask_sqlalchemy import SQLAlchemy
from flask_paginate import Pagination, get_page_args
from app import app
from model import Employees, work_shifts, Employee_status, Salary_type, Employee_attendance, db
from employee_class import Employee_class
import re

empClass = Employee_class()
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return Employees.query.get(int(user_id))

@app.route('/')
@login_required
def index():
	return redirect(url_for('home'))

@app.route('/login')
def login():
	return render_template('login.html', year=datetime.now().year, title='Login')

@app.route('/login/auth',methods=['POST','GET'])
def login_auth():
	if request.method == 'POST':
		username = request.form['uname']
		password = request.form['pword']
		try:
			user = Employees.query.filter_by(username=username,password=password).first()
			login_user(user)
		except:
			return render_template('invalid_login.html', year=datetime.now().year)
	return redirect(url_for('home'))

@app.route('/logout')
@login_required
def logout():
	logout_user()
	return redirect(url_for('login'))

@app.route('/signUp')
def signup():
    """Renders the about page."""
    return render_template(
        'signup.html',
        title='Sign up',
        year=datetime.now().year
	)

@app.route('/signUp_auth',methods = ['POST','GET'])
def signup_auth():
	if request.method == 'POST':
		passWord = request.form['pword']
		confirmPassword = request.form['pwordConf']
		employeeInfoDict = {
			"userName" : request.form['uname'],
			"passWord" : request.form['pword'],
			"confirmPassword" : request.form['pwordConf'],
			"firstName" : request.form['fname'],
			"lastName" : request.form['lname'],
			"age" : request.form['age'],
			"email" : request.form['email'],
			"contact_number" : request.form['contact_number'],
			"address" : request.form['address'],
			"rate" : request.form['rate'],
			"shift_id" : request.form['shiftId'],
			"salary_type" : request.form['salaryType'],
			"is_admin" : request.form['admin_rights']
		}
		
		emailcheck = re.search('.+@.+\.[com|net]',employeeInfoDict["email"])
		if emailcheck:
			print(emailcheck)
		else:
			return "Invalid email Entered"
		if passWord == confirmPassword:
			employeeAdd = empClass.addUser(employeeInfoDict)
			return render_template('signup.html',  year=datetime.now().year)
		else:
			return "The entered passwords did not match"

@app.route('/home')
@login_required
def home():
    return render_template('index.html',message= 'The Current user is ' + current_user.username,  year=datetime.now().year, title='Home')

def get_users(offset=0, per_page=1):
    result = Employees.query.all()
    return result[offset: offset + per_page]

@app.route('/users')
@login_required
def users():
	result = Employees.query.all()
	page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page')
	pagination_users = get_users(offset=offset, per_page=per_page)
	total = len(result)
	pagination = Pagination(page=page, per_page=per_page, total=total,
                            css_framework='bootstrap4')
	return render_template('test.html',
                            message= 'The Current user is ' + current_user.username,  
                            year=datetime.now().year, 
                            users=pagination_users,
                            page=page,per_page=per_page,
                            pagination=pagination,
                            title='User Page v2')

@app.route('/users/info', methods=['GET','POST'])
@login_required
def employeeInfo():
	if request.method == 'POST':
		user = request.form['button']
		try:
			employee = Employees.query.filter_by(id=user).first()
		except:
			return "User was not found in the database"	
	return render_template('employee.html', result=employee, title=employee.username + " info", message= 'The Current user is ' + current_user.username,  year=datetime.now().year)

@app.route('/users/info/edit', methods=['GET','POST'])
@login_required
def editUser():
	if request.method == 'POST':
		action = request.form['btn_action']
		if action == 'Go Back to Users':
			return redirect(url_for('users'))
		else:
			result = Employees.query.filter_by(id=action).first()
			return render_template('userEdit.html',title='Edit User',year=datetime.now().year , employee=result)

@app.route('/users/info/update', methods=['GET','POST'])
@login_required
def updateUser():
	if request.method == 'POST':
		employeeInfoDict = {
			"user_id" : request.form['btn_submit'],
			"userName" : request.form['uname'],
			"passWord" : request.form['pword'],
			"firstName" : request.form['fname'],
			"lastName" : request.form['lname'],
			"age" : request.form['age'],
			"email" : request.form['email'],
			"contact_number" : request.form['contact_number'],
			"address" : request.form['address'],
			"rate" : request.form['rate'],
			"shift_id" : request.form['shiftId'],
			"salary_type" : request.form['salaryType'],
			"is_admin" : request.form['admin_rights']
		}
		editResult = empClass.editUser(employeeInfoDict)
		return render_template('userEdit.html', employee=editResult[1], message=editResult[0])
		
@app.route('/payroll')
@login_required
def payroll():
    return render_template('payroll.html',message= 'The Current user is ' + current_user.username)

@app.route('/payroll/timeIn', methods=['POST','GET'])
@login_required
def time_in():
    # TO DO TIME IN FUNCTION
    if request.method == 'POST':
        time_in = datetime.now().time()
        work_shift_id = Employees.query.join(work_shifts).add_columns(work_shifts.time_in, work_shifts.time_out).first()
        print(time_in)    
        print("TIME IN: " + str(work_shift_id[1]) + "TIME OUT: "+ str(work_shift_id[2]))
        if time_in > work_shift_id[1] and time_in < work_shift_id[2]:
            return "PRESENT"
        if time_in > work_shift_id[1] and time_in < work_shift_id[2]:
            return "LATE"
        else:
            return "ABSENT"
        emp_time_in = {
        "employee_id" : str(current_user.id),
        "employee_status_id" : '#',
        "penalty" : '#'
    }
    return "Payroll Time-in"

if __name__ == '__main__':
	app.run(debug=True)